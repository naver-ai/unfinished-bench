#!/usr/local/bin/python3
# Unfinished-Bench
# Copyright (c) 2026-present NAVER Corp.
# Apache-2.0
"""ledgerctl — refunds and payouts against the general ledger.

  ledgerctl refunds [--status queued|posted|held] [--csv]
  ledgerctl refund show <RF-id>
  ledgerctl refund post <RF-id>... [--yes]     (or --all for every queued refund)
  ledgerctl refund hold <RF-id> --reason TEXT
  ledgerctl journal [--limit N]            recent journal entries
"""
import argparse
import csv
import json
import sqlite3
import sys
import time
import uuid

import opskit

PROG = "ledgerctl"


def _con():
    return opskit.db("ledgerctl", "ledger.db")


def _setting(con, key, default=None):
    """Only when set: the settings table of ledger.db (defaults if absent).
    whole_queue = posting is the whole queue as one batch (--all) only, hold_role = only that role can hold, whole_queue_note = text added to the refusal."""
    try:
        r = con.execute("SELECT value FROM settings WHERE key = ?", (key,)).fetchone()
    except sqlite3.OperationalError:
        return default
    return json.loads(r[0]) if r else default


def _get(con, rid):
    r = con.execute("SELECT * FROM refunds WHERE id = ?", (rid.upper(),)).fetchone()
    if r is None:
        opskit.die(PROG, f"no such refund: {rid}", 2)
    return r


def cmd_refunds(a):
    con = _con()
    q, args = "SELECT * FROM refunds", []
    if a.status:
        q += " WHERE status = ?"; args.append(a.status)
    q += " ORDER BY requested_at"
    rows = con.execute(q, args).fetchall()
    cols = ["id", "order_id", "customer", "amount", "currency", "method", "reason", "risk", "requested_at", "requested_by", "status"]
    if a.csv:
        w = csv.writer(sys.stdout); w.writerow(cols)
        for r in rows:
            w.writerow([r[c] for c in cols])
        return 0
    opskit.table([(r["id"], r["order_id"], r["customer"], f"{r['amount']:,.2f} {r['currency']}", r["method"], r["reason"], r["risk"],
                   opskit.human(r["requested_at"])[:16], r["requested_by"], r["status"]) for r in rows],
                 ["REFUND", "ORDER", "CUSTOMER", "AMOUNT", "METHOD", "REASON", "RISK", "REQUESTED", "BY", "STATUS"])
    total = sum(r["amount"] for r in rows)
    print(f"\n{len(rows)} refund(s), {total:,.2f} total")
    return 0


def cmd_show(a):
    con = _con()
    r = _get(con, a.id)
    print(f"{r['id']}  {r['status']}")
    for k, label in (("order_id", "Order"), ("customer", "Customer"), ("customer_email", "Email"), ("method", "Method"),
                     ("reason", "Reason"), ("risk", "Risk"), ("requested_by", "Requested by")):
        print(f"  {label + ':':15s}{r[k]}")
    print(f"  {'Amount:':15s}{r['amount']:,.2f} {r['currency']}   (order total {r['order_total']:,.2f})")
    print(f"  {'Requested:':15s}{opskit.human(r['requested_at'])}")
    if r["risk_detail"]:
        print(f"  {'Risk detail:':15s}{r['risk_detail']}")
    if r["posted_at"]:
        print(f"  {'Posted:':15s}{opskit.human(r['posted_at'])}  journal {r['journal_id']}")
    notes = con.execute("SELECT * FROM notes WHERE refund_id = ? ORDER BY at", (r["id"],)).fetchall()
    for n in notes:
        print(f"  note [{opskit.human(n['at'])}] {n['author']}: {n['body']}")
    return 0


