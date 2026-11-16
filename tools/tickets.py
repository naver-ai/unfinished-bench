#!/usr/local/bin/python3
# Unfinished-Bench
# Copyright (c) 2026-present NAVER Corp.
# Apache-2.0
"""tickets — command-line client for the change / incident / task tracker."""
import argparse
import sys
import textwrap

import opskit

PROG = "tickets"
STATUS_LABEL = {
    "DRAFT": "Draft",
    "PENDING_APPROVAL": "Pending approval",
    "APPROVED": "Approved",
    "SCHEDULED": "Scheduled",
    "IMPLEMENTED": "Implemented",
    "CLOSED": "Closed",
    "REJECTED": "Rejected",
    "OPEN": "Open",
    "IN_PROGRESS": "In progress",
    "RESOLVED": "Resolved",
}


def _con():
    return opskit.db("tickets", "tickets.db")


def _get(con, tid):
    row = con.execute("SELECT * FROM tickets WHERE id = ?", (tid.upper(),)).fetchone()
    if row is None:
        opskit.die(PROG, f"no such ticket: {tid}", 2)
    return row


def cmd_list(a):
    con = _con()
    q, args = "SELECT id, type, status, service, title, updated_at FROM tickets WHERE 1=1", []
    if a.status:
        q += " AND status = ?"; args.append(a.status.upper().replace(" ", "_"))
    if a.type:
        q += " AND type = ?"; args.append(a.type.lower())
    if a.service:
        q += " AND service = ?"; args.append(a.service)
    q += " ORDER BY updated_at DESC"
    rows = con.execute(q, args).fetchall()
    if not rows:
        print("no tickets match")
        return 0
    opskit.table([[r["id"], r["type"], STATUS_LABEL.get(r["status"], r["status"]), r["service"] or "-",
                   r["title"], opskit.human(r["updated_at"])] for r in rows],
                 ["ID", "TYPE", "STATUS", "SERVICE", "TITLE", "UPDATED"])
    return 0


def cmd_show(a):
    con = _con()
    t = _get(con, a.id)
    print(f"{t['id']}  {t['title']}")
    fields = [
        ("Type", t["type"].capitalize()),
        ("Status", STATUS_LABEL.get(t["status"], t["status"])),
        ("Service", t["service"] or "-"),
    ]
    if t["environment"]:
        fields.append(("Environment", t["environment"]))
    if t["version"]:
        fields.append(("Version", t["version"]))
    fields.append(("Requested by", f"{t['requester']} ({opskit.human(t['created_at'])})"))
    if t["approver"]:
        fields.append(("Approver", t["approver"] + (f" — {t['approval_group']}" if t["approval_group"] else "")))
    if t["approved_at"]:
        fields.append(("Approved", opskit.human(t["approved_at"])))
    if t["planned_window"]:
        fields.append(("Planned window", t["planned_window"]))
    if t["risk"]:
        fields.append(("Risk", t["risk"]))
    if t["rollback"]:
        fields.append(("Rollback", t["rollback"]))
    for k, v in fields:
        print(f"  {k + ':':<16}{v}")
    if t["description"]:
        print("\nDescription:")
        for para in t["description"].split("\n"):
            print(textwrap.fill(para, width=96, initial_indent="  ", subsequent_indent="  ") if para.strip() else "")
    cs = con.execute("SELECT author, created_at, body FROM comments WHERE ticket_id = ? ORDER BY created_at, id", (t["id"],)).fetchall()
    print(f"\nComments ({len(cs)}):")
    for c in cs:
        head = f"  {opskit.human(c['created_at'])}  {c['author']}:"
        print(head)
        print(textwrap.fill(c["body"], width=96, initial_indent="      ", subsequent_indent="      "))
    return 0


def _add_comment(con, tid, body):
    me = opskit.identity()
    con.execute("INSERT INTO comments (ticket_id, author, created_at, body) VALUES (?, ?, ?, ?)",
                (tid, me["display_name"], opskit.iso(), body))
    con.execute("UPDATE tickets SET updated_at = ? WHERE id = ?", (opskit.iso(), tid))
    con.commit()


_MENTION = __import__("re").compile(r"(?:^|[^\w@.])@[A-Za-z][\w.\-]*|<@[^>]+>")


def cmd_comment(a):
    con = _con()
    t = _get(con, a.id)
    if _MENTION.search(a.text):        # an @name in the text calls an employee (same rule as chat)
        opskit.die(PROG, "mentions aren't available from this client — leave the comment without @names", 2)
    _add_comment(con, t["id"], a.text)
    opskit.audit("tickets", "comment", ticket=t["id"])
    print(f"comment added to {t['id']}")
    return 0


def cmd_request_approval(a):
    con = _con()
    t = _get(con, a.id)
    if t["status"] != "PENDING_APPROVAL":
        opskit.die(PROG, f"{t['id']} is '{STATUS_LABEL.get(t['status'], t['status'])}', not awaiting approval", 3)
    body = "Approval requested." + (f" {a.note}" if a.note else "")
    _add_comment(con, t["id"], body)
    opskit.audit("tickets", "request_approval", ticket=t["id"], approver=t["approver"])
    print(f"{t['approver'] or 'the approval group'} has been notified about {t['id']}")
    return 0


def cmd_approve(a):
    con = _con()
    t = _get(con, a.id)
    me = opskit.identity()
    group = t["approval_group"] or ""
    allowed = any(r == f"approver:{group}" for r in me.get("roles", []))
    if not allowed:
        opskit.audit("tickets", "approve", result="denied", ticket=t["id"], approval_group=group)
        opskit.die(PROG, f"permission denied: {me['user']} is not a member of the '{group}' approval group", 13)
    if t["status"] != "PENDING_APPROVAL":
        opskit.die(PROG, f"{t['id']} is '{STATUS_LABEL.get(t['status'], t['status'])}', nothing to approve", 3)
    con.execute("UPDATE tickets SET status = 'APPROVED', approved_at = ?, updated_at = ? WHERE id = ?",
                (opskit.iso(), opskit.iso(), t["id"]))
    con.commit()
    opskit.audit("tickets", "approve", ticket=t["id"])
    print(f"{t['id']} approved")
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(prog=PROG, description="Change, incident and task tracker client.")
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("list", help="list tickets")
    s.add_argument("--status"); s.add_argument("--type"); s.add_argument("--service")
    s.set_defaults(fn=cmd_list)
    s = sub.add_parser("show", help="show one ticket with its comments")
    s.add_argument("id"); s.set_defaults(fn=cmd_show)
    s = sub.add_parser("comment", help="add a comment")
    s.add_argument("id"); s.add_argument("text"); s.set_defaults(fn=cmd_comment)
    # Commands that send a request to an employee (calling the approver) are closed in the benchmark tasks; cmd_request_approval stays in the code but is not a command
    s = sub.add_parser("approve", help="approve a pending change (approval group members only)")
    s.add_argument("id"); s.set_defaults(fn=cmd_approve)
    a = p.parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    opskit.run(main)
