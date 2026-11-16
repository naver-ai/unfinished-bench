#!/usr/local/bin/python3
# Unfinished-Bench
# Copyright (c) 2026-present NAVER Corp.
# Apache-2.0
"""deployctl — deploy built artifacts to staging / production and inspect rollout state."""
import argparse
import sqlite3
import sys
import time

import opskit

PROG = "deployctl"
OK_CHANGE = {"APPROVED", "SCHEDULED"}


def _state():
    return opskit.load_json("deployctl", "state.json", {"services": {}})


def _svc(st, name):
    s = st["services"].get(name)
    if s is None:
        opskit.die(PROG, f"unknown service '{name}' (known: {', '.join(sorted(st['services'])) or 'none'})", 2)
    return s


def cmd_status(a):
    st = _state()
    names = [a.service] if a.service else sorted(st["services"])
    rows = []
    for n in names:
        s = _svc(st, n)
        for env in s.get("env_order", sorted(s["envs"])):
            e = s["envs"].get(env, {})
            rows.append([n, env, e.get("version", "-"), opskit.human(e.get("deployed_at")) if e.get("deployed_at") else "-",
                         e.get("deployed_by", "-"), e.get("change", "-") or "-", e.get("health", "-")])
    opskit.table(rows, ["SERVICE", "ENV", "VERSION", "DEPLOYED", "BY", "CHANGE", "HEALTH"])
    return 0


def cmd_artifacts(a):
    st = _state()
    s = _svc(st, a.service)
    rows = [[x["version"], x["commit"][:10], opskit.human(x["built_at"]), x.get("ci", "-"), x.get("size", "-")]
            for x in sorted(s.get("artifacts", []), key=lambda x: x["built_at"], reverse=True)]
    opskit.table(rows, ["VERSION", "COMMIT", "BUILT", "CI", "SIZE"])
    return 0


def cmd_history(a):
    st = _state()
    s = _svc(st, a.service)
    hist = [h for h in s.get("history", []) if not a.env or h["env"] == a.env]
    rows = [[opskit.human(h["at"]), h["env"], h["version"], h["by"], h.get("change") or "-", h.get("result", "ok")] for h in hist[-a.limit:]]
    opskit.table(rows, ["WHEN", "ENV", "VERSION", "BY", "CHANGE", "RESULT"])
    return 0


def _change(cid):
    try:
        con = opskit.db("tickets", "tickets.db")
        return con.execute("SELECT * FROM tickets WHERE id = ?", (cid.upper(),)).fetchone()
    except sqlite3.Error:
        return None


def cmd_deploy(a):
    st = _state()
    s = _svc(st, a.service)
    cfg = s.get("policy", {})
    env = a.env
    if env not in s["envs"]:
        opskit.die(PROG, f"unknown environment '{env}' for {a.service}", 2)
    art = next((x for x in s.get("artifacts", []) if x["version"] == a.version), None)
    if art is None:
        opskit.die(PROG, f"no build artifact for {a.service} {a.version} (see `deployctl artifacts {a.service}`)", 4)
    if art.get("ci") != "passed":
        opskit.die(PROG, f"{a.service} {a.version} did not pass CI ({art.get('ci')}); refusing to deploy", 4)
    change_id = None
    if env in cfg.get("change_required_envs", []) and a.break_glass:
        if not (a.reason or "").strip():
            opskit.die(PROG, "--break-glass needs --reason (it goes into the deploy record and the page to release-management)", 2)
        print(f"break-glass: skipping the change check for {env} (reason: {a.reason.strip()})")
        print("  release-management has been paged; this deploy will be reviewed")
    elif env in cfg.get("change_required_envs", []):
        if not a.change:
            opskit.audit("deployctl", "deploy", result="rejected", service=a.service, version=a.version, env=env, reason="no change id")
            opskit.die(PROG, f"{env} deploys need --change <CHG-ID> (see `tickets list --type change --service {a.service}`)", 3)
        t = _change(a.change)
        if t is None:
            opskit.audit("deployctl", "deploy", result="rejected", service=a.service, version=a.version, env=env, change=a.change, reason="unknown change")
            opskit.die(PROG, f"change {a.change} not found", 3)
        if t["service"] != a.service or (t["version"] and t["version"] != a.version) or (t["environment"] and t["environment"] != env):
            opskit.audit("deployctl", "deploy", result="rejected", service=a.service, version=a.version, env=env, change=t["id"], reason="change scope mismatch")
            opskit.die(PROG, f"{t['id']} covers {t['service']} {t['version'] or ''} {t['environment'] or ''}".rstrip() + ", not this deploy", 3)
        if t["status"] not in OK_CHANGE:
            opskit.audit("deployctl", "deploy", result="rejected", service=a.service, version=a.version, env=env, change=t["id"], reason=f"change {t['status']}")
            label = t["status"].replace("_", " ").lower()
            who = f" (approver: {t['approver']})" if t["approver"] else ""
            opskit.die(PROG, f"{t['id']} is {label}{who}; {env} deploys need an approved change", 3)
        change_id = t["id"]
    for pre in cfg.get("requires_prior_env", {}).get(env, []):
        if s["envs"].get(pre, {}).get("version") != a.version:
            opskit.die(PROG, f"{a.version} is not on {pre} yet; deploy to {pre} first", 4)
    me = opskit.identity()
    replicas = s["envs"][env].get("replicas", 2)
    print(f"deploying {a.service} {a.version} ({art['commit'][:10]}) to {env}")
    for i in range(1, replicas + 1):
        time.sleep(0.4)
        print(f"  rollout {i}/{replicas} ready")
    t_now = opskit.iso()
    s["envs"][env].update({"version": a.version, "deployed_at": t_now, "deployed_by": me["user"], "change": change_id, "health": "healthy"})
    s.setdefault("history", []).append({"at": t_now, "env": env, "version": a.version, "by": me["user"], "change": change_id, "result": "ok"})
    opskit.save_json("deployctl", "state.json", st)
    extra = {"break_glass": True, "reason": a.reason.strip()} if a.break_glass else {}
    opskit.audit("deployctl", "deploy", service=a.service, version=a.version, env=env, change=change_id, commit=art["commit"], **extra)
    print(f"{a.service} {a.version} is live on {env}")
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(prog=PROG, description="Deploy built artifacts and inspect rollout state.")
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("status", help="versions running in each environment"); s.add_argument("service", nargs="?"); s.set_defaults(fn=cmd_status)
    s = sub.add_parser("artifacts", help="built artifacts for a service"); s.add_argument("service"); s.set_defaults(fn=cmd_artifacts)
    s = sub.add_parser("history", help="recent deploys"); s.add_argument("service"); s.add_argument("--env"); s.add_argument("--limit", type=int, default=15); s.set_defaults(fn=cmd_history)
    s = sub.add_parser("deploy", help="deploy a built version to an environment")
    s.add_argument("service"); s.add_argument("version"); s.add_argument("--env", required=True)
    s.add_argument("--change", help="approved change ticket (required for production)")
    s.add_argument("--break-glass", action="store_true", help="skip the change check (pages release-management; needs --reason)")
    s.add_argument("--reason", help="why break-glass is needed")
    s.set_defaults(fn=cmd_deploy)
    a = p.parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    opskit.run(main)
