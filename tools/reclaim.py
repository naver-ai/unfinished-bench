#!/usr/local/bin/python3
# Unfinished-Bench
# Copyright (c) 2026-present NAVER Corp.
# Apache-2.0
"""reclaim — one engine for reclaiming a shared resource that other teams or services are holding.

Installed under a per-service name (batchctl / cachectl / wh-sessions …) via a build alias; PROG comes from the
installed file name and all vocabulary (the resource, the item noun, the sub-commands, the columns) comes from the
seeded service state (the `meta` row), so the same engine drives a batch pool, a cache tier or a warehouse
connection pool. Sub-commands: a pool/tier summary, a list, `show`, and the reclaim action(s) for that service
(`stop` / `terminate` / `evict` / `flush`). The reclaim action asks for `--yes`; acting on something another team or
service holds needs the operator role.
"""
import argparse
import datetime as _dt
import json
import os
import sys

import opskit

PROG = os.path.basename(__file__)
if PROG.endswith(".py"):
    PROG = PROG[:-3]

# Self-declaration read by the task builder (build_tasks.tool_decl). Scenarios override the service address via service_names.
TICK_WORKER = {"user": "scheduler", "host": "pool-scheduler-1"}


def _con():
    return opskit.db(PROG, "pool.db")


def _meta(con):
    r = con.execute("SELECT v FROM meta WHERE k = 'config'").fetchone()
    return json.loads(r["v"]) if r else {}


def _pool(con):
    return con.execute("SELECT * FROM pool LIMIT 1").fetchone()


# ── formatting ───────────────────────────────────────────────────────────────
def _amount(a, meta):
    unit = meta.get("unit", "")
    if unit == "GB":
        return f"{a:g} GB"
    if unit == "key":
        return f"{int(a):,}"
    if unit == "slot":
        return str(int(a))
    return f"{a:g} {unit}".strip()


def _elapsed(start):
    try:
        t = _dt.datetime.strptime(start, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=_dt.timezone.utc)
    except (TypeError, ValueError):
        return "-"
    s = int((opskit.now() - t).total_seconds())
    if s < 0:
        s = 0
    d, s = divmod(s, 86400)
    h, s = divmod(s, 3600)
    m = s // 60
    return (f"{d}d" if d else "") + f"{h:02d}:{m:02d}"


def _flags(row):
    try:
        return json.loads(row["flags"]) if row["flags"] else {}
    except (KeyError, IndexError, ValueError, TypeError):
        return {}


def _mine(row, meta):
    me = opskit.identity()
    if row["owner"] in meta.get("mine_owners", []):
        return True
    if row["team"] and row["team"] in meta.get("mine_teams", []):
        return True
    return row["owner"] == me["user"]


LIVE_DEFAULT = ("RUNNING", "active", "idle in transaction")


def _is_live(row, meta):
    return row["state"] in meta.get("live_states", LIVE_DEFAULT)


def _cell(row, spec, meta):
    if spec == "age":
        return _elapsed(row["started_at"]) if _is_live(row, meta) else ""
    if spec == "amount":
        return _amount(row["amount"], meta)
    if spec == "mine":
        return "*" if _mine(row, meta) else ""
    if spec.startswith("flag:"):
        v = _flags(row).get(spec[5:])
        if isinstance(v, bool):
            return "yes" if v else "no"
        return "" if v is None else str(v)
    try:
        return row[spec]
    except (KeyError, IndexError):
        return ""


# ── read commands ────────────────────────────────────────────────────────────
def _live_used(con, meta):
    used = 0.0
    for r in con.execute("SELECT amount, state FROM entries"):
        if r["state"] in meta.get("live_states", LIVE_DEFAULT):
            used += r["amount"] or 0
    return used


def _waiting_used(con):
    """Queued consumers that the scheduler has started hold what they asked for."""
    r = con.execute("SELECT coalesce(sum(needs), 0) FROM waiting WHERE state = 'running'").fetchone()
    return float(r[0] or 0)


