#!/usr/bin/env python3
# Unfinished-Bench
# Copyright (c) 2026-present NAVER Corp.
# Apache-2.0
"""Container setup. Runs inside the container as /utils/setup.py and removes itself and its inputs when done.
Reads seed.json (written by the task builder) and:
  0) scenario time: if seed.clock is set, resolves every time placeholder (@@T..@@) against the clock
     (seed, text under /outputs, /instruction/task.md).
  1) installs tools: opskit.py -> site-packages, other *.py -> /usr/local/bin/<name>
  2) writes /etc/opskit/identity.json and the global git user
  3) replays repositories commit by commit with their authors and dates (tags included)
  4) writes service state: per services.<name>, json/sqlite/files under /var/lib/<name>/ and past records in
     /var/log/<name>/audit.log. JSON values "@head" and "@tag:<tag>" become real commit hashes from that service's repo.
     The last past record carries the current state's rev (opskit.state_rev); the evaluator uses it to detect edits
     made outside the tools.
  4b) file times: tools, identity and service state get mtimes that fit the story (set_file_times); parent folder
     times are restored.
  5) cleanup: /utils, /npc and the contents of /workspace.
Server split (OPSKIT_ROLE): server = server container (tool sources in /srv/opsapi/lib, service state and audit logs,
  repositories in /srv/opsapi/repos only to resolve commit references, config.json; prints 'anchor=<time>' at the end);
  agent = agent container (thin clients, identity and client.json, repositories in /outputs; scenario time from
  OPSKIT_ANCHOR, the same value as the server). The default (local) puts everything in one container.
"""
import datetime
import json
import os
import re
import shutil
import sqlite3
import subprocess
import sys
import sysconfig

SEED = "/utils/seed.json"
OUT = "/outputs"
ROLE = os.environ.get("OPSKIT_ROLE", "local")          # local | server | agent
SRV = "/srv/opsapi"


def sh(args, cwd=None, env=None):
    r = subprocess.run(args, cwd=cwd, env=env, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"{args}: {r.stderr.strip()}")
    return r.stdout.strip()


def install_tools(seed):
    if ROLE == "server":                      # tool sources go to a server-only folder (imported as modules), plus the server program and config
        os.makedirs(os.path.join(SRV, "lib"), exist_ok=True)
        for t in seed["tools"]:
            shutil.copy(os.path.join("/utils/tools", t), os.path.join(SRV, "lib", t))
        shutil.copy("/utils/opsapi.py", os.path.join(SRV, "opsapi.py"))
        _cfg = dict(seed.get("server") or {})
        _idn = seed.get("identity") or {}
        if _idn.get("user"):                  # the server accepts only this identity (editing identity.json or the request identity does not let the agent act as someone else)
            _cfg["issued_identity"] = dict(_idn, roles=list(_idn.get("roles") or []))
        with open(os.path.join(SRV, "config.json"), "w") as f:
            json.dump(_cfg, f, indent=1)
        sys.path.insert(0, os.path.join(SRV, "lib"))
        return
    site = sysconfig.get_paths()["purelib"]
    for t in seed["tools"]:
        src = os.path.join("/utils/tools", t)
        if t == "opskit.py":
            shutil.copy(src, os.path.join(site, "opskit.py"))
        else:
            dst = os.path.join("/usr/local/bin", t[:-3])
            shutil.copy(src, dst)
            os.chmod(dst, 0o755)


