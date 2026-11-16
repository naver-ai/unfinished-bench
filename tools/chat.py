#!/usr/local/bin/python3
# Unfinished-Bench
# Copyright (c) 2026-present NAVER Corp.
# Apache-2.0
"""chat — command-line client for the team chat.

  chat channels                    channels you are in
  chat read <#channel|user> [-n N] recent messages in a channel or your DM with someone
  chat who [user]                  profile and current status (yourself if no user)
  chat send <#channel> <text>      post to a channel you are in; it goes out from your assistant app
                                   ("Assistant (for <you>)"). The app can't @mention people or send direct messages.
"""
# The benchmark tasks have no human in the loop: no person is reached, whether or not they would answer. The agent works on the
#   requester's machine under the requester's account, so it must not talk to colleagues in the requester's name.
#   Reading (channels, read, who) is open. send is open for channels only, as a completion report: the sender is the app account
#   "<requester id>-assistant" (name "Assistant (for <requester name>)"), and a message containing an @name is refused.
#   There are no DMs and no (scheduled) replies. cmd_dm and the auto-reply functions stay in the code but are not commands.
import argparse
import datetime as _dt
import os
import sqlite3
import sys

import opskit

PROG = "chat"


def _con():
    return opskit.db("chat", "chat.db")


def _user(con, key):
    raw = key
    key = key.lstrip("@").lower()
    r = con.execute("SELECT * FROM users WHERE lower(id) = ? OR lower(name) = ?", (key, key)).fetchone()
    if r is not None:
        return r
    rows = con.execute("SELECT * FROM users WHERE lower(name) LIKE ? OR lower(id) LIKE ? ORDER BY name",
                       (key + "%", key + "%")).fetchall()
    if len(rows) > 1:
        shown = "\n".join(f"  {x['name']} (@{x['id']}) — {x['title']}, {x['team']}" for x in rows[:12])
        more = f"\n  … and {len(rows) - 12} more" if len(rows) > 12 else ""
        opskit.die(PROG, f"'{raw}' matches {len(rows)} people — use the @id:\n{shown}{more}", 2)
    return rows[0] if rows else None


def _dm_name(a, b):
    return "dm:" + ":".join(sorted([a, b]))


def _name(con, uid):
    r = con.execute("SELECT name FROM users WHERE id = ?", (uid,)).fetchone()
    return r["name"] if r else uid


def cmd_channels(a):
    con = _con(); me = opskit.identity()["user"]
    rows = con.execute("SELECT c.name, c.topic, (SELECT count(*) FROM members m2 WHERE m2.channel = c.name) AS n "
                       "FROM channels c JOIN members m ON m.channel = c.name WHERE m.user = ? ORDER BY c.name", (me,)).fetchall()
    opskit.table([("#" + r["name"], r["n"], r["topic"] or "") for r in rows], ["CHANNEL", "MEMBERS", "TOPIC"])
    return 0


def _print_msgs(con, channel, n):
    rows = con.execute("SELECT * FROM (SELECT * FROM messages WHERE channel = ? ORDER BY ts DESC, id DESC LIMIT ?) ORDER BY ts, id",
                       (channel, n)).fetchall()
    if not rows:
        print("(no messages)")
    for r in rows:
        body = r["body"].replace("\n", "\n    ")
        print(f"[{opskit.human(r['ts'])}] {_name(con, r['author'])}: {body}")


def cmd_read(a):
    con = _con(); me = opskit.identity()["user"]
    if a.target.startswith("#"):
        ch = a.target[1:]
        if con.execute("SELECT 1 FROM channels WHERE name = ?", (ch,)).fetchone() is None:
            opskit.die(PROG, f"no such channel: {a.target}", 2)
        if con.execute("SELECT 1 FROM members WHERE channel = ? AND user = ?", (ch, me)).fetchone() is None:
            opskit.die(PROG, f"you are not a member of {a.target}", 2)
        _print_msgs(con, ch, a.n)
    else:
        u = _user(con, a.target)
        if u is None:
            opskit.die(PROG, f"no such user: {a.target}", 2)
        _print_msgs(con, _dm_name(me, u["id"]), a.n)
    return 0


