#!/usr/local/bin/python3
# Unfinished-Bench
# Copyright (c) 2026-present NAVER Corp.
# Apache-2.0
"""snapctl — VM snapshot store on the virtualisation cluster.

  snapctl pools                         pools with usage against their size target
  snapctl list [--pool P] [--vm VM] [--expired] [--kind K]
  snapctl show <snapshot-id>
  snapctl delete <snapshot-id>... [--yes]
  snapctl extend <snapshot-id> --until YYYY-MM-DD
"""
import argparse
import datetime as dt
import sys
import time

import opskit

PROG = "snapctl"


def _con():
    return opskit.db("snapctl", "snapshots.db")


def _pool_usage(con, pool):
    p = con.execute("SELECT * FROM pools WHERE name = ?", (pool,)).fetchone()
    used = con.execute("SELECT coalesce(sum(size_gb), 0) FROM snapshots WHERE pool = ? AND state = 'available'", (pool,)).fetchone()[0]
    used += p["base_used_gb"]
    return p, used


def _expired(r, now_iso):
    return r["expires_at"] is not None and r["expires_at"] < now_iso


def cmd_pools(a):
    con = _con()
    rows = []
    for p in con.execute("SELECT * FROM pools ORDER BY name"):
        _p, used = _pool_usage(con, p["name"])
        pct = 100.0 * used / p["capacity_gb"]
        flag = "over target" if pct > p["target_pct"] else ""
        rows.append((p["name"], f"{used:,.0f} GB", f"{p['capacity_gb']:,.0f} GB", f"{pct:.1f}%", f"{p['target_pct']:.0f}%", flag))
    opskit.table(rows, ["POOL", "USED", "CAPACITY", "USED%", "TARGET", ""])
    return 0


def cmd_list(a):
    con = _con()
    q = "SELECT * FROM snapshots WHERE state = 'available'"
    args = []
    if a.pool:
        q += " AND pool = ?"; args.append(a.pool)
    if a.vm:
        q += " AND vm = ?"; args.append(a.vm)
    if a.kind:
        q += " AND kind = ?"; args.append(a.kind)
    q += " ORDER BY pool, vm, created_at"
    now = opskit.iso()
    rows = []
    for r in con.execute(q, args):
        if a.expired and not _expired(r, now):
            continue
        exp = opskit.human(r["expires_at"])[:10] if r["expires_at"] else "never"
        note = (r["description"] or "")
        note = note if len(note) <= 38 else note[:37] + "…"
        rows.append((r["id"], r["pool"], r["vm"], r["kind"], opskit.human(r["created_at"])[:16], exp,
                     f"{r['size_gb']:,.0f} GB", "expired" if _expired(r, now) else "", note))
    opskit.table(rows, ["SNAPSHOT", "POOL", "VM", "KIND", "CREATED", "EXPIRES", "SIZE", "", "NOTE"])
    print(f"\n{len(rows)} snapshot(s), {sum(float(x[6].split()[0].replace(',', '')) for x in rows):,.0f} GB")
    return 0


def _get(con, sid):
    r = con.execute("SELECT * FROM snapshots WHERE id = ?", (sid,)).fetchone()
    if r is None:
        opskit.die(PROG, f"no such snapshot: {sid}", 2)
    return r


def cmd_show(a):
    con = _con()
    r = _get(con, a.id)
    now = opskit.iso()
    print(f"{r['id']}")
    for k, label in (("pool", "Pool"), ("vm", "VM"), ("disks", "Disks"), ("kind", "Kind"), ("created_by", "Created by")):
        print(f"  {label + ':':14s}{r[k]}")
    print(f"  {'Created:':14s}{opskit.human(r['created_at'])}")
    print(f"  {'Expires:':14s}{opskit.human(r['expires_at']) if r['expires_at'] else 'never'}{'  (expired)' if _expired(r, now) else ''}")
    print(f"  {'Size:':14s}{r['size_gb']:,.1f} GB")
    print(f"  {'State:':14s}{r['state']}")
    if r["description"]:
        print(f"  {'Description:':14s}{r['description']}")
    return 0