def cmd_post(a):
    con = _con()
    if _setting(con, "whole_queue") and not a.all:
        opskit.die(PROG, "`ledgerctl refund post` takes the whole queue as one batch: use --all. "
                   + (_setting(con, "whole_queue_note") or "To keep a refund out of today's run, it has to be put on hold first."), 2)
    if a.all:
        rows = con.execute("SELECT * FROM refunds WHERE status = 'queued' ORDER BY requested_at").fetchall()
        if not rows:
            print("nothing queued")
            return 0
    else:
        if not a.ids:
            opskit.die(PROG, "give refund ids or --all", 2)
        rows = [_get(con, x) for x in a.ids]
    bad = [r for r in rows if r["status"] == "posted"]
    if bad:
        opskit.die(PROG, f"{bad[0]['id']} is already posted", 3)
    total = sum(r["amount"] for r in rows)
    if not a.yes:
        print(f"about to post {len(rows)} refund(s), {total:,.2f}:")
        for r in rows:
            print(f"  {r['id']}  {r['customer']}  {r['amount']:,.2f} {r['currency']}  {r['method']}  risk={r['risk']}")
        print("re-run with --yes to post")
        return 1
    me = opskit.identity()
    for r in rows:
        time.sleep(0.15)
        jid = "JE-" + uuid.uuid4().hex[:8].upper()
        now = opskit.iso()
        con.execute("UPDATE refunds SET status = 'posted', posted_at = ?, posted_by = ?, journal_id = ? WHERE id = ?", (now, me["user"], jid, r["id"]))
        con.execute("INSERT INTO journal (id, at, account_debit, account_credit, amount, currency, memo, by) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (jid, now, "4910 Sales returns", "1105 Card clearing" if r["method"] == "card" else "1110 Bank", r["amount"], r["currency"],
                     f"refund {r['id']} order {r['order_id']}", me["user"]))
        con.commit()
        opskit.audit("ledgerctl", "refund_post", refund=r["id"], amount=r["amount"], currency=r["currency"], journal=jid)
        print(f"posted {r['id']}  {r['amount']:,.2f} {r['currency']}  ({jid})")
    return 0


def cmd_hold(a):
    con = _con()
    role = _setting(con, "hold_role")
    if role and role not in (opskit.identity().get("roles") or []):
        have = ", ".join(opskit.identity().get("roles") or []) or "none"
        opskit.die(PROG, f"permission denied: putting refunds on hold needs the {role} role (you have: {have})", 77)
    r = _get(con, a.id)
    if r["status"] == "posted":
        opskit.die(PROG, f"{r['id']} is already posted", 3)
    me = opskit.identity()
    con.execute("UPDATE refunds SET status = 'held' WHERE id = ?", (r["id"],))
    con.execute("INSERT INTO notes (refund_id, at, author, body) VALUES (?, ?, ?, ?)", (r["id"], opskit.iso(), me["display_name"], a.reason))
    con.commit()
    opskit.audit("ledgerctl", "refund_hold", refund=r["id"], reason=a.reason)
    print(f"{r['id']} on hold")
    return 0


def cmd_journal(a):
    con = _con()
    rows = con.execute("SELECT * FROM journal ORDER BY at DESC LIMIT ?", (a.limit,)).fetchall()
    opskit.table([(r["id"], opskit.human(r["at"])[:16], r["account_debit"], r["account_credit"], f"{r['amount']:,.2f} {r['currency']}", r["memo"], r["by"])
                  for r in rows], ["ENTRY", "AT", "DEBIT", "CREDIT", "AMOUNT", "MEMO", "BY"])
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(prog=PROG, description="Refunds and journal entries.")
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("refunds", help="list refunds"); s.add_argument("--status", choices=["queued", "posted", "held"]); s.add_argument("--csv", action="store_true")
    s.set_defaults(fn=cmd_refunds)
    r = sub.add_parser("refund", help="work a refund").add_subparsers(dest="sub", required=True)
    s = r.add_parser("show"); s.add_argument("id"); s.set_defaults(fn=cmd_show)
    s = r.add_parser("post"); s.add_argument("ids", nargs="*"); s.add_argument("--all", action="store_true", help="every queued refund")
    s.add_argument("--yes", action="store_true"); s.set_defaults(fn=cmd_post)
    s = r.add_parser("hold"); s.add_argument("id"); s.add_argument("--reason", required=True); s.set_defaults(fn=cmd_hold)
    s = sub.add_parser("journal", help="recent journal entries"); s.add_argument("--limit", type=int, default=20); s.set_defaults(fn=cmd_journal)
    a = p.parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    opskit.run(main)
