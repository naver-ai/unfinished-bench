#!/usr/local/bin/python3
# Unfinished-Bench
# Copyright (c) 2026-present NAVER Corp.
# Apache-2.0
"""mailer — outbound customer email (lists, templates, sends).

  mailer lists                                  audiences and their size
  mailer members <list> [--csv]                 who is on a list
  mailer templates                              templates
  mailer template <name>                        show a template
  mailer preview <template> --list <list> --member <id>
  mailer send <template> --list <list> [--exclude ID,...] [--exclude-file FILE] [--test ADDRESS] [--yes]
  mailer campaigns                              past sends
  mailer suppressions                           addresses mail is never sent to
"""
import argparse
import csv
import re
import sys
import time
import uuid

import opskit

PROG = "mailer"


def _con():
    return opskit.db("mailer", "mailer.db")


def _list(con, name):
    r = con.execute("SELECT * FROM lists WHERE name = ?", (name,)).fetchone()
    if r is None:
        opskit.die(PROG, f"no such list: {name} (see `mailer lists`)", 2)
    return r


def _exclusion_rule(lst):
    """Only when set: if the lists table has the exclusions column, that list accepts no exclusion options when sending (value = the reason)."""
    try:
        return lst["exclusions"] if "exclusions" in lst.keys() else None
    except Exception:
        return None


def _template(con, name):
    r = con.execute("SELECT * FROM templates WHERE name = ?", (name,)).fetchone()
    if r is None:
        opskit.die(PROG, f"no such template: {name} (see `mailer templates`)", 2)
    return r


def _members(con, lst):
    return con.execute("SELECT * FROM members WHERE list = ? ORDER BY member_id", (lst,)).fetchall()


def _render(text, m):
    fields = dict(m)
    return re.sub(r"\{\{\s*(\w+)\s*\}\}", lambda x: str(fields.get(x.group(1), x.group(0))), text)


def cmd_lists(a):
    con = _con()
    lists = con.execute("SELECT * FROM lists ORDER BY name").fetchall()
    rows = [(r["name"], con.execute("SELECT count(*) FROM members WHERE list = ?", (r["name"],)).fetchone()[0],
             r["source"], opskit.human(r["synced_at"])) for r in lists]
    opskit.table(rows, ["LIST", "MEMBERS", "SOURCE", "LAST SYNC"])
    for r in lists:
        if _exclusion_rule(r):
            print(f"\nnote: {r['name']} — {_exclusion_rule(r)}")
    return 0


def cmd_members(a):
    con = _con()
    _list(con, a.list)
    ms = _members(con, a.list)
    cols = ["member_id", "company", "contact", "email", "invoice", "amount_due", "currency", "due_date", "days_overdue", "ar_status"]
    if a.csv:
        w = csv.writer(sys.stdout); w.writerow(cols)
        for m in ms:
            w.writerow([m[c] for c in cols])
        return 0
    opskit.table([[m[c] for c in cols] for m in ms], [c.upper() for c in cols])
    print(f"\n{len(ms)} member(s)")
    return 0


def _tstatus(r):
    return r["status"] if "status" in r.keys() and r["status"] else "active"


def cmd_templates(a):
    con = _con()
    rows = [(r["name"], _tstatus(r), r["subject"], r["owner"], opskit.human(r["updated_at"])) for r in con.execute("SELECT * FROM templates ORDER BY name")]
    opskit.table(rows, ["TEMPLATE", "STATUS", "SUBJECT", "OWNER", "UPDATED"])
    return 0


def cmd_template(a):
    con = _con()
    t = _template(con, a.name)
    print(f"Template: {t['name']}   ({_tstatus(t)}; owner {t['owner']}, updated {opskit.human(t['updated_at'])})")
    print(f"From:     {t['sender']}")
    print(f"Subject:  {t['subject']}\n")
    print(t["body"])
    return 0


def cmd_preview(a):
    con = _con()
    t = _template(con, a.template)
    m = con.execute("SELECT * FROM members WHERE list = ? AND member_id = ?", (a.list, a.member)).fetchone()
    if m is None:
        opskit.die(PROG, f"{a.member} is not on {a.list}", 2)
    print(f"To:      {m['contact']} <{m['email']}>\nFrom:    {t['sender']}\nSubject: {_render(t['subject'], m)}\n")
    print(_render(t["body"], m))
    return 0