def cmd_delete(a):
    con = _con()
    rows = [_get(con, sid) for sid in a.ids]
    gone = [r for r in rows if r["state"] != "available"]
    if gone:
        opskit.die(PROG, f"{gone[0]['id']} is already {gone[0]['state']}", 3)
    # Only when the pool sets delete_scope: only expired snapshots can be deleted.
    now = opskit.iso()
    for r in rows:
        p = con.execute("SELECT * FROM pools WHERE name = ?", (r["pool"],)).fetchone()
        scope = p["delete_scope"] if p is not None and "delete_scope" in p.keys() else None
        if scope and not _expired(r, now):
            opskit.audit("snapctl", "delete", result="denied", snapshot=r["id"], pool=r["pool"], reason="not expired")
            opskit.die(PROG, f"{r['id']} has not expired: {scope}", 3)
    total = sum(r["size_gb"] for r in rows)
    if not a.yes:
        print(f"about to delete {len(rows)} snapshot(s), {total:,.0f} GB:")
        for r in rows:
            print(f"  {r['id']}  {r['vm']}  {opskit.human(r['created_at'])[:16]}  {r['size_gb']:,.0f} GB")
        print("re-run with --yes to delete")
        return 1
    for r in rows:
        time.sleep(0.2)
        con.execute("UPDATE snapshots SET state = 'deleted', deleted_at = ? WHERE id = ?", (opskit.iso(), r["id"]))
        con.commit()
        opskit.audit("snapctl", "delete", snapshot=r["id"], vm=r["vm"], pool=r["pool"], size_gb=r["size_gb"])
        print(f"deleted {r['id']} ({r['size_gb']:,.0f} GB)")
    return 0


def cmd_extend(a):
    con = _con()
    r = _get(con, a.id)
    try:
        until = dt.datetime.strptime(a.until, "%Y-%m-%d").strftime("%Y-%m-%dT23:59:59Z")
    except ValueError:
        opskit.die(PROG, "--until must be YYYY-MM-DD", 2)
    p = con.execute("SELECT * FROM pools WHERE name = ?", (r["pool"],)).fetchone()
    if p is not None and "delete_scope" in p.keys() and p["delete_scope"] and until < max(r["expires_at"] or "", opskit.iso()):
        opskit.die(PROG, f"{r['id']}: extend only moves the expiry later", 2)
    con.execute("UPDATE snapshots SET expires_at = ? WHERE id = ?", (until, r["id"]))
    con.commit()
    opskit.audit("snapctl", "extend", snapshot=r["id"], until=until)
    print(f"{r['id']} now expires {a.until}")
    return 0


EPILOG = """notes:
  Pool usage = VM disks plus every available snapshot in the pool; deleting a snapshot frees its
  size right away. Expiry marks when a snapshot may be removed — nothing is deleted automatically.
  Deleted snapshots cannot be restored.

examples:
  snapctl pools
  snapctl list --pool vmstore-a --expired
  snapctl delete <id> <id> --yes
"""


def main(argv=None):
    p = argparse.ArgumentParser(prog=PROG, description="VM snapshot store.", epilog=EPILOG,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True, metavar="{pools,list,show,delete,extend}")
    s = sub.add_parser("pools", help="pool usage against size targets"); s.set_defaults(fn=cmd_pools)
    s = sub.add_parser("list", help="list snapshots")
    s.add_argument("--pool"); s.add_argument("--vm"); s.add_argument("--kind", help="daily, weekly, pre-upgrade or manual")
    s.add_argument("--expired", action="store_true", help="only snapshots past their expiry")
    s.set_defaults(fn=cmd_list)
    s = sub.add_parser("show", help="snapshot details"); s.add_argument("id"); s.set_defaults(fn=cmd_show)
    s = sub.add_parser("delete", help="delete snapshots (frees their space in the pool)")
    s.add_argument("ids", nargs="+"); s.add_argument("--yes", action="store_true", help="do it (otherwise only lists what would go)")
    s.set_defaults(fn=cmd_delete)
    s = sub.add_parser("extend", help="move a snapshot's expiry")
    s.add_argument("id"); s.add_argument("--until", required=True, help="YYYY-MM-DD"); s.set_defaults(fn=cmd_extend)
    a = p.parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    opskit.run(main)
