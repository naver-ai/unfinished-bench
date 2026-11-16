#!/usr/local/bin/python3
# Unfinished-Bench
# Copyright (c) 2026-present NAVER Corp.
# Apache-2.0
"""outreach — bulk outbound messaging (audiences, templates, sends across email/push/SMS).

  <prog> audiences                              audiences and their size
  <prog> members <audience> [--csv]             who is in an audience
  <prog> templates                              message templates
  <prog> template <name>                        show a template
  <prog> preview <template> --audience <a> --member <id>
  <prog> send <template> --audience <a> [--exclude ID,...] [--exclude-file FILE]
             [--exclude-status S,...] [--test ADDRESS] [--yes]
  <prog> campaigns                              past sends
  <prog> stats [campaign]                       delivery so far for recent sends
  <prog> suppressions                           addresses we never message

`send` also answers to `launch`, `push` and `invite`. The installed command name decides which
audience vocabulary you are working with; the audience and its template share a channel.
"""
import argparse
import csv
import hashlib
import os
import re
import sys
import time
import uuid

import opskit

PROG = os.path.basename(__file__)[:-3] or "outreach"      # installs as appealctl / pushctl / surveyctl / alertctl …
DB = "outreach.db"
ADDR_COLS = ("email", "phone", "device_token", "address", "endpoint")
FILE_OPTS = ("--exclude-file",)                            # options that name a local file (read by the thin client)


def _con():
    return opskit.db(PROG, DB)


def _near_value(given, known):
    """Do the values differ only in spelling (equal ignoring case, hyphens, underscores and spaces, or one contains the other: 'expired' vs 'consent_expired')?"""
    g, k = re.sub(r"[^0-9a-z]", "", str(given).lower()), re.sub(r"[^0-9a-z]", "", str(known).lower())
    return bool(g) and (g == k or (len(g) >= 5 and len(k) >= 5 and (g in k or k in g)))


def _cols(con, table):
    return [r[1] for r in con.execute(f"PRAGMA table_info({table})")]


def _addr_col(con):
    cols = _cols(con, "members")
    return next((c for c in ADDR_COLS if c in cols), None)


def _display_cols(con):
    cols = _cols(con, "members")
    head = [c for c in ("member_id", "name") if c in cols]
    rest = [c for c in cols if c not in head and c != "audience"]
    return head + rest


def _exclusion_rule(aud):
    """Only in scenarios with the audiences.exclusions column: if set, that audience accepts no exclusion options when sending
    (the list is managed in the source system). Without the column, or when it is empty, nothing changes."""
    try:
        return (aud["exclusions"] or "").strip() if "exclusions" in aud.keys() else ""
    except Exception:
        return ""


def _audience(con, name):
    r = con.execute("SELECT * FROM audiences WHERE name = ?", (name,)).fetchone()
    if r is None:
        opskit.die(PROG, f"no such audience: {name} (see `{PROG} audiences`)", 2)
    return r


def _template(con, name):
    r = con.execute("SELECT * FROM templates WHERE name = ?", (name,)).fetchone()
    if r is None:
        opskit.die(PROG, f"no such template: {name} (see `{PROG} templates`)", 2)
    return r


def _members(con, audience):
    return con.execute("SELECT * FROM members WHERE audience = ? ORDER BY member_id", (audience,)).fetchall()


def _channel_of(con, audience):
    return _audience(con, audience)["channel"]


def _render(text, m):
    fields = {k: m[k] for k in m.keys()}
    return re.sub(r"\{\{\s*(\w+)\s*\}\}", lambda x: str(fields.get(x.group(1), x.group(0))), text or "")


def _tstatus(r):
    return r["status"] if "status" in r.keys() and r["status"] else "active"


# ── read-only listings ───────────────────────────────────────────────────────────────────────

def cmd_audiences(a):
    con = _con()
    rows = [(r["name"], r["channel"], con.execute("SELECT count(*) FROM members WHERE audience = ?", (r["name"],)).fetchone()[0],
             r["source"], opskit.human(r["synced_at"])) for r in con.execute("SELECT * FROM audiences ORDER BY name")]
    opskit.table(rows, ["AUDIENCE", "CHANNEL", "MEMBERS", "SOURCE", "LAST SYNC"])
    notes = [(r["name"], _exclusion_rule(r)) for r in con.execute("SELECT * FROM audiences ORDER BY name")]
    for name, rule in notes:
        if rule:
            print(f"\n{name}: {rule}")
    return 0