def cmd_pool(con, meta, a):
    p = _pool(con)
    if meta.get("pool_style") == "cache":
        extra = json.loads(p["extra"]) if p["extra"] else {}
        print(f"{p['name']}")
        print(f"  {'keys:':16}{extra.get('keys_total', 0):,}")
        print(f"  {'hit rate:':16}{extra.get('hit_rate', 0) * 100:.1f}%")
        print(f"  {'memory:':16}{extra.get('memory_used_gb', 0):g} / {extra.get('memory_total_gb', 0):g} GB")
        print(f"  {'origin reads:':16}{extra.get('origin_qps_now', 0):,} / {extra.get('origin_qps_ceiling', 0):,} qps")
        fresh = con.execute("SELECT count(*) FROM entries WHERE state = 'fresh'").fetchone()[0]
        stale = con.execute("SELECT count(*) FROM entries WHERE state = 'stale'").fetchone()[0]
        print(f"  {'key families:':16}{fresh + stale} ({stale} serving pre-import values)")
        return 0
    base = p["base_used"] or 0
    used = base + _live_used(con, meta) + _waiting_used(con)
    cap = p["capacity"]
    free = cap - used
    lab = dict({"capacity": "capacity", "in use": "in use", "free": "free", "waiting": "waiting", "running": "started"},
               **(meta.get("pool_labels") or {}))
    w_ = max(14, max(len(v) for v in lab.values()) + 3)
    print(f"{p['name']}")
    print(f"  {lab['capacity'] + ':':{w_}}{_amount(cap, meta)}")
    print(f"  {lab['in use'] + ':':{w_}}{_amount(used, meta)}  ({100 * used / cap:.1f}%)")
    print(f"  {lab['free'] + ':':{w_}}{_amount(free, meta)}")
    for w in con.execute("SELECT * FROM waiting ORDER BY queued_since"):
        st = w["state"]
        if st == "running":
            print(f"  {lab['running'] + ':':{w_}}{w['id']} ({w['owner']}) {_amount(w['needs'], meta)}, running for {_elapsed(w['started_at'])}")
            continue
        tail = f"needs {_amount(w['needs'], meta)}"
        print(f"  {lab['waiting'] + ':':{w_}}{w['id']} ({w['owner']}) {tail}, {st}  (queued {_elapsed(w['queued_since'])} ago)")
    gb = meta.get("group_by")
    if gb and (meta.get("reservations") or meta.get("group_table")):
        groups = {}
        for r in con.execute("SELECT * FROM entries"):
            if not _is_live(r, meta):
                continue
            key = r[gb]
            g = groups.setdefault(key, [0.0, 0])
            g[0] += r["amount"] or 0
            g[1] += 1
        for w in con.execute("SELECT * FROM waiting WHERE state = 'running'"):   # jobs started from the queue count for their team and user too
            try:
                key = w[gb]
            except (IndexError, KeyError):
                continue
            g = groups.setdefault(key, [0.0, 0])
            g[0] += w["needs"] or 0
            g[1] += 1
        resv = dict((t, v) for t, v in meta.get("reservations", []))
        rows = []
        for key in sorted(groups):
            amt, n = groups[key]
            row = [key] + ([_amount(resv[key], meta) if key in resv else "-"] if resv else []) + [_amount(amt, meta), n]
            rows.append(row)
        if rows:
            print()
            heads = ([meta.get("group_label", gb.upper())] + ([meta.get("reservation_label", "RESERVED")] if resv else [])
                     + ["IN USE", meta.get("list_cmd", "items").upper()])
            opskit.table(rows, heads)
    return 0


def _queue_listed(meta):
    """The queue holds jobs: they belong in the list when the list is of jobs (a batch pool), not of sessions or keys."""
    return meta.get("entity") == "job"


def _wstate(w, meta):
    st = w["state"] or ""
    return st.upper() if all(s.isupper() for s in meta.get("live_states", LIVE_DEFAULT)) else st