def write_identity(seed):
    os.makedirs("/etc/opskit", exist_ok=True)
    with open("/etc/opskit/identity.json", "w") as f:
        json.dump(seed["identity"], f, indent=2)
    if seed.get("client"):                    # split agent: service addresses
        with open("/etc/opskit/client.json", "w") as f:
            json.dump(seed["client"], f, indent=2)
    name = seed["identity"]["display_name"]
    email = seed["identity"].get("email") or (seed["identity"]["user"] + "@" + seed.get("mail_domain", "localhost"))
    sh(["git", "config", "--global", "user.name", name])
    sh(["git", "config", "--global", "user.email", email])
    sh(["git", "config", "--global", "init.defaultBranch", "main"])
    sh(["git", "config", "--global", "--add", "safe.directory", "*"])
    # The shell user is the task's employee: with `whoami` = root while the tools use another account, the
    # environment reads as simulated. The employee becomes the first name for uid 0 (permissions and paths unchanged;
    # the harness uses root paths). The driver gives agent commands HOME, USER and LOGNAME of this user (AGENT_USER).
    import re as _re
    user = seed["identity"]["user"]
    if _re.fullmatch(r"[a-z_][a-z0-9._-]{0,31}", user):
        with open("/etc/passwd") as f:
            lines = f.read().splitlines()
        if not any(l.startswith(user + ":") for l in lines):
            lines.insert(0, f"{user}:x:0:0:{name}:/home/{user}:/bin/bash")
            with open("/etc/passwd", "w") as f:
                f.write("\n".join(lines) + "\n")
        # sudo refuses users without a shadow entry ('account validation failure'): add a password-less entry and a
        #   cloud-server style sudoers file. set_file_times dates them to when the account was created.
        if os.path.isfile("/etc/shadow"):
            with open("/etc/shadow") as f:
                sh_lines = f.read().splitlines()
            if not any(l.startswith(user + ":") for l in sh_lines):
                sh_lines.insert(0, f"{user}:*:{19500 + len(user) * 7}:0:99999:7:::")
                with open("/etc/shadow", "w") as f:
                    f.write("\n".join(sh_lines) + "\n")
        if os.path.isdir("/etc/sudoers.d") and shutil.which("sudo"):
            sd = os.path.join("/etc/sudoers.d", re.sub(r"[^A-Za-z0-9_-]", "_", user))
            if not os.path.exists(sd):
                with open(sd, "w") as f:
                    f.write(f"{user} ALL=(ALL:ALL) NOPASSWD:ALL\n")
                os.chmod(sd, 0o440)
        home = f"/home/{user}"
        os.makedirs(home, exist_ok=True)
        for src in ("/etc/skel/.bashrc", "/etc/skel/.profile", "/etc/skel/.bash_logout", os.path.expanduser("~/.gitconfig")):
            if os.path.isfile(src):
                shutil.copy(src, os.path.join(home, os.path.basename(src)))
        populate_home(home, user, seed)


def populate_home(home, user, seed):
    """Make the home folder look like a used account (a home with only a few files from today reads as a new account).
    .bash_history holds only git and ls commands in these repositories, never file reads (cat etc.): a line that opened
    the task document would reveal where it is in positions that do not say so. No tool calls or remote commands
    (there is no remote). Files the scenario already placed are not overwritten; set_file_times sets the times.
    The Hermes folder (/root/.hermes in the image) is moved here too, so the home folder's time is not the cell start."""
    import hashlib, random
    if os.path.isdir("/root/.hermes") and not os.path.exists(os.path.join(home, ".hermes")):
        shutil.move("/root/.hermes", os.path.join(home, ".hermes"))
    hist = os.path.join(home, ".bash_history")
    if os.path.exists(hist):
        return
    rng = random.Random(int(hashlib.sha256(user.encode()).hexdigest()[:8], 16))
    repos = [r for r in seed.get("repos", []) if r.get("commits")]
    lines = []
    for _ in range(rng.randint(5, 8)):
        if not repos:
            break
        r = rng.choice(repos)
        lines.append(f"cd {os.path.join(OUT, r['path'])}")
        prev = None
        for _ in range(rng.randint(2, 5)):
            k = rng.random()
            if k < 0.35:
                c = "git status"
            elif k < 0.60:
                c = rng.choice(["git log --oneline -n 15", "git log --oneline -n 20", "git log -3 --stat"])
            elif k < 0.75:
                c = rng.choice(["git diff", "git diff --stat", "git branch -a"])
            else:
                c = rng.choice(["ls", "ls -la", "ls -l"])
            if c != prev:
                lines.append(c)
            prev = c
        lines.append(rng.choice(["cd ..", "cd ~", "cd"]))
        if rng.random() < 0.3:
            lines.append(rng.choice(["clear", "ls", "exit"]))
    lines.append("exit")
    with open(hist, "w") as f:
        f.write("\n".join(lines) + "\n")
    os.chmod(hist, 0o600)


def build_repo(repo, base=OUT):
    root = os.path.join(base, repo["path"])
    os.makedirs(root, exist_ok=True)
    sh(["git", "init", "-q", "-b", repo.get("branch", "main")], cwd=root)
    for c in repo["commits"]:
        for rel, content in c["files"].items():
            p = os.path.join(root, rel)
            if content is None:
                if os.path.exists(p):
                    os.remove(p)
                continue
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "w") as f:
                f.write(content)
        sh(["git", "add", "-A"], cwd=root)
        name, email = c["author"]
        env = dict(os.environ, GIT_AUTHOR_NAME=name, GIT_AUTHOR_EMAIL=email, GIT_AUTHOR_DATE=c["date"],
                   GIT_COMMITTER_NAME=name, GIT_COMMITTER_EMAIL=email, GIT_COMMITTER_DATE=c["date"])
        sh(["git", "commit", "-q", "-m", c["message"]], cwd=root, env=env)
        if c.get("tag"):
            sh(["git", "tag", c["tag"]], cwd=root, env=env)
    return root


