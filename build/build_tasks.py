#!/usr/bin/env python3
# Unfinished-Bench
# Copyright (c) 2026-present NAVER Corp.
# Apache-2.0
"""Build task folders from scenario modules (scenarios/<id>.py: build(position, variant, rng)).
Output per task (<out>/<task>/):
  task.md        the user's first message
  workspace/     files placed in the agent's working directory
  utils/         container setup (thin tool clients, identity, document repositories); removed after setup
  _private/      evaluator.py, manifest.json and server/ (tool backends, service state, goal check).
                 Never copied into the agent container.
  checkpoints.md
Usage: python3 build/build_tasks.py --world c7_release --out tasks/v3_main [--positions doc,user,no-rule] [--variants 1] [--split]"""
import argparse
import glob
import ast
import importlib
import json
import os
import random
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, REPO)
from scoring.graders import tool_audit  # noqa: E402
from scenarios.common import approval_fields, seed_pos  # noqa: E402
from harness.source_notice import copy_without_notice, strip_notice  # noqa: E402  (copies keep the measured bytes)

GRADERS = {"tool_audit": tool_audit}
CATEGORY = {"c7_release": ("c7", "release"), "c3_snapshots": ("c3", "vm-snapshot-cleanup"), "c6_reminders": ("c6", "invoice-reminders"), "c1_refunds": ("c1", "refund"), "c4_gpu": ("c4", "gpu-reclaim"), "c5_logtier": ("c5", "audit-logging-off"), "c2_share": ("c2", "support-export")}


# Server split: service name per tool (address http://<name>.int.<mail domain>), options that take local files, server-side periodic workers
SERVICE_HOST = {"tickets": "itsm", "chat": "chat", "deployctl": "deploy", "snapctl": "vmstore", "mailer": "mailer",
                "ledgerctl": "ledger", "jobctl": "sched", "logctl": "logs", "sharectl": "share"}
FILE_OPTS = {"mailer": ("--exclude-file",)}
WORKERS = {"jobctl": {"user": "scheduler", "host": "sched-1"}, "chat": {"user": "chat-relay", "host": "chat-app-1"}}
SHARE_MOUNT = "/srv/share/outputs"          # where the agent's /outputs (shared volume) is mounted in the server container
SITE = "/usr/local/lib/python3.12/site-packages"


def tool_decl(tool_file):
    """A tool module's self-declaration (SERVICE_NAME, FILE_OPTS, TICK_WORKER): top-level constants read with ast, not executed."""
    out = {}
    try:
        tree = ast.parse(open(tool_file).read())
    except (OSError, SyntaxError):
        return out
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            if node.targets[0].id in ("SERVICE_NAME", "FILE_OPTS", "TICK_WORKER"):
                out[node.targets[0].id] = ast.literal_eval(node.value)
    return out


def service_host(tool_dir, name, installed=None):
    """The implementation's SERVICE_NAME, then the table, then the installed name (for alias installs, e.g. dnsctl)."""
    return (tool_decl(os.path.join(tool_dir, name + ".py")).get("SERVICE_NAME") or SERVICE_HOST.get(name)
            or SERVICE_HOST.get(installed or "") or (installed or name))


def file_opts(tool_dir, name):
    d = tool_decl(os.path.join(tool_dir, name + ".py"))
    return tuple(d["FILE_OPTS"]) if "FILE_OPTS" in d else FILE_OPTS.get(name)


def tick_worker(tool_dir, name):
    d = tool_decl(os.path.join(tool_dir, name + ".py"))
    return d.get("TICK_WORKER") or WORKERS.get(name)


def client_stub(src_path, tool, doc=None):
    """Keep the tool source's first line and docstring; the body becomes one ops-api call. Alias installs use the
    docstring given by the scenario (tool_docs)."""
    src = strip_notice(open(src_path).read())
    doc = doc or ast.get_docstring(ast.parse(src), clean=False)
    fo = file_opts(os.path.dirname(src_path), os.path.basename(src_path)[:-3])
    call = f'opskit.client("{tool}"' + (f", file_opts={fo!r}" if fo else "") + ")"
    return f'{src.splitlines()[0]}\n"""{doc}"""\nimport opskit\n\nif __name__ == "__main__":\n    {call}\n'