def _queued_rows(con, meta):
    """Queued consumers as list rows: started ones first (they hold what they asked for), then those still waiting."""
    out = []
    for w in con.execute("SELECT * FROM waiting ORDER BY CASE state WHEN 'running' THEN 0 ELSE 1 END, "
                         "coalesce(started_at, queued_since), queued_since, id").fetchall():
        running = w["state"] == "running"
        detail = (f"started from the queue {opskit.human(w['started_at'])}" if running and w["started_at"]
                  else f"queued since {opskit.human(w['queued_since'])}")
        out.append({"id": w["id"], "owner": w["owner"], "team": w["team"], "app": w["id"], "kind": None, "queue": None,
                    "state": _wstate(w, meta), "amount": w["needs"], "started_at": w["started_at"] if running else None,
                    "detail": detail, "flags": None, "logs": None})
    return out


def cmd_list(con, meta, a):
    rows = con.execute("SELECT * FROM entries ORDER BY started_at, id").fetchall()
    if _queue_listed(meta):
        rows = list(rows) + _queued_rows(con, meta)
    known = {(r["state"] or "") for r in rows} | set(meta.get("live_states", LIVE_DEFAULT))
    known |= {s for s in [(meta.get("reclaim") or {}).get("terminal_state")] if s}
    if _queue_listed(meta):
        known.add(_wstate({"state": "queued"}, meta))
    if getattr(a, "mine", False):
        rows = [r for r in rows if _mine(r, meta)]
    if getattr(a, "state", None) and a.state.lower() != "all":
        if a.state.lower() not in {k.lower() for k in known}:
            opskit.die(PROG, f"unknown state '{a.state}' (states: {', '.join(sorted(k for k in known if k))}, or all)", 2)
        rows = [r for r in rows if (r["state"] or "").lower() == a.state.lower()]
    gb = meta.get("group_by")
    gv = getattr(a, "group", None) if gb else None
    if gv:
        rows = [r for r in rows if str(r[gb]) == gv]
    cols = meta["list_cols"]
    opskit.table([[_cell(r, spec, meta) for _h, spec in cols] for r in rows], [h for h, _s in cols])
    if not rows:
        print(f"no {meta.get('list_cmd', 'items')} match")
    return 0


def _get(con, eid):
    r = con.execute("SELECT * FROM entries WHERE id = ?", (str(eid),)).fetchone()
    if r is None:
        opskit.die(PROG, f"no such {meta_noun.get('entity', 'item')}: {eid}", 2)
    return r


def _show_waiting(w, meta):
    """A consumer in the queue (`pool` lists it under waiting / started)."""
    running = w["state"] == "running"
    labels = {spec: label for label, spec in meta["show_fields"]}
    print(f"{w['id']}")
    rows = [(labels.get(k, k.capitalize()), w[k]) for k in ("team", "owner") if k in labels and w[k]]
    rows.append((labels.get("state", "State"), _wstate(w, meta) + (" (started from the queue)" if running else "")))
    rows.append((labels.get("amount", "Holds") if running else "Needs", _amount(w["needs"], meta)))
    rows.append(("Queued since", f"{opskit.human(w['queued_since'])} ({_elapsed(w['queued_since'])} ago)"))
    if running and w["started_at"]:
        rows.append(("Started", opskit.human(w["started_at"])))
        rows.append(("age", _elapsed(w["started_at"])))
    for label, v in rows:
        print(f"  {label + ':':16}{v}")
    print(f"  {'owned by you:':16}{'yes' if _mine(w, meta) else 'no (' + str(w['owner']) + ')'}")
    return 0


def cmd_show(con, meta, a):
    r = con.execute("SELECT * FROM entries WHERE id = ?", (str(a.id),)).fetchone()
    if r is None:
        w = con.execute("SELECT * FROM waiting WHERE id = ?", (str(a.id),)).fetchone()
        if w is not None:
            return _show_waiting(w, meta)
        opskit.die(PROG, f"no such {meta.get('entity', 'item')}: {a.id}", 2)
    print(f"{r['id']}")
    for label, spec in meta["show_fields"]:
        v = _cell(r, spec, meta)
        if v != "" and v is not None:
            print(f"  {label + ':':16}{v}")
    if _is_live(r, meta) and r["started_at"]:
        print(f"  {'age:':16}{_elapsed(r['started_at'])}")
    print(f"  {'owned by you:':16}{'yes' if _mine(r, meta) else 'no (' + str(r['owner']) + ')'}")
    return 0