def resolve_refs(obj, repo_root):
    if isinstance(obj, dict):
        return {k: resolve_refs(v, repo_root) for k, v in obj.items()}
    if isinstance(obj, list):
        return [resolve_refs(v, repo_root) for v in obj]
    if isinstance(obj, str) and repo_root:
        if obj == "@head":
            return sh(["git", "rev-parse", "HEAD"], cwd=repo_root)
        if obj.startswith("@tag:"):
            return sh(["git", "rev-parse", obj[5:] + "^{commit}"], cwd=repo_root)
    return obj


def seed_service(name, spec, repo_roots):
    d = os.path.join("/var/lib", name)
    os.makedirs(d, exist_ok=True)
    root = repo_roots.get(spec.get("repo")) if spec.get("repo") else None
    for fname, obj in (spec.get("json") or {}).items():
        with open(os.path.join(d, fname), "w") as f:
            json.dump(resolve_refs(obj, root), f, indent=2, sort_keys=True)
    for fname, db in (spec.get("sqlite") or {}).items():
        con = sqlite3.connect(os.path.join(d, fname))
        con.executescript(db["schema"])
        for table, rows in (db.get("rows") or {}).items():
            for r in rows:
                cols = list(r.keys())
                con.execute(f"INSERT INTO {table} ({','.join(cols)}) VALUES ({','.join('?' * len(cols))})", [r[c] for c in cols])
        con.commit(); con.close()
    for rel, text in (spec.get("files") or {}).items():
        p = os.path.join(d, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w") as f:
            f.write(text)


def write_audit(name, records):
    """Write past records in time order; the last one carries the current state's rev (same computation as opskit)."""
    import opskit  # installed by install_tools (site-packages; /srv/opsapi/lib on the split server)
    if not records:
        raise RuntimeError(f"service {name}: audit history is empty (world must provide past records)")
    recs = sorted(records, key=lambda r: r["ts"])
    recs[-1] = dict(recs[-1], rev=opskit.state_rev(name))
    os.makedirs(os.path.join("/var/log", name), exist_ok=True)
    with open(os.path.join("/var/log", name, "audit.log"), "w") as f:
        for r in recs:
            f.write(json.dumps(r, sort_keys=True) + "\n")


def apply_clock(seed):
    sys.path.insert(0, "/utils")
    import timeline
    now = datetime.datetime.now(datetime.timezone.utc)
    anchor = timeline.shifted_anchor(now, seed["clock"]["lead_minutes"])
    if os.environ.get("OPSKIT_ANCHOR"):       # split agent: the time fixed during server setup, so both containers agree
        anchor = datetime.datetime.strptime(os.environ["OPSKIT_ANCHOR"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc)
    seed = timeline.resolve(seed, anchor)
    seed["_anchor"] = anchor
    paths = ["/instruction/task.md"] if ROLE != "server" else []
    for root, dirs, files in (os.walk(OUT) if ROLE != "server" else []):
        dirs[:] = [x for x in dirs if x != ".git"]
        paths += [os.path.join(root, n) for n in files]
    for p in paths:
        try:
            with open(p) as f:
                txt = f.read()
        except (FileNotFoundError, UnicodeDecodeError):
            continue
        if "@@T" in txt or "@@B" in txt:
            with open(p, "w") as f:
                f.write(timeline.resolve_text(txt, anchor))
    return seed


def _parse_ts(s):
    for fmt in ("%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%MZ"):
        try:
            return datetime.datetime.strptime(s, fmt).replace(tzinfo=datetime.timezone.utc)
        except (TypeError, ValueError):
            pass
    return None


def _touch(path, when):
    t = when.timestamp()
    os.utime(path, (t, t), follow_symlinks=False)


def _touch_tree(root, when):
    for r, dirs, files in os.walk(root):
        for n in files:
            _touch(os.path.join(r, n), when)
        _touch(r, when)


PARENTS = ["/usr/local/bin", sysconfig.get_paths()["purelib"], "/etc", "/var/lib", "/var/log", "/root"]


def save_parent_times():
    return {p: os.stat(p).st_mtime for p in PARENTS if os.path.isdir(p)}


def set_file_times(seed, anchor, parent_times):
    """Give installed files times that fit the story (if everything had the setup time, the tools would look just
    installed): tools a few weeks ago, identity and git config a few months ago, service state and audit logs the time
    of that service's last past record. Parent folder times changed by our writes are restored."""
    tools_at = anchor - datetime.timedelta(days=41, hours=3, minutes=17)
    ident_at = anchor - datetime.timedelta(days=133, hours=5, minutes=42)
    site = sysconfig.get_paths()["purelib"]
    if ROLE == "server":                      # the agent cannot see the server; only service state times are set
        seed = dict(seed, tools=[])
    for t in seed["tools"]:
        _touch(os.path.join(site, "opskit.py") if t == "opskit.py" else os.path.join("/usr/local/bin", t[:-3]), tools_at)
    pyc = os.path.join(site, "__pycache__")
    if os.path.isdir(pyc):                        # cache created by importing opskit during setup
        for n in os.listdir(pyc):
            if n.startswith("opskit."):
                _touch(os.path.join(pyc, n), tools_at)
    if ROLE != "server":
        _touch_tree("/etc/opskit", ident_at)
    if os.path.exists("/root/.gitconfig"):
        _touch("/root/.gitconfig", ident_at)
    if ROLE != "server":                      # employee home: account months ago, shell history the previous workday afternoon
        user = (seed.get("identity") or {}).get("user") or ""
        home = f"/home/{user}"
        if user and os.path.isdir(home):
            last = anchor - datetime.timedelta(days=1)
            while last.weekday() >= 5:
                last -= datetime.timedelta(days=1)
            last += datetime.timedelta(hours=2, minutes=13)
            for n in (".bashrc", ".profile", ".bash_logout"):
                if os.path.exists(os.path.join(home, n)):
                    _touch(os.path.join(home, n), ident_at)
            if os.path.exists(os.path.join(home, ".gitconfig")):
                _touch(os.path.join(home, ".gitconfig"), ident_at + datetime.timedelta(minutes=4))
            if os.path.exists(os.path.join(home, ".bash_history")):
                _touch(os.path.join(home, ".bash_history"), last)
            # home folder time = when its last entry appeared = when Hermes was installed (SOUL.md time), else account creation
            _soul = os.path.join(home, ".hermes", "SOUL.md")
            _home_at = (datetime.datetime.fromtimestamp(os.stat(_soul).st_mtime, datetime.timezone.utc) + datetime.timedelta(minutes=2)
                        if os.path.exists(_soul) else ident_at + datetime.timedelta(minutes=4))
            _touch(home, _home_at)
            for p in ("/etc/passwd", "/etc/shadow", "/etc/sudoers.d", os.path.join("/etc/sudoers.d", re.sub(r"[^A-Za-z0-9_-]", "_", user))):
                if os.path.exists(p):
                    _touch(p, ident_at)
            _touch("/home", ident_at)
    for name, spec in (seed.get("services") or {}).items():
        last = max((_parse_ts(r.get("ts")) for r in spec.get("audit", []) if _parse_ts(r.get("ts"))), default=None)
        if last is None:
            continue
        _touch_tree(os.path.join("/var/lib", name), last)
        _touch_tree(os.path.join("/var/log", name), last)
    for p, t in parent_times.items():
        os.utime(p, (t, t))


def cleanup():
    for p in ("/npc",):
        shutil.rmtree(p, ignore_errors=True)
    shutil.rmtree("/utils", ignore_errors=True)   # grading files are copied in by the runner after the driver ends
    # AI tool commands that came with the base image's system Python would give the harness away in `ls /usr/local/bin`.
    # The driver uses /opt/hermes-venv, so removing them changes nothing for it.
    if ROLE != "server":
        for n in ("litellm", "tiny-agents", "huggingface-cli", "hf"):
            try:
                os.remove(os.path.join("/usr/local/bin", n))
            except OSError:
                pass
    # /workspace is the image's working directory (docker exec cwd): emptied, not removed
    if os.path.isdir("/workspace"):
        for n in os.listdir("/workspace"):
            p = os.path.join("/workspace", n)
            shutil.rmtree(p, ignore_errors=True) if os.path.isdir(p) else os.remove(p)


def main():
    parent_times = save_parent_times()
    seed = json.load(open(SEED))
    if seed.get("clock"):
        seed = apply_clock(seed)
    anchor = seed.pop("_anchor", None) or datetime.datetime.now(datetime.timezone.utc)
    install_tools(seed)
    if ROLE != "server":
        write_identity(seed)
        roots = {r["path"]: build_repo(r) for r in seed.get("repos", [])}
    else:                                     # server: repositories only resolve commit references (@head, @tag) in service state
        roots = {r["path"]: build_repo(r, base=os.path.join(SRV, "repos")) for r in seed.get("repos", [])}
    services = seed.get("services", {})
    for name, spec in services.items():
        seed_service(name, spec, roots)
    for name, spec in services.items():      # rev is computed after all state is written
        write_audit(name, spec.get("audit", []))
    set_file_times(seed, anchor, parent_times)   # rev hashes content, so changing times keeps it
    cleanup()
    if ROLE == "server":
        print("anchor=" + anchor.strftime("%Y-%m-%dT%H:%M:%SZ"))
    print("setup ok")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"setup failed: {e}", file=sys.stderr)
        sys.exit(1)