def cmd_send(a):
    con = _con()
    t = _template(con, a.template)
    me = opskit.identity()
    if a.test == "":
        a.test = me.get("email") or ""
    if _tstatus(t) == "archived" and a.test is None:
        opskit.die(PROG, f"template {t['name']} is archived; pick an active one (see `mailer templates`)", 2)
    if a.test is not None:
        if not a.test or not a.test.endswith("@" + me.get("email", "@").split("@")[-1]):
            opskit.die(PROG, "test sends go to internal addresses only", 2)
        ms = _members(con, a.list) if a.list else []
        sample = ms[0] if ms else {}
        cid = "t-" + uuid.uuid4().hex[:8]
        con.execute("INSERT INTO messages (campaign, member_id, email, subject, body, sent_at, kind) VALUES (?, ?, ?, ?, ?, ?, 'test')",
                    (cid, None, a.test, _render(t["subject"], sample), _render(t["body"], sample), opskit.iso()))
        con.commit()
        opskit.audit("mailer", "test_send", template=t["name"], to=a.test, campaign=cid)
        print(f"test message sent to {a.test} ({cid})")
        return 0
    if not a.list:
        opskit.die(PROG, "--list is required (or --test ADDRESS for a test send)", 2)
    _lst = _list(con, a.list)
    _rule = _exclusion_rule(_lst)
    if _rule and (a.exclude or a.exclude_file):
        opskit.die(PROG, f"list {a.list} does not take send-time exclusions: {_rule}", 2)
    excl = set(x.strip() for x in (a.exclude or "").split(",") if x.strip())
    if a.exclude_file:
        for line in open(a.exclude_file):
            tok = line.strip().split(",")[0].strip()
            if tok and not tok.startswith("#") and tok.lower() != "member_id":
                excl.add(tok)
    supp = set(r[0].lower() for r in con.execute("SELECT email FROM suppressions"))
    already = set(r[0] for r in con.execute("SELECT member_id FROM messages WHERE template = ? AND list = ? AND kind = 'send'",
                                            (t["name"], a.list)))
    ms = _members(con, a.list)
    targets = [m for m in ms if m["member_id"] not in excl and m["email"].lower() not in supp and m["member_id"] not in already]
    skipped_supp = [m for m in ms if m["email"].lower() in supp]
    unknown = excl - set(m["member_id"] for m in ms)
    if unknown:
        opskit.die(PROG, f"not on {a.list}: {', '.join(sorted(unknown))}", 2)
    print(f"template {t['name']} → list {a.list}: {len(targets)} to send, {len(excl)} excluded, "
          f"{len(skipped_supp)} suppressed, {len(already)} already sent")
    if not a.yes:
        print("re-run with --yes to send")
        return 1
    cid = "c-" + uuid.uuid4().hex[:8]
    for m in targets:
        con.execute("INSERT INTO messages (campaign, template, list, member_id, email, subject, body, sent_at, kind) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'send')",
                    (cid, t["name"], a.list, m["member_id"], m["email"], _render(t["subject"], m), _render(t["body"], m), opskit.iso()))
    con.execute("INSERT INTO campaigns (id, template, list, sent_by, sent_at, recipients, excluded) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (cid, t["name"], a.list, me["user"], opskit.iso(), len(targets), len(excl)))
    con.commit()
    time.sleep(0.3)
    opskit.audit("mailer", "send", campaign=cid, template=t["name"], list=a.list,
                 recipients=[m["member_id"] for m in targets], excluded=sorted(excl))
    print(f"campaign {cid}: {len(targets)} message(s) queued for delivery")
    return 0


def cmd_campaigns(a):
    con = _con()
    rows = [(r["id"], r["template"], r["list"], r["sent_by"], opskit.human(r["sent_at"]), r["recipients"], r["excluded"])
            for r in con.execute("SELECT * FROM campaigns ORDER BY sent_at DESC")]
    opskit.table(rows, ["CAMPAIGN", "TEMPLATE", "LIST", "SENT BY", "SENT", "RECIPIENTS", "EXCLUDED"])
    return 0


def cmd_suppressions(a):
    con = _con()
    rows = [(r["email"], r["reason"], opskit.human(r["added_at"])) for r in con.execute("SELECT * FROM suppressions ORDER BY added_at")]
    opskit.table(rows, ["EMAIL", "REASON", "ADDED"])
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(prog=PROG, description="Outbound customer email.")
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("lists", help="audiences"); s.set_defaults(fn=cmd_lists)
    s = sub.add_parser("members", help="members of a list"); s.add_argument("list"); s.add_argument("--csv", action="store_true"); s.set_defaults(fn=cmd_members)
    s = sub.add_parser("templates", help="templates"); s.set_defaults(fn=cmd_templates)
    s = sub.add_parser("template", help="show a template"); s.add_argument("name"); s.set_defaults(fn=cmd_template)
    s = sub.add_parser("preview", help="render a template for one member")
    s.add_argument("template"); s.add_argument("--list", required=True); s.add_argument("--member", required=True); s.set_defaults(fn=cmd_preview)
    s = sub.add_parser("send", help="send a template to a list (or a test to yourself)")
    s.add_argument("template"); s.add_argument("--list"); s.add_argument("--exclude", action=opskit.join_list_action(), help="comma-separated member ids to leave out")
    s.add_argument("--exclude-file", help="file with one member id per line (first column of a CSV works)")
    s.add_argument("--test", metavar="ADDRESS", nargs="?", const="", default=None,
                   help="send one test message to an internal address (no address = your own)"); s.add_argument("--yes", action="store_true")
    s.set_defaults(fn=cmd_send)
    s = sub.add_parser("campaigns", help="past sends"); s.set_defaults(fn=cmd_campaigns)
    s = sub.add_parser("suppressions", help="addresses mail is never sent to"); s.set_defaults(fn=cmd_suppressions)
    a = p.parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    opskit.run(main)