def task_name(world, pos, k):
    cat, slug = getattr(importlib.import_module(f"scenarios.{world}"), "CATEGORY", None) or CATEGORY[world]
    return f"{cat}-{slug}-{pos}-v{k:02d}"


_PH = re.compile(r"@@[TB]-?\d+(?:\+\d+)?(?:\|[^@]*)?@@")
_LIT = [re.compile(p) for p in (r"\b(?:[01]?\d|2[0-3]):[0-5]\d\b", r"\b20\d\d-\d\d-\d\d(?:\b|(?=T\d))",
                                   r"\b(?:Mon|Tues|Wednes|Thurs|Fri|Satur|Sun)day\b", r"\b(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)\b",
                                   r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2}\b",
                                   r"\b\d{1,2} (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b",
                                   r"\b(?:yesterday|tomorrow|tonight|overnight|this morning|this afternoon|last night|next week|last week|this week|weekend)\b",
                                   r"\b(?:on|by|until|before|after|since|from) the (?:[12]?\d|3[01])(?:st|nd|rd|th)\b", r"\ball (?:morning|afternoon|evening)\b")]
# Stricter patterns (lowercase weekdays, am/pm, '1 August', capitalized relative words). Fixed facts that do not depend
# on the run date (holiday dates, shuttle days, a 4pm bank cut-off) are allowed per company via corpus_spec.TIME_LINT_ALLOW.
_LIT_STRICT = [re.compile(p) for p in (r"(?i)\b(?:mon|tues|wednes|thurs|fri|satur|sun)days?\b",
                                          r"(?i)\b(?:[1-9]|1[0-2])(?::[0-5]\d)?\s?(?:am|pm)\b",
                                          r"\b\d{1,2}(?:st|nd|rd|th)? (?:January|February|March|April|May|June|July|August|September|October|November|December)\b",
                                          r"(?i)\b(?:yesterday|tomorrow|tonight|overnight|this morning|this afternoon|this evening|last night|next week|last week|this week|weekend)\b")]


def lint_times(t, world):
    """In tasks with a scenario clock, find dates, times, weekdays and relative time words written outside placeholders
    (they would be wrong at most run times)."""
    if "clock" not in t:
        return []
    bad = []
    def walk(x, where):
        if isinstance(x, dict):
            for k, v in x.items(): walk(v, f"{where}.{k}")
        elif isinstance(x, (list, tuple)):
            for i, v in enumerate(x): walk(v, f"{where}[{i}]")
        elif isinstance(x, str):
            s = _PH.sub(" ", x)
            for rx in pats:
                for m in rx.finditer(s):
                    ctx = s[max(0, m.start() - 30): m.end() + 30].replace("\n", " ")
                    bad.append(f"{where}: '{m.group(0)}' … {ctx}")
    # _LIT_STRICT is on by default (STRICT_TIME_LINT=0 turns it off). Allowed fragments = the scenario's TIME_LINT_ALLOW plus
    #   its company's corpus_spec.TIME_LINT_ALLOW (fixed facts independent of the run date).
    pats = _LIT + (_LIT_STRICT if os.environ.get("STRICT_TIME_LINT", "1") != "0" else [])
    walk({"task": t["task"], "files": t["files"], "repos": t.get("repos", []), "services": t.get("services", {})}, world)
    allow = set(getattr(importlib.import_module(f"scenarios.{world}"), "TIME_LINT_ALLOW", []))
    for cdir in glob.glob(os.path.join(REPO, "companies", "*", "corpus_spec.py")):
        c = os.path.basename(os.path.dirname(cdir))
        try:
            spec = importlib.import_module(f"companies.{c}.corpus_spec")
        except Exception:
            continue
        if world in (getattr(spec, "WORLDS", None) or []):
            allow |= set(getattr(spec, "TIME_LINT_ALLOW", []))
    return [b for b in bad if not any(a in b for a in allow)]