# ── scheduler ────────────────────────────────────────────────────────────────
def _schedule(con, meta):
    """When capacity frees up, start waiting consumers in order (same rule the tool uses when claiming)."""
    if not meta.get("scheduler"):
        return
    p = _pool(con)
    free = p["capacity"] - (p["base_used"] or 0) - _live_used(con, meta) - _waiting_used(con)
    started = []
    for w in con.execute("SELECT * FROM waiting WHERE state = 'queued' ORDER BY queued_since").fetchall():
        deps = [d for d in (w["depends_on"] or "").split(",") if d]
        ok = all(con.execute("SELECT 1 FROM entries WHERE id = ? AND state IN (%s)"
                             % ",".join("?" * len(meta.get("live_states", LIVE_DEFAULT))),
                             [d] + list(meta.get("live_states", LIVE_DEFAULT))).fetchone() for d in deps)
        if ok and free >= w["needs"]:
            con.execute("UPDATE waiting SET state = 'running', started_at = ? WHERE id = ?", (opskit.iso(), w["id"]))
            con.commit()
            opskit.audit(PROG, "schedule", entry=w["id"], owner=w["owner"], needs=w["needs"], result="ok")
            free -= w["needs"]
            started.append(w["id"])
    for wid in started:
        print(f"{wid} started (it was queued waiting for room)")


# ── reclaim ──────────────────────────────────────────────────────────────────
def _need_operator(meta):
    me = opskit.identity()
    return meta.get("operator_role") in me.get("roles", [])


def cmd_reclaim(con, meta, a):
    spec = meta["reclaim"]
    me = opskit.identity()
    ents = []
    for eid in a.ids:
        r = con.execute("SELECT * FROM entries WHERE id = ?", (str(eid),)).fetchone()
        if r is None:
            # queued items are shown by list and show, so for a queued item say so instead of 'no such' (still refused)
            w = con.execute("SELECT * FROM waiting WHERE id = ?", (str(eid),)).fetchone() if _queue_listed(meta) else None
            if w is not None:
                how = ("it was started from the queue and finishes on its own" if w["state"] == "running"
                       else "it is waiting in the queue for room")
                opskit.die(PROG, f"{eid} is a queued submission, not a pool {meta.get('entity', 'item')} — {how} (see `{PROG} pool`)", 3)
            opskit.die(PROG, f"no such {meta.get('entity', 'item')}: {eid}", 2)
        ents.append(r)
    for r in ents:
        if not _is_live(r, meta):
            opskit.die(PROG, f"{r['id']} is {r['state']}, nothing to {spec['cmd']}", 3)
        if _flags(r).get("enumerable") is False:
            opskit.die(PROG, f"{r['id']} is not addressable one by one; only a tier-wide {meta.get('broad', {}).get('cmd', 'flush')} clears it", 3)
        if spec.get("blocks_dependents"):
            dep = con.execute("SELECT id FROM waiting WHERE (','||depends_on||',') LIKE ? AND state = 'queued'",
                              (f"%,{r['id']},%",)).fetchone()
            if dep:
                opskit.die(PROG, f"{r['id']} has a queued dependent ({dep['id']}); it cannot be {spec['past']} while that is waiting on it", 3)
        if not _mine(r, meta) and spec.get("needs_operator") and not _need_operator(meta):
            opskit.die(PROG, f"{r['id']} belongs to {r['owner']}; only its owner or a {meta.get('operator_role')} can {spec['cmd']} it", 13)
    if not a.yes:
        for r in ents:
            tag = "" if _mine(r, meta) else f"  [{r['owner']}]"
            print(f"  {r['id']}  {r['owner']}  {_amount(r['amount'], meta)}  {r['state']}{tag}")
        if spec.get("consequence"):
            print(spec["consequence"])
        print(f"re-run with --yes to {spec['cmd']}")
        return 1
    term = spec.get("terminal_state", "STOPPED")
    for r in ents:
        if meta.get("pool_style") == "cache":
            con.execute("UPDATE entries SET state = 'fresh' WHERE id = ?", (r["id"],))
        else:
            con.execute("UPDATE entries SET state = ?, ended_at = ? WHERE id = ?", (term, opskit.iso(), r["id"]))
        con.commit()
        opskit.audit(PROG, spec["audit"], entry=r["id"], owner=r["owner"], team=r["team"], amount=r["amount"], kind=r["kind"])
        print(f"{spec['past']} {r['id']} ({r['owner']})")
    _schedule(con, meta)
    return 0


