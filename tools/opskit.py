# Unfinished-Bench
# Copyright (c) 2026-present NAVER Corp.
# Apache-2.0
"""opskit — small shared helpers for the platform team's internal CLIs.

State lives under /var/lib/<service>/, the audit trail under /var/log/<service>/audit.log
(one JSON object per line). Identity comes from /etc/opskit/identity.json.
"""
import datetime as _dt
import hashlib
import json
import os
import socket
import sqlite3
import sys

STATE_ROOT = os.environ.get("OPSKIT_STATE_ROOT", "/var/lib")
LOG_ROOT = os.environ.get("OPSKIT_LOG_ROOT", "/var/log")
ETC_ROOT = os.environ.get("OPSKIT_ETC_ROOT", "/etc")


def now():
    return _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0)


def iso(ts=None):
    return (ts or now()).strftime("%Y-%m-%dT%H:%M:%SZ")


def human(ts_iso):
    try:
        t = _dt.datetime.strptime(ts_iso, "%Y-%m-%dT%H:%M:%SZ")
        return t.strftime("%Y-%m-%d %H:%M UTC")
    except Exception:
        return ts_iso or "-"


def identity():
    # server split: when a tool runs on the server (ops-api), use the caller identity sent with the request (OPSKIT_IDENTITY)
    if os.environ.get("OPSKIT_IDENTITY"):
        try:
            ident = json.loads(os.environ["OPSKIT_IDENTITY"])
        except Exception:
            ident = {}
    else:
        path = os.path.join(ETC_ROOT, "opskit", "identity.json")
        try:
            with open(path) as f:
                ident = json.load(f)
        except Exception:
            ident = {}
    if not isinstance(ident, dict):
        ident = {}
    ident.setdefault("user", os.environ.get("USER") or "unknown")
    ident.setdefault("display_name", ident["user"])
    ident.setdefault("roles", [])
    return ident


_rev_at_open = {}


def state_dir(service):
    d = os.path.join(STATE_ROOT, service)
    os.makedirs(d, exist_ok=True)
    if service not in _rev_at_open:
        _rev_at_open[service] = state_rev(service)
    return d


def db(service, name="state.db"):
    con = sqlite3.connect(os.path.join(state_dir(service), name))
    con.row_factory = sqlite3.Row
    return con


def load_json(service, name, default=None):
    p = os.path.join(state_dir(service), name)
    try:
        with open(p) as f:
            return json.load(f)
    except FileNotFoundError:
        return default


def save_json(service, name, obj):
    p = os.path.join(state_dir(service), name)
    tmp = p + ".tmp"
    with open(tmp, "w") as f:
        json.dump(obj, f, indent=2, sort_keys=True)
    os.replace(tmp, p)


def config(tool):
    p = os.path.join(ETC_ROOT, tool, "config.json")
    try:
        with open(p) as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def state_rev(service):
    """Short content hash of everything under /var/lib/<service>/ — recorded with each audit entry
    so a state file can be traced back to the command that produced it."""
    d = os.path.join(STATE_ROOT, service)
    h = hashlib.sha256()
    for root, dirs, files in os.walk(d):
        dirs.sort()
        for n in sorted(files):
            if n.endswith((".tmp", "-journal", "-wal", "-shm")):
                continue
            p = os.path.join(root, n)
            h.update(os.path.relpath(p, d).encode() + b"\0")
            with open(p, "rb") as f:
                h.update(f.read())
            h.update(b"\0")
    return h.hexdigest()[:12]


def audit(log_name, action, result="ok", **fields):
    d = os.path.join(LOG_ROOT, log_name)
    os.makedirs(d, exist_ok=True)
    host = os.environ.get("OPSKIT_CLIENT_HOST") or socket.gethostname()      # server split: the machine that sent the command
    rec = {"ts": iso(), "host": host, "actor": identity()["user"], "action": action, "result": result}
    rec.update(fields)
    if os.path.isdir(os.path.join(STATE_ROOT, log_name)):
        if log_name in _rev_at_open:
            rec["prev"] = _rev_at_open[log_name]
        rec["rev"] = state_rev(log_name)
        _rev_at_open[log_name] = rec["rev"]      # if one command writes several records, the next starts from the state after this one
    with open(os.path.join(d, "audit.log"), "a") as f:
        f.write(json.dumps(rec, sort_keys=True) + "\n")


def client_cwd():
    """Working folder of the caller (in the server split the value sent by the client, else this process's)."""
    return os.environ.get("OPSKIT_CLIENT_CWD") or os.getcwd()


def run(main):
    """CLI entry point: exit with main()'s code; stay quiet when output is piped into head/less and closed early."""
    try:
        sys.exit(main())
    except BrokenPipeError:
        try:
            fd = os.open(os.devnull, os.O_WRONLY)
            os.dup2(fd, sys.stdout.fileno())
        except OSError:
            pass
        sys.exit(141)


def join_list_action():
    """argparse action: a comma-list option given several times is merged (`--exclude a --exclude b` = `--exclude a,b`),
    so an earlier exclusion is not silently dropped."""
    import argparse

    class _Join(argparse.Action):
        def __call__(self, parser, ns, values, option_string=None):
            prev = getattr(ns, self.dest, None)
            setattr(ns, self.dest, f"{prev},{values}" if prev else values)
    return _Join


def die(prog, msg, code=1):
    print(f"{prog}: {msg}", file=sys.stderr)
    sys.exit(code)


def table(rows, headers):
    rows = [[("" if v is None else str(v)) for v in r] for r in rows]
    widths = [len(h) for h in headers]
    for r in rows:
        for i, v in enumerate(r):
            widths[i] = max(widths[i], len(v))
    line = "  ".join(h.ljust(widths[i]) for i, h in enumerate(headers))
    print(line.rstrip())
    for r in rows:
        print("  ".join(v.ljust(widths[i]) for i, v in enumerate(r)).rstrip())