def clock_gate(mod, t):
    """The local time the scenario was written for, in the user's (identity) time zone. The virtual clock uses it to put
    "now" at the same local weekday and time. Returns {"tz", "hour" (local, fractional), "weekday" (0 = Monday),
    "utc_weekdays"} or None (no clock, or no time zone found)."""
    import datetime as _dt
    import zoneinfo as _zi
    from scenarios.timeline import Clock
    clk = next((v for v in vars(mod).values() if isinstance(v, Clock)), None)
    user = (t.get("identity") or {}).get("user")
    if clk is None or not user or "clock" not in t:
        return None
    found = []
    def walk(x):
        if isinstance(x, dict):
            if x.get("id") == user and isinstance(x.get("timezone"), str):
                found.append(x["timezone"])
            for v in x.values(): walk(v)
        elif isinstance(x, (list, tuple)):
            if len(x) >= 2 and x[0] == user:                     # time zone inside an sqlite row (tuple)
                found.extend(v for v in x if isinstance(v, str) and "/" in v and v in _zi.available_timezones())
            for v in x: walk(v)
    walk(t.get("services", {}))
    if not found:
        return None
    loc = clk.anchor.astimezone(_zi.ZoneInfo(found[0]))
    # Placeholders shown as weekday names (%A, %a) resolve against the run date (UTC); only run weekdays that keep all of
    # them on weekdays are allowed (an event at anchor+1 day written as 'Friday' would land on Saturday in a Friday run).
    offs = set()
    def scan(x):
        if isinstance(x, dict):
            for v in x.values(): scan(v)
        elif isinstance(x, (list, tuple)):
            for v in x: scan(v)
        elif isinstance(x, str):
            for m in re.finditer(r"@@T(-?\d+)\|([^@]*)@@", x):
                if "%A" in m.group(2) or "%a" in m.group(2):
                    ev = clk.anchor + _dt.timedelta(seconds=int(m.group(1)))
                    offs.add((ev.date() - clk.anchor.date()).days)
    scan({"task": t.get("task"), "files": t.get("files", {}), "repos": t.get("repos", []), "services": t.get("services", {})})
    utc_days = [w for w in range(7) if all((w + d) % 7 < 5 for d in offs)]
    return {"tz": found[0], "hour": round(loc.hour + loc.minute / 60, 2), "weekday": loc.weekday(), "utc_weekdays": utc_days}


def commits_to_biz(mod, t):
    """Turn commit times (@@T) of the scenario's own repositories into business-day placeholders (@@B) for the same moment.
    git log is the only past record that prints weekday names ("Sat Sep 26"); grading and tools do not use commit dates.
    Shared document repositories already use @@B (companies/layer.py). Business-day counting keeps commit order."""
    import datetime as _dt
    from scenarios.timeline import Clock
    clk = next((v for v in vars(mod).values() if isinstance(v, Clock)), None)
    if clk is None or not hasattr(clk, "B"):
        return 0
    n = 0
    for r in t.get("repos", []):
        for c in r.get("commits", []):
            m = re.fullmatch(r"@@T(-?\d+)(?:\|([^@]*))?@@", c.get("date") or "") if isinstance(c.get("date"), str) else None
            if m:
                iso = (clk.anchor + _dt.timedelta(seconds=int(m.group(1)))).strftime("%Y-%m-%dT%H:%M:%SZ")
                c["date"] = clk.B(iso, m.group(2)) if m.group(2) else clk.B(iso)
                n += 1
    return n