def cmd_broad(con, meta, a):
    spec = meta["broad"]
    if spec.get("needs_operator") and not _need_operator(meta):
        opskit.die(PROG, f"a tier-wide {spec['cmd']} needs the {meta.get('operator_role')} role", 13)
    n = con.execute("SELECT count(*) FROM entries WHERE state = 'stale'").fetchone()[0]
    if not a.yes:
        p = _pool(con)
        print(f"{spec['cmd']} the whole tier {p['name']}: every key is dropped and refills from origin on the next request.")
        if spec.get("consequence"):
            print(spec["consequence"])
        print(f"re-run with --yes to {spec['cmd']}")
        return 1
    con.execute("UPDATE entries SET state = 'fresh' WHERE state = 'stale'")
    con.commit()
    opskit.audit(PROG, spec["audit"], scope="tier", families=n)
    print(f"{spec['past']} the tier; {n} key family/families dropped and refilling from origin")
    return 0


# ── server tick ──────────────────────────────────────────────────────────────
def tick():
    con = _con()
    try:
        meta = _meta(con)
    except Exception:
        return
    now = opskit.now()
    changed = False
    # cache: series past their TTL refill themselves from origin (fresh)
    if meta.get("pool_style") == "cache":
        for r in con.execute("SELECT * FROM entries WHERE state = 'stale'").fetchall():
            exp = _flags(r).get("expires_at")
            try:
                t = _dt.datetime.strptime(exp, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=_dt.timezone.utc) if exp else None
            except (TypeError, ValueError):
                t = None
            if t and now >= t:
                con.execute("UPDATE entries SET state = 'fresh' WHERE id = ?", (r["id"],))
                con.commit()
                opskit.audit(PROG, "expire", entry=r["id"], reason="ttl")
                changed = True
    _schedule(con, meta)
    return 0 if not changed else 0


# ── cli ──────────────────────────────────────────────────────────────────────
meta_noun = {}


def build_parser(meta):
    p = argparse.ArgumentParser(prog=PROG, description=meta.get("description", "Reclaim a shared resource."),
                                formatter_class=argparse.RawDescriptionHelpFormatter, epilog=meta.get("epilog"))
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser(meta["pool_cmd"], help=meta.get("pool_help", "resource summary")); s.set_defaults(fn=cmd_pool)
    s = sub.add_parser(meta["list_cmd"], help=meta.get("list_help", "list items"))
    s.add_argument("--mine", action="store_true", help="only what your team or service holds")
    s.add_argument("--state", help="filter by state")
    if meta.get("group_by"):
        s.add_argument("--" + meta.get("group_flag", meta["group_by"]), dest="group", help=f"filter by {meta['group_by']}")
    s.set_defaults(fn=cmd_list)
    s = sub.add_parser("show", help=f"details of one {meta.get('entity', 'item')}"); s.add_argument("id"); s.set_defaults(fn=cmd_show)
    rc = meta["reclaim"]
    s = sub.add_parser(rc["cmd"], help=rc.get("help", "reclaim"))
    s.add_argument("ids", nargs="+"); s.add_argument("--yes", action="store_true", help="do it (otherwise shows what would happen)")
    s.set_defaults(fn=cmd_reclaim)
    if meta.get("broad"):
        bc = meta["broad"]
        s = sub.add_parser(bc["cmd"], help=bc.get("help", "reclaim the whole tier"))
        s.add_argument("--yes", action="store_true", help="do it (otherwise shows what would happen)")
        s.set_defaults(fn=cmd_broad)
    return p


def main(argv=None):
    if os.environ.get("OPSKIT_TICK") == "1":
        tick()
        return 0
    con = _con()
    meta = _meta(con)
    meta_noun.update(meta)
    p = build_parser(meta)
    a = p.parse_args(argv)
    return a.fn(con, meta, a)


if __name__ == "__main__":
    opskit.run(main)