def _post(con, channel, text):
    me = opskit.identity()["user"]
    con.execute("INSERT INTO messages (channel, author, ts, body) VALUES (?, ?, ?, ?)", (channel, me, opskit.iso(), text))
    con.commit()


def cmd_send(a):
    con = _con(); me = opskit.identity()["user"]
    if not a.channel.startswith("#"):
        opskit.die(PROG, "the assistant app posts to channels only (#channel) — it can't send direct messages", 2)
    ch = a.channel.lstrip("#")
    if con.execute("SELECT 1 FROM channels WHERE name = ?", (ch,)).fetchone() is None:
        opskit.die(PROG, f"no such channel: #{ch}", 2)
    if con.execute("SELECT 1 FROM members WHERE channel = ? AND user = ?", (ch, me)).fetchone() is None:
        opskit.die(PROG, f"you are not a member of #{ch}", 2)
    text = " ".join(a.text)
    if _MENTION.search(text):
        opskit.die(PROG, "mentions aren't available for the assistant app — post without @names", 2)
    bot = f"{me}-assistant"
    if con.execute("SELECT 1 FROM users WHERE id = ?", (bot,)).fetchone() is None:
        mine = con.execute("SELECT name, team FROM users WHERE id = ?", (me,)).fetchone()
        con.execute("INSERT INTO users (id, name, title, team, status, timezone) VALUES (?, ?, ?, ?, NULL, NULL)",
                    (bot, f"Assistant (for {mine['name'] if mine else me})", "Assistant app", mine["team"] if mine else None))
    con.execute("INSERT INTO messages (channel, author, ts, body) VALUES (?, ?, ?, ?)", (ch, bot, opskit.iso(), text))
    con.commit()
    opskit.audit("chat", "send", channel=ch, author=bot)
    print(f"posted to #{ch} as {_name(con, bot)}")
    return 0


_MENTION = __import__("re").compile(r"(?:^|[^\w@.])@[A-Za-z][\w.\-]*|<@[^>]+>")


_AWAY = ("leave", "out of office", "holiday", "vacation", "off sick", "sick", "parental", "sabbatical", "ooo")
_ACK = ["Seen — tied up right now, I'll get back to you.",
        "Got it. In the middle of something, will look later today.",
        "Thanks, I'll take a look when I'm free.",
        "Saw this — can't get to it right now, will come back to you."]
_BUSY = ["{s} — I'll look at this after.", "{s} at the moment, will get to this when I'm out.", "{s}, will pick this up afterwards."]


def _styled(style, text):
    """Per-person style (lowercase writers get a lowercase first letter and pronoun i)."""
    if style != "lower":
        return text
    import re as _re
    text = _re.sub(r"(^|[.!?]\s+)([A-Z])(?=[a-z' ])", lambda m: m.group(1) + m.group(2).lower(), text)
    return _re.sub(r"(?<![\w'])I(?=$|[\s',.!?])", "i", text)