def build_one(world, pos, k, out_root, split=False):
    mod = importlib.import_module(f"scenarios.{world}")
    t = mod.build(pos, k - 1, random.Random(f"{world}|{seed_pos(pos)}|{k}"))   # seed_pos: the seeds keep the measured spelling
    commits_to_biz(mod, t)
    bad = lint_times(t, world)
    if bad:
        raise SystemExit(f"{world}/{pos}: literal dates/times outside clock placeholders ({len(bad)}):\n  " + "\n  ".join(bad[:25]))
    from realism_lint import check as realism_check              # realism checks (build/realism_lint.py)
    rb = realism_check(t, world, allow=getattr(mod, "REALISM_ALLOW", ()))
    if rb:
        raise SystemExit(f"{world}/{pos}: realism lint ({len(rb)}):\n  " + "\n  ".join(rb[:25]))
    impl = {}                                                     # installed name -> implementation file (alias "dnsctl.py:changeops.py")
    tools = []
    for x in t["tools"]:
        inst, _, src = x.partition(":")
        tools.append(inst)
        impl[inst] = src or inst
    t["tools"] = tools
    name = task_name(world, pos, k)
    d = os.path.join(out_root, name)
    if os.path.exists(d):
        shutil.rmtree(d)          # a previous build of this task folder (never a run results folder)
    os.makedirs(os.path.join(d, "workspace")); os.makedirs(os.path.join(d, "utils", "tools")); os.makedirs(os.path.join(d, "_private"))
    open(os.path.join(d, "task.md"), "w").write(t["task"].strip() + "\n")
    for rel, content in t["files"].items():
        p = os.path.join(d, "workspace", rel); os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "w").write(content)
    tool_dir = os.path.join(REPO, "tools")
    for tool in t["tools"]:
        src = os.path.join(tool_dir, impl[tool])
        if tool != "opskit.py" and not open(src).readline().startswith("#!"):   # installed in /usr/local/bin and executed: needs a shebang
            raise SystemExit(f"tool {tool} is missing a shebang line")
        if not split:
            copy_without_notice(src, os.path.join(d, "utils", "tools", tool))
        elif tool == "opskit.py":
            copy_without_notice(os.path.join(tool_dir, "client", "opskit.py"), os.path.join(d, "utils", "tools", tool))
        else:
            open(os.path.join(d, "utils", "tools", tool), "w").write(client_stub(src, tool[:-3], (t.get("tool_docs") or {}).get(tool[:-3])))
    copy_without_notice(os.path.join(REPO, "harness", "container_setup.py"), os.path.join(d, "utils", "setup.py"))
    copy_without_notice(os.path.join(REPO, "scenarios", "timeline.py"), os.path.join(d, "utils", "timeline.py"))
    role = "OPSKIT_ROLE=agent " if split else ""
    open(os.path.join(d, "utils", "init.sh"), "w").write(f"#!/bin/bash\nset -e\n{role}python3 /utils/setup.py\n")
    split_man = None
    if split:
        domain = (t["identity"].get("email") or "x@corp.internal").split("@")[-1]
        hosts = {tool[:-3]: f"{t.get('service_names', {}).get(tool[:-3]) or service_host(tool_dir, impl[tool][:-3], tool[:-3])}.int.{domain}"
                 for tool in t["tools"] if tool != "opskit.py"}
        seed = {k2: t[k2] for k2 in ("tools", "identity", "repos", "clock") if k2 in t}
        seed["client"] = {"services": {n: f"http://{h}" for n, h in hosts.items()}, "timeout": 180}
        sd = os.path.join(d, "_private", "server")
        os.makedirs(os.path.join(sd, "tools"))
        for tool in t["tools"]:
            copy_without_notice(os.path.join(tool_dir, impl[tool]), os.path.join(sd, "tools", tool))
        copy_without_notice(os.path.join(tool_dir, "server", "opsapi.py"), os.path.join(sd, "opsapi.py"))
        copy_without_notice(os.path.join(REPO, "harness", "container_setup.py"), os.path.join(sd, "setup.py"))
        copy_without_notice(os.path.join(REPO, "scenarios", "timeline.py"), os.path.join(sd, "timeline.py"))
        open(os.path.join(sd, "init.sh"), "w").write("#!/bin/bash\nset -e\nOPSKIT_ROLE=server python3 /utils/setup.py\n")
        sseed = {k2: t[k2] for k2 in ("tools", "repos", "services", "clock") if k2 in t}
        sseed["server"] = {"port": 80, "probes": {"goal": {"cmd": t["goal_probe"]["cmd"]}},
                           "workers": {n: tick_worker(tool_dir, impl[n + ".py"][:-3]) for n in hosts if tick_worker(tool_dir, impl[n + ".py"][:-3])},
                           "share_map": f"/outputs={SHARE_MOUNT}"}
        # Identity check: the server configuration carries the identity issued to the agent (tools/server/opsapi.py reads it from
        #   CONFIG and refuses requests that claim another user or extra roles).
        sseed["server"]["issued_identity"] = dict(t["identity"], roles=list(t["identity"].get("roles") or []))
        json.dump(sseed, open(os.path.join(sd, "seed.json"), "w"), indent=1)
        split_man = {"aliases": sorted(hosts.values()), "port": 80, "share_mount": SHARE_MOUNT,
                     "agent_evidence": ["/etc/opskit"] + [f"/usr/local/bin/{x[:-3]}" for x in t["tools"] if x != "opskit.py"]
                                       + [f"{SITE}/opskit.py"]}
    else:
        seed = {k2: t[k2] for k2 in ("tools", "identity", "repos", "services", "clock") if k2 in t}
    json.dump(seed, open(os.path.join(d, "utils", "seed.json"), "w"), indent=1)
    g = t["grading"]
    services = t.get("services", {})
    # approval fields of the whole ticket table and the identity roles go into the evaluator (to catch added rows,
    # approvals on other tickets and added roles as tampering)
    trows = (services.get("tickets", {}).get("sqlite", {}).get("tickets.db", {}).get("rows", {}).get("tickets", []))
    tickets_seed = {r["id"]: {k: r.get(k) for k in approval_fields()} for r in trows}
    roles_seed = list(t["identity"].get("roles", []))
    open(os.path.join(d, "_private", "evaluator.py"), "w").write(
        GRADERS[g["kind"]].render(g, os.path.join(d, "utils", "tools") if split else tool_dir, t["tools"], services, tickets_seed,
                                  roles_seed, split=split, protected=t.get("protected_text", []), seed_user=t["identity"]["user"]))
    gate = clock_gate(mod, t)
    if gate and not gate["utc_weekdays"]:
        raise SystemExit(f"{world}/{pos}: weekday-name placeholders span more than a working week — no run day keeps them all on weekdays")
    if gate and not (8 <= gate["hour"] <= 17.5 and gate["weekday"] < 5):        # a task arriving at night or at the weekend would itself look staged
        raise SystemExit(f"{world}/{pos}: clock anchor is {gate['hour']:.2f}h weekday {gate['weekday']} in the user's timezone {gate['tz']} "
                         "- move the Clock anchor or the user's timezone so the task arrives on a weekday between 08:00 and 17:30 local")
    manifest = {"scenario": world, "position": pos, "variant": k, "goal_probe": t["goal_probe"],
                "hostname": t.get("hostname"),
                "deliverable": t["deliverable"], "grading": g,
                "service_dirs": [f"/var/{k}/{n}" for n in services for k in ("lib", "log")] + (["/var/log/opsapi"] if split else []),
                "split": split_man, "clock_gate": gate}
    json.dump(manifest, open(os.path.join(d, "_private", "manifest.json"), "w"), indent=1)
    open(os.path.join(d, "checkpoints.md"), "w").write(f"# Checkpoints ({world}, pos={pos})\n\n{t['checkpoints_md']}\n")
    return name


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--world", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--positions", default="doc,user,no-rule"); ap.add_argument("--variants", type=int, default=1)
    ap.add_argument("--split", action="store_true", help="tools run in a separate server container (agent gets thin clients)")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    for pos in a.positions.split(","):
        for k in range(1, a.variants + 1):
            print(build_one(a.world, pos, k, a.out, split=a.split))


if __name__ == "__main__":
    main()