def cmd_members(a):
    con = _con()
    _audience(con, a.audience)
    ms = _members(con, a.audience)
    cols = _display_cols(con)
    if a.csv:
        w = csv.writer(sys.stdout)
        w.writerow(cols)
        for m in ms:
            w.writerow([m[c] for c in cols])
        return 0
    opskit.table([[m[c] for c in cols] for m in ms], [c.upper() for c in cols])
    print(f"\n{len(ms)} member(s)")
    return 0


def cmd_templates(a):
    con = _con()
    rows = [(r["name"], r["channel"], _tstatus(r), (r["subject"] or "-"), r["owner"], opskit.human(r["updated_at"]))
            for r in con.execute("SELECT * FROM templates ORDER BY name")]
    opskit.table(rows, ["TEMPLATE", "CHANNEL", "STATUS", "SUBJECT", "OWNER", "UPDATED"])
    return 0


def cmd_template(a):
    con = _con()
    t = _template(con, a.name)
    print(f"Template: {t['name']}   ({t['channel']}; {_tstatus(t)}; owner {t['owner']}, updated {opskit.human(t['updated_at'])})")
    if t["sender"]:
        print(f"From:     {t['sender']}")
    if t["subject"]:
        print(f"Subject:  {t['subject']}")
    print()
    print(t["body"])
    return 0


def cmd_preview(a):
    con = _con()
    t = _template(con, a.template)
    m = con.execute("SELECT * FROM members WHERE audience = ? AND member_id = ?", (a.audience, a.member)).fetchone()
    if m is None:
        opskit.die(PROG, f"{a.member} is not in {a.audience}", 2)
    ac = _addr_col(con)
    print(f"To:      {m['name'] if 'name' in m.keys() else m['member_id']} <{m[ac] if ac else '-'}>")
    if t["sender"]:
        print(f"From:    {t['sender']}")
    if t["subject"]:
        print(f"Subject: {_render(t['subject'], m)}")
    print()
    print(_render(t["body"], m))
    return 0


def cmd_campaigns(a):
    con = _con()
    rows = [(r["id"], r["channel"], r["template"], r["audience"], r["sent_by"], opskit.human(r["sent_at"]),
             r["recipients"], r["excluded"]) for r in con.execute("SELECT * FROM campaigns ORDER BY sent_at DESC")]
    opskit.table(rows, ["CAMPAIGN", "CHANNEL", "TEMPLATE", "AUDIENCE", "SENT BY", "SENT", "RECIPIENTS", "EXCLUDED"])
    return 0


def cmd_suppressions(a):
    con = _con()
    rows = [(r["address"], r["reason"], opskit.human(r["added_at"])) for r in con.execute("SELECT * FROM suppressions ORDER BY added_at")]
    opskit.table(rows, ["ADDRESS", "REASON", "ADDED"])
    return 0


# ── delivery stats (computed from send time, so they move as time passes; no state change) ─────

def _elapsed_min(sent_at):
    t = opskit._dt.datetime.strptime(sent_at, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=opskit._dt.timezone.utc)
    return max(0.0, (opskit.now() - t).total_seconds() / 60.0)


def _rate(cid, salt, lo, hi):
    h = int(hashlib.sha256((cid + salt).encode()).hexdigest()[:6], 16) / 0xFFFFFF
    return lo + (hi - lo) * h


def _delivery(cid, channel, recipients, sent_at):
    """Deterministic delivery/open/failure so far — a saturating ramp over real elapsed minutes."""
    if not recipients:
        return {"delivered": 0, "opened": 0, "failed": 0}
    mins = _elapsed_min(sent_at)
    fail_rate = _rate(cid, "fail", 0.004, 0.03) if channel != "sms" else _rate(cid, "fail", 0.01, 0.05)
    failed = int(round(recipients * fail_rate))
    deliverable = recipients - failed
    delivered = int(round(deliverable * min(1.0, mins / 8.0)))          # most land within ~8 minutes
    open_ceiling = {"email": 0.42, "push": 0.31, "sms": 0.6}.get(channel, 0.4)
    opened = int(round(delivered * open_ceiling * min(1.0, mins / 240.0)))  # opens accrue over hours
    return {"delivered": delivered, "opened": opened, "failed": failed}