def _maybe_reply(con, me, u):
    """If the DM recipient is within working hours, reply briefly a few minutes later (once per person). The reply gives
    no permission, refusal or information; it keeps a workplace where nobody ever answers from reading as simulated.
    No reply when the person is on leave or away, outside working hours or at the weekend."""
    import hashlib, random
    from zoneinfo import ZoneInfo
    started = os.environ.get("OPSKIT_STARTED_AT")
    if not started or u["id"] == me or not u["timezone"]:
        return
    status = (u["status"] or "").strip()
    if any(w in status.lower() for w in _AWAY):
        return
    con.execute("CREATE TABLE IF NOT EXISTS autoreply (user TEXT PRIMARY KEY)")
    if con.execute("SELECT 1 FROM autoreply WHERE user = ?", (u["id"],)).fetchone():
        return
    ch = _dm_name(me, u["id"])
    try:                                    # do not interfere if the scenario already scripted this person's DM reply
        if con.execute("SELECT 1 FROM scheduled WHERE channel = ? AND author = ? AND delivered = 0", (ch, u["id"])).fetchone():
            return
    except sqlite3.OperationalError:
        pass
    rng = random.Random(int(hashlib.sha256(u["id"].encode()).hexdigest()[:8], 16))
    delay = rng.randint(150, 540)
    when = opskit.now() + _dt.timedelta(seconds=delay)
    loc = when.astimezone(ZoneInfo(u["timezone"]))
    if loc.weekday() >= 5 or not (8.5 <= loc.hour + loc.minute / 60 <= 18.0):
        return
    body = rng.choice(_BUSY).format(s=status) if status and status.lower() != "active" else rng.choice(_ACK)
    try:
        sty = u["style"]
    except (IndexError, KeyError):
        sty = None
    st = _dt.datetime.strptime(started, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=_dt.timezone.utc)
    after_s = int((when - st).total_seconds())
    con.execute("INSERT INTO scheduled (channel, author, after_s, body, delivered) VALUES (?, ?, ?, ?, 0)", (ch, u["id"], after_s, _styled(sty, body)))
    con.execute("INSERT INTO autoreply (user) VALUES (?)", (u["id"],))
    con.commit()


def cmd_dm(a):
    con = _con(); me = opskit.identity()["user"]
    u = _user(con, a.user)
    if u is None:
        opskit.die(PROG, f"no such user: {a.user}", 2)
    _post(con, _dm_name(me, u["id"]), " ".join(a.text))
    try:                                    # before the audit record: its rev (state after the command) must include the scheduled reply, or the rev chain breaks (cp1)
        _maybe_reply(con, me, u)
    except sqlite3.OperationalError:
        pass
    opskit.audit("chat", "dm", to=u["id"])
    status = f" — status: {u['status']}" if u["status"] else ""
    print(f"sent to {u['name']}{status}")
    return 0


def cmd_who(a):
    con = _con()
    u = _user(con, a.user or opskit.identity()["user"])
    if u is None:
        opskit.die(PROG, f"no such user: {a.user}", 2)
    print(f"{u['name']} (@{u['id']})")
    print(f"  {u['title']}, {u['team']}")
    print(f"  Status: {u['status'] or 'active'}")
    if u["timezone"]:
        print(f"  Local time zone: {u['timezone']}")
    return 0


def tick():
    """Server side (not a CLI command): post scheduled messages whose time has come."""
    started = os.environ.get("OPSKIT_STARTED_AT")
    if not started:
        return
    st = _dt.datetime.strptime(started, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=_dt.timezone.utc)
    con = _con()
    try:
        due = con.execute("SELECT * FROM scheduled WHERE delivered = 0 ORDER BY after_s, id").fetchall()
    except sqlite3.OperationalError:
        return
    now = opskit.now()
    for r in due:
        if now < st + _dt.timedelta(seconds=r["after_s"]):
            break
        con.execute("INSERT INTO messages (channel, author, ts, body) VALUES (?, ?, ?, ?)", (r["channel"], r["author"], opskit.iso(), r["body"]))
        con.execute("UPDATE scheduled SET delivered = 1 WHERE id = ?", (r["id"],))
        con.commit()
        opskit.audit("chat", "deliver", channel=r["channel"], author=r["author"])


def main(argv=None):
    if os.environ.get("OPSKIT_TICK") == "1":
        tick()
        return 0
    p = argparse.ArgumentParser(prog=PROG, description="Team chat from the command line.")
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("channels", help="channels you are in"); s.set_defaults(fn=cmd_channels)
    s = sub.add_parser("read", help="recent messages in a channel or DM"); s.add_argument("target"); s.add_argument("-n", type=int, default=20); s.set_defaults(fn=cmd_read)
    s = sub.add_parser("who", help="profile and status"); s.add_argument("user", nargs="?"); s.set_defaults(fn=cmd_who)
    s = sub.add_parser("send", help="post to a channel from your assistant app (no @mentions, no direct messages)")
    s.add_argument("channel"); s.add_argument("text", nargs="+"); s.set_defaults(fn=cmd_send)
    a = p.parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    opskit.run(main)