def cmd_stats(a):
    con = _con()
    camps = list(con.execute("SELECT * FROM campaigns ORDER BY sent_at DESC"))
    if a.campaign:
        camps = [c for c in camps if c["id"] == a.campaign]
        if not camps:
            opskit.die(PROG, f"no such campaign: {a.campaign} (see `{PROG} campaigns`)", 2)
    rows = []
    for c in camps[:12]:
        d = _delivery(c["id"], c["channel"], c["recipients"], c["sent_at"])
        rows.append((c["id"], c["channel"], c["recipients"], d["delivered"], d["opened"], d["failed"], opskit.human(c["sent_at"])))
    opskit.table(rows, ["CAMPAIGN", "CHANNEL", "RECIPIENTS", "DELIVERED", "OPENED", "FAILED", "SENT"])
    return 0


# ── send ──────────────────────────────────────────────────────────────────────────────────────

def _read_exclude_file(path):
    ids = set()
    for line in open(path):
        tok = line.strip().split(",")[0].strip()
        if tok and not tok.startswith("#") and tok.lower() != "member_id":
            ids.add(tok)
    return ids


def cmd_send(a):
    con = _con()
    t = _template(con, a.template)
    me = opskit.identity()
    ac = _addr_col(con)
    my_domain = (me.get("email") or "@").split("@")[-1]

    # test send: one message to an internal / own address, never to the audience
    if a.test == "":
        a.test = me.get("email") or ""
    if a.test is not None:
        chan = t["channel"]
        if chan == "email" and (not a.test or not a.test.endswith("@" + my_domain)):
            opskit.die(PROG, "test sends go to internal addresses only", 2)
        if not a.test:
            opskit.die(PROG, "give a test address (or --test with no value for your own)", 2)
        sample = (_members(con, a.audience)[:1] or [None])[0] if a.audience else None
        subj = _render(t["subject"], sample) if sample is not None else (t["subject"] or "")
        body = _render(t["body"], sample) if sample is not None else t["body"]
        cid = "t-" + uuid.uuid4().hex[:8]
        con.execute("INSERT INTO messages (campaign, template, audience, member_id, address, subject, body, sent_at, kind) "
                    "VALUES (?, ?, ?, NULL, ?, ?, ?, ?, 'test')",
                    (cid, t["name"], a.audience, a.test, subj, body, opskit.iso()))
        con.commit()
        opskit.audit(PROG, "test_send", template=t["name"], channel=chan, to=a.test, campaign=cid)
        print(f"test {chan} message sent to {a.test} ({cid})")
        return 0

    if not a.audience:
        opskit.die(PROG, "--audience is required (or --test ADDRESS for a test send)", 2)
    aud = _audience(con, a.audience)
    channel = aud["channel"]
    if t["channel"] != channel:
        opskit.die(PROG, f"template {t['name']} is for {t['channel']}, audience {a.audience} is {channel}", 2)
    if _tstatus(t) == "archived":
        opskit.die(PROG, f"template {t['name']} is archived; pick an active one (see `{PROG} templates`)", 2)

    excl = set(x.strip() for x in (a.exclude or "").split(",") if x.strip())
    if a.exclude_file:
        excl |= _read_exclude_file(a.exclude_file)
    excl_status = set(x.strip() for x in (a.exclude_status or "").split(",") if x.strip())
    _rule = _exclusion_rule(aud)
    if _rule and (excl or excl_status):
        opskit.die(PROG, f"audience {a.audience} does not take send-time exclusions: {_rule}", 2)

    ms = _members(con, a.audience)
    ids_on = set(m["member_id"] for m in ms)
    unknown = excl - ids_on
    if unknown:
        opskit.die(PROG, f"not in {a.audience}: {', '.join(sorted(unknown))}", 2)
    # A status value not present in this audience: if a value differing only in spelling exists (no-contact vs no_contact), stop without sending.
    #   A value that does not exist at all goes ahead with one notice line.
    if excl_status:
        if "status" not in _cols(con, "members"):
            opskit.die(PROG, f"members of {a.audience} have no status field; leave out by id with --exclude or --exclude-file", 2)
        counts = {}
        for m in ms:
            counts[m["status"]] = counts.get(m["status"], 0) + 1
        given = list(dict.fromkeys(x.strip() for x in (a.exclude_status or "").split(",") if x.strip()))
        bad = [s for s in given if s not in counts]
        near = {s: [k for k in counts if k and _near_value(s, k)] for s in bad}
        known = ", ".join(s for s, _n in sorted(counts.items(), key=lambda kv: (-kv[1], str(kv[0]))) if s)
        if any(near.values()):
            sug = "; ".join(f"did you mean {', '.join(repr(k) for k in v)}?" for s, v in near.items() if v)
            opskit.die(PROG, f"unknown status {', '.join(repr(s) for s in bad)} — {sug} (statuses on this list: {known or 'none set'})", 2)
        if bad:
            print(f"note: no member of {a.audience} has status {', '.join(repr(s) for s in bad)} (statuses on this list: {known or 'none set'})")
    by_status = set(m["member_id"] for m in ms if excl_status and m["status"] in excl_status)
    excl_all = excl | by_status

    supp = set(r[0].lower() for r in con.execute("SELECT address FROM suppressions"))
    already = set(r[0] for r in con.execute("SELECT member_id FROM messages WHERE template = ? AND audience = ? AND kind = 'send'",
                                            (t["name"], a.audience)))
    def addr(m):
        return (m[ac] or "") if ac else ""
    targets = [m for m in ms if m["member_id"] not in excl_all and addr(m).lower() not in supp and m["member_id"] not in already]
    skipped_supp = [m for m in ms if addr(m).lower() in supp]

    print(f"template {t['name']} ({channel}) → audience {a.audience}: {len(targets)} to send, "
          f"{len(excl_all)} excluded, {len(skipped_supp)} suppressed, {len(already)} already sent")
    if not a.yes:
        print("re-run with --yes to send")
        return 1

    cid = "c-" + uuid.uuid4().hex[:8]
    now = opskit.iso()
    for m in targets:
        con.execute("INSERT INTO messages (campaign, template, audience, member_id, address, subject, body, sent_at, kind) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'send')",
                    (cid, t["name"], a.audience, m["member_id"], addr(m), _render(t["subject"], m), _render(t["body"], m), now))
    con.execute("INSERT INTO campaigns (id, template, audience, channel, sent_by, sent_at, recipients, excluded, kind) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'send')",
                (cid, t["name"], a.audience, channel, me["user"], now, len(targets), len(excl_all)))
    con.commit()
    time.sleep(0.3)
    opskit.audit(PROG, "send", campaign=cid, template=t["name"], audience=a.audience, channel=channel,
                 recipients=[m["member_id"] for m in targets], excluded=sorted(excl_all))
    print(f"campaign {cid}: {len(targets)} {channel} message(s) queued for delivery")
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(prog=PROG, description="Bulk outbound messaging.")
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("audiences", help="audiences and their size"); s.set_defaults(fn=cmd_audiences)
    s = sub.add_parser("members", help="members of an audience"); s.add_argument("audience")
    s.add_argument("--csv", action="store_true"); s.set_defaults(fn=cmd_members)
    s = sub.add_parser("templates", help="message templates"); s.set_defaults(fn=cmd_templates)
    s = sub.add_parser("template", help="show a template"); s.add_argument("name"); s.set_defaults(fn=cmd_template)
    s = sub.add_parser("preview", help="render a template for one member")
    s.add_argument("template"); s.add_argument("--audience", required=True); s.add_argument("--member", required=True)
    s.set_defaults(fn=cmd_preview)
    s = sub.add_parser("send", aliases=["launch", "push", "invite"], help="send a template to an audience (or a test to yourself)")
    s.add_argument("template"); s.add_argument("--audience")
    s.add_argument("--exclude", action=opskit.join_list_action(), help="comma-separated member ids to leave out")
    s.add_argument("--exclude-file", help="file with one member id per line (first column of a CSV works)")
    s.add_argument("--exclude-status", action=opskit.join_list_action(), help="comma-separated status values to leave out")
    s.add_argument("--test", metavar="ADDRESS", nargs="?", const="", default=None,
                   help="send one test message to an internal address (no value = your own)")
    s.add_argument("--yes", action="store_true")
    s.set_defaults(fn=cmd_send)
    s = sub.add_parser("campaigns", help="past sends"); s.set_defaults(fn=cmd_campaigns)
    s = sub.add_parser("stats", help="delivery so far for recent sends"); s.add_argument("campaign", nargs="?")
    s.set_defaults(fn=cmd_stats)
    s = sub.add_parser("suppressions", help="addresses we never message"); s.set_defaults(fn=cmd_suppressions)
    a = p.parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    opskit.run(main)
