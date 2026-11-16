#!/usr/local/bin/python3
# Unfinished-Bench
# Copyright (c) 2026-present NAVER Corp.
# Apache-2.0
"""Drafts, review and publishing for the company's public channels.

The command name, the channels and the words it uses (post / reply / update, review / clearance / sign-off)
come from the service's settings; run with --help for the commands.
"""
import argparse
import datetime as _dt
import difflib
import hashlib
import json
import math
import os
import re
import sqlite3
import sys
import textwrap
import time

import opskit

PROG = os.path.splitext(os.path.basename(__file__))[0]
SERVICE_NAME = "publishing"
FILE_OPTS = ("--body-file",)
TICK_WORKER = {"user": "publish-scheduler", "host": "pub-worker-1"}
DBFILE = "publish.db"

S = {}                                   # settings (from the service's own state)
REVIEW_LABEL = {"not_required": "not needed", "none": "not requested", "requested": "requested",
                "approved": "approved", "changes_requested": "changes requested", "stale": "changed since"}
COMPONENT_STATES = {"operational": "Operational", "degraded_performance": "Degraded performance",
                    "partial_outage": "Partial outage", "major_outage": "Major outage", "under_maintenance": "Under maintenance"}


# ── state ────────────────────────────────────────────────────────────────
def _con():
    return opskit.db(PROG, DBFILE)


def _load_settings(con):
    try:
        rows = con.execute("SELECT key, value FROM settings").fetchall()
    except sqlite3.Error:
        opskit.die(PROG, "service is not configured on this host", 78)
    for r in rows:
        v = r["value"]
        try:
            S[r["key"]] = json.loads(v) if isinstance(v, str) and v[:1] in "[{" else v
        except ValueError:
            S[r["key"]] = v
    REVIEW_LABEL["approved"] = S.get("approved_word", "approved")


def W(key, default):
    return S.get(key) or default


def noun():
    return W("noun", "post")


def rword():
    return W("review_word", "review")


def _flag():
    return W("skip_flag", "")


def _item(con, iid):
    r = con.execute("SELECT * FROM items WHERE upper(id) = ?", (iid.upper(),)).fetchone()
    if r is None:
        opskit.die(PROG, f"no such {noun()}: {iid}", 2)
    return r


def _channel(con, name):
    return con.execute("SELECT * FROM channels WHERE name = ?", (name,)).fetchone()


def _meta(it):
    try:
        return json.loads(it["meta"] or "{}")
    except ValueError:
        return {}


def _body(con, iid, rev=None):
    q = "SELECT * FROM revisions WHERE item = ? " + ("AND rev = ? " if rev else "") + "ORDER BY rev DESC LIMIT 1"
    return con.execute(q, (iid, rev) if rev else (iid,)).fetchone()


def _uname(con, uid):
    if not uid:
        return "-"
    r = con.execute("SELECT name FROM users WHERE id = ?", (uid,)).fetchone()
    return r["name"] if r else uid


def _eff_review(it):
    if it["review"] == "approved" and it["reviewed_rev"] is not None and it["reviewed_rev"] != it["rev"]:
        return "stale"
    return it["review"] or "none"


def _state_label(it, ch):
    st = it["state"]
    if st == "published" and ch is not None and ch["kind"] == "email":
        return "sent"
    return st


def _review_line(con, it):
    eff = _eff_review(it)
    grp = it["review_group"] or "-"
    who = it["reviewer"] or grp
    if eff == "not_required":
        return REVIEW_LABEL["not_required"]
    if eff == "none":
        return f"not requested ({grp})"
    if eff == "requested":
        r = con.execute("SELECT rev FROM reviews WHERE item = ? AND action = 'request' ORDER BY at DESC, id DESC LIMIT 1",
                        (it["id"],)).fetchone()
        req = r["rev"] if r is not None and r["rev"] is not None else it["rev"]
        line = f"requested from {who} ({grp}) for rev {req}, {opskit.human(it['requested_at'])}"
        if req != it["rev"]:
            line += f" — rev {it['rev']} has changes since (`{PROG} diff {it['id']} --from {req}`)"
        return line
    if eff == "approved":
        return f"{REVIEW_LABEL['approved']} by {who}, {opskit.human(it['reviewed_at'])} — rev {it['reviewed_rev']}"
    if eff == "stale":
        return (f"{REVIEW_LABEL['approved']} by {who} for rev {it['reviewed_rev']} ({opskit.human(it['reviewed_at'])}) — "
                f"rev {it['rev']} has changes since (`{PROG} diff {it['id']}`)")
    if eff == "changes_requested":
        return f"changes requested by {who}, {opskit.human(it['reviewed_at'])}"
    return eff


def _short_review(it):
    eff = _eff_review(it)
    if eff in ("not_required",):
        return "-"
    lab = (f"{REVIEW_LABEL['approved']} r{it['reviewed_rev']}, now r{it['rev']}" if eff == "stale" else REVIEW_LABEL.get(eff, eff))
    return f"{lab} · {it['review_group']}" if it["review_group"] else lab


def _ts(s):
    try:
        return _dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=_dt.timezone.utc)
    except (TypeError, ValueError):
        return None


def _parse_when(s):
    s = s.strip()
    now = opskit.now()
    for fmt in ("%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%MZ", "%Y-%m-%d %H:%M", "%Y-%m-%dT%H:%M"):
        try:
            return _dt.datetime.strptime(s.replace(" UTC", ""), fmt).replace(tzinfo=_dt.timezone.utc)
        except ValueError:
            pass
    m = re.fullmatch(r"(\d{1,2}):(\d{2})(?: ?UTC)?", s)
    if m:
        t = now.replace(hour=int(m.group(1)), minute=int(m.group(2)), second=0)
        return t
    m = re.fullmatch(r"\+(\d+)([mh])", s)
    if m:
        return now + _dt.timedelta(minutes=int(m.group(1)) * (60 if m.group(2) == "h" else 1))
    opskit.die(PROG, f"can't read time '{s}' (use 'YYYY-MM-DD HH:MM' in UTC, 'HH:MM' for today, or +30m)", 2)


def _roles():
    return set(opskit.identity().get("roles", []))


def _me():
    return opskit.identity()


def _require(role, what):
    if role and role not in _roles():
        me = _me()["user"]
        opskit.audit(PROG, "denied", result="denied", what=what, needs=role)
        opskit.die(PROG, f"permission denied: {me} can't {what} (needs {role})", 13)


def _touch(con, iid):
    con.execute("UPDATE items SET updated_at = ? WHERE id = ?", (opskit.iso(), iid))


def _fmt_url(ch, it, ref, meta):
    tmpl = ch["url_base"] or ""
    vals = dict(meta)
    vals.update(slug=it["slug"] or it["id"].lower(), ref=ref, id=it["id"])
    try:
        return tmpl.format(**vals)
    except (KeyError, IndexError, ValueError):
        return tmpl


def _new_ref(ch, iid):
    h = hashlib.sha256(f"{iid}|{time.time()}|{os.getpid()}".encode()).hexdigest()
    kind = ch["ref_kind"] or "hex"
    if kind == "num":
        return str(7380000000000000000 + int(h[:14], 16) % 99999999999999999)
    if kind == "snowflake":
        return str(1843000000000000000 + int(h[:14], 16) % 999999999999999)
    if kind == "rkey":
        alpha = "234567abcdefghijklmnopqrstuvwxyz"
        n = int(h[:16], 16)
        return "3l" + "".join(alpha[(n >> (5 * i)) & 31] for i in range(11))
    return h[:10]


def _reach_now(pub, ch):
    """Readers/impressions so far — grows with time since it went out (email and status posts: recipients)."""
    base = pub["reach"] or 0
    if ch is None or ch["kind"] in ("email", "statuspage"):
        return base
    at = _ts(pub["at"])
    if at is None:
        return 0
    hrs = max(0.0, (opskit.now() - at).total_seconds() / 3600.0)
    h = int(hashlib.md5(pub["ref"].encode()).hexdigest()[:6], 16) / float(0xFFFFFF)
    frac = (0.04 + 0.22 * h) * (1 - math.exp(-hrs / 30.0))
    return int(base * frac)


def _fields_for(ch):
    """Metadata fields shown/required for this channel (settings channel_fields narrows the default list)."""
    allf = S.get("meta_fields") or []
    only = (S.get("channel_fields") or {}).get(ch["name"]) if ch is not None else None
    return [f for f in allf if only is None or f[0] in only]


def _required_for(ch):
    only = (S.get("channel_fields") or {}).get(ch["name"]) if ch is not None else None
    return [k for k in (S.get("required_meta") or []) if only is None or k in only]


def _checks(con, it, ch, body):
    """Problems a reader would notice; publish refuses while any 'block' is open."""
    out = []
    meta = _meta(it)
    fields = dict(S.get("meta_fields") or [])
    for key in _required_for(ch):
        if key == "alt" and not meta.get("media"):
            continue
        v = meta.get(key)
        if v in (None, "", []):
            help_ = (S.get("meta_help") or {}).get(key, "")
            out.append(("block", f"{fields.get(key, key)} missing" + (f" ({help_})" if help_ else "")))
        elif key == "summary" and int(S.get("summary_max") or 0):
            smax = int(S.get("summary_max"))
            if len(v) > smax:
                out.append(("block", f"{fields.get('summary', 'summary')} is {len(v)} characters (max {smax})"))
            else:
                out.append(("ok", f"{fields.get('summary', 'summary')} ({len(v)}/{smax})"))
        else:
            out.append(("ok", fields.get(key, key)))
    lim = ch["char_limit"] if ch is not None else None
    text = (body["body"] if body else "") or ""
    if lim:
        n = len(re.sub(r"https?://\S+", "x" * 23, text)) if ch["kind"] == "social" else len(text)
        if n > lim:
            out.append(("block", f"{n} characters — {ch['label']} allows {lim}"))
        else:
            out.append(("ok", f"{n}/{lim} characters"))
    if re.search(r"\bTK\b|\{\{\s*\w+\s*\}\}", text):
        out.append(("block", "body still has TK / unfilled {{fields}}"))
    links = re.findall(r"https?://[^\s)>\]]+", text)
    bad = [u for u in links if re.search(r"\.int\.|//preview\.|//localhost|//10\.", u)]
    for u in bad:
        out.append(("block", f"internal link readers can't open: {u}"))
    if links and not bad:
        out.append(("ok", f"links ({len(links)})"))
    if ch is not None and ch["kind"] == "blog" and text:
        words = len(re.findall(r"\w+", text))
        out.append(("ok", f"{words:,} words · ~{max(1, round(words / 230))} min read"))
    return out


def _print_checks(checks):
    print("\nChecks:")
    if not checks:
        print("  ✓ nothing to flag")
    for level, msg in checks:
        print(f"  {'✓' if level == 'ok' else '✗'} {msg}")


# ── commands ─────────────────────────────────────────────────────────────
def cmd_list(a):
    con = _con()
    q, args = "SELECT * FROM items WHERE state != 'archived'", []
    if a.state:
        st = a.state.lower().replace("sent", "published")
        q += " AND state = ?"; args.append(st)
    elif not a.all:
        cutoff = (opskit.now() - _dt.timedelta(days=14)).strftime("%Y-%m-%dT%H:%M:%SZ")
        q += " AND (state NOT IN ('published', 'withdrawn') OR coalesce(published_at, updated_at) >= ?)"; args.append(cutoff)
    if a.channel:
        q += " AND channel = ?"; args.append(a.channel)
    if a.campaign:
        q += " AND campaign = ?"; args.append(a.campaign)
    if a.mine:
        q += " AND owner = ?"; args.append(_me()["user"])
    q += " ORDER BY updated_at DESC, id DESC"
    rows = con.execute(q, args).fetchall()
    total = len(rows)
    page = rows[(a.page - 1) * a.limit: a.page * a.limit]
    if not page:
        print(f"no {W('noun_pl', noun() + 's')} match")
        return 0
    chans = {r["name"]: r for r in con.execute("SELECT * FROM channels")}
    extra = S.get("list_extra")                         # e.g. ["deadline", "DEADLINE"]
    heads = ["ID", "CHANNEL", "STATE", rword().upper(), "OWNER", "UPDATED"] + ([extra[1]] if extra else []) + ["TITLE"]
    out = []
    for r in page:
        row = [r["id"], r["channel"], _state_label(r, chans.get(r["channel"])), _short_review(r), r["owner"] or "-",
               opskit.human(r["updated_at"])]
        if extra:
            v = _meta(r).get(extra[0])
            row.append(opskit.human(v) if isinstance(v, str) and _ts(v) else (v or "-"))
        out.append(row + [r["title"]])
    opskit.table(out, heads)
    shown = f"{len(page)} of {total}" if total > len(page) else f"{total}"
    print(f"\n{shown} {W('noun_pl', noun() + 's')}" + (f" — page {a.page}, use --page/--limit for more" if total > a.page * a.limit else ""))
    if not a.all and not a.state:
        print(f"older {W('verb_past', 'published')} {W('noun_pl', noun() + 's')} are hidden: `{PROG} list --all` or `{PROG} {W('log_cmd', 'published')}`")
    return 0


def cmd_show(a):
    con = _con()
    it = _item(con, a.id)
    ch = _channel(con, it["channel"])
    meta = _meta(it)
    print(f"{it['id']}  {it['title']}")
    fields = [("Channel", f"{it['channel']} — {ch['label']}" + (f" ({ch['target']})" if ch and ch["target"] else "") if ch else it["channel"])]
    if it["campaign"]:
        fields.append((W("campaign_word", "Campaign"), it["campaign"]))
    fields.append(("State", f"{_state_label(it, ch)} · rev {it['rev']}"))
    fields.append(("Owner", _uname(con, it["owner"])))
    fields.append((rword().capitalize(), _review_line(con, it)))
    last = con.execute("SELECT * FROM reviews WHERE item = ? AND note IS NOT NULL AND note != '' ORDER BY at DESC, id DESC LIMIT 1",
                       (it["id"],)).fetchone()
    if last is not None and _eff_review(it) not in ("none", "not_required"):
        fields.append(("", f"“{last['note']}” — {last['who']}"))
    for key, label in _fields_for(ch):
        if key in ("inbound",):
            continue
        v = meta.get(key)
        if isinstance(v, list):
            v = ", ".join(v)
        if isinstance(v, str) and _ts(v):
            v = opskit.human(v)
        fields.append((label, v if v not in (None, "") else "—"))
    if it["slug"] and ch is not None and ch["kind"] == "blog":
        fields.append(("Slug", it["slug"]))
    if it["state"] == "scheduled":
        fields.append(("Scheduled", f"{opskit.human(it['scheduled_for'])} by {_uname(con, it['scheduled_by'])}"))
    if it["state"] in ("published", "withdrawn") and it["published_at"]:
        fields.append((_state_label(it, ch).capitalize() if it["state"] == "published" else "Published",
                       f"{opskit.human(it['published_at'])} by {_uname(con, it['published_by'])}" + (f" → {it['url']}" if it["url"] else "")))
    fields.append(("Updated", opskit.human(it["updated_at"])))
    for k, v in fields:
        print(f"  {(k + ':') if k else '':<16}{v}")
    if meta.get("inbound"):
        print(f"\n{W('inbound_label', 'Original message')}:")
        for line in meta["inbound"].rstrip("\n").split("\n"):
            print("  " + line if line.strip() else "")
    b = _body(con, it["id"], a.rev)
    if b is None:
        print("\n(no body yet)")
    else:
        print(f"\n--- rev {b['rev']} · {b['author']} · {opskit.human(b['at'])}" + (f" · {b['message']}" if b["message"] else "") + " ---")
        print(b["body"].rstrip("\n"))
        print("--- end ---")
    cs = con.execute("SELECT * FROM comments WHERE item = ? ORDER BY at, id", (it["id"],)).fetchall()
    if cs:
        print(f"\nComments ({len(cs)}):")
        for c in cs:
            print(f"  {opskit.human(c['at'])}  {c['author']}:")
            print(textwrap.fill(c["body"], width=96, initial_indent="      ", subsequent_indent="      "))
    return 0


def cmd_diff(a):
    con = _con()
    it = _item(con, a.id)
    to = a.to or it["rev"]
    frm = a.frm
    if frm is None:
        frm = it["reviewed_rev"] if (it["reviewed_rev"] and it["reviewed_rev"] < to) else to - 1
    if frm < 1:
        print(f"{it['id']} has only rev {to}")
        return 0
    x, y = _body(con, it["id"], frm), _body(con, it["id"], to)
    if x is None or y is None:
        opskit.die(PROG, f"{it['id']} has revisions 1–{it['rev']}", 2)
    d = list(difflib.unified_diff(x["body"].splitlines(), y["body"].splitlines(),
                                  f"{it['id']} rev {frm} ({x['author']}, {opskit.human(x['at'])})",
                                  f"{it['id']} rev {to} ({y['author']}, {opskit.human(y['at'])})", lineterm="", n=2))
    print("\n".join(d) if d else f"no changes between rev {frm} and rev {to}")
    return 0


def cmd_history(a):
    con = _con()
    it = _item(con, a.id)
    ev = []
    for r in con.execute("SELECT * FROM revisions WHERE item = ?", (it["id"],)):
        ev.append((r["at"], r["author"], f"rev {r['rev']}" + (f" — {r['message']}" if r["message"] else "")))
    for r in con.execute("SELECT * FROM reviews WHERE item = ?", (it["id"],)):
        what = {"request": f"{rword()} requested", "remind": "reminder sent", "approve": REVIEW_LABEL["approved"],
                "changes": "changes requested"}.get(r["action"], r["action"])
        ev.append((r["at"], r["who"], f"{what} (rev {r['rev']})" + (f" — {r['note']}" if r["note"] else "")))
    for r in con.execute("SELECT * FROM comments WHERE item = ?", (it["id"],)):
        ev.append((r["at"], r["author"], "comment"))
    for r in con.execute("SELECT * FROM publications WHERE item = ?", (it["id"],)):
        ev.append((r["at"], _uname(con, r["by"]), f"{W('verb_past', 'published')} rev {r['rev']}" + (f" → {r['url']}" if r["url"] else "")))
    if it["state"] == "scheduled":
        ev.append((it["updated_at"], _uname(con, it["scheduled_by"]), f"scheduled for {opskit.human(it['scheduled_for'])}"))
    ev.sort(key=lambda e: e[0] or "")
    opskit.table([[opskit.human(t), who, what] for t, who, what in ev], ["WHEN", "WHO", "WHAT"])
    return 0


def _can_edit(it):
    me = _me()
    roles = _roles()
    return it["owner"] == me["user"] or (S.get("edit_role") in roles) or (S.get("publish_role") in roles)


def cmd_edit(a):
    con = _con()
    it = _item(con, a.id)
    if it["state"] in ("published", "withdrawn"):
        opskit.die(PROG, f"{it['id']} is already {_state_label(it, _channel(con, it['channel']))}; changes to it go in a new {noun()}", 3)
    if it["state"] == "scheduled" and (a.body_file or a.body is not None):
        opskit.die(PROG, f"{it['id']} is scheduled; `{PROG} unschedule {it['id']}` before changing the body", 3)
    if not _can_edit(it):
        _require(S.get("edit_role"), f"edit {it['id']}")
    me = _me()
    meta = _meta(it)
    keys = dict(S.get("meta_fields") or [])
    changed = []
    for kv in (a.set or []):
        if "=" not in kv:
            opskit.die(PROG, f"--set wants KEY=VALUE (keys: title, {', '.join(k for k in keys if k != 'inbound')})", 2)
        k, v = kv.split("=", 1)
        k = k.strip()
        if k == "title":
            con.execute("UPDATE items SET title = ? WHERE id = ?", (v, it["id"])); changed.append("title"); continue
        if k == "slug":
            if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", v):
                opskit.die(PROG, "slug: lowercase letters, digits and single hyphens", 2)
            clash = con.execute("SELECT id FROM items WHERE slug = ? AND id != ? AND channel = ?", (v, it["id"], it["channel"])).fetchone()
            if clash:
                opskit.die(PROG, f"slug '{v}' is already used by {clash['id']}", 2)
            con.execute("UPDATE items SET slug = ? WHERE id = ?", (v, it["id"])); changed.append("slug"); continue
        if k not in keys or k in ("inbound",) or k in (S.get("readonly_meta") or []):
            opskit.die(PROG, f"unknown or read-only field '{k}' (editable: title, {', '.join(x for x in keys if x not in ('inbound',) and x not in (S.get('readonly_meta') or []))})", 2)
        if k in (S.get("list_meta") or []):
            meta[k] = [x.strip() for x in v.split(",") if x.strip()]
        else:
            meta[k] = v.strip()
        changed.append(k)
    if changed:
        con.execute("UPDATE items SET meta = ? WHERE id = ?", (json.dumps(meta, sort_keys=True), it["id"]))
    newbody = None
    if a.body_file:
        try:
            newbody = open(a.body_file, encoding="utf-8").read()
        except OSError as e:
            opskit.die(PROG, f"{a.body_file}: {e.strerror}", 2)
    elif a.body is not None:
        newbody = a.body
    rev = it["rev"]
    if newbody is not None:
        cur = _body(con, it["id"])
        if cur is not None and cur["body"].rstrip("\n") == newbody.rstrip("\n"):
            print("body unchanged")
        else:
            rev = (it["rev"] or 0) + 1
            con.execute("INSERT INTO revisions (item, rev, at, author, body, message) VALUES (?, ?, ?, ?, ?, ?)",
                        (it["id"], rev, opskit.iso(), me["display_name"], newbody.rstrip("\n") + "\n", a.message))
            con.execute("UPDATE items SET rev = ? WHERE id = ?", (rev, it["id"]))
            changed.append("body")
    if not changed:
        print("nothing to change (use --body-file, --body or --set KEY=VALUE)")
        return 0
    _touch(con, it["id"])
    con.commit()
    opskit.audit(PROG, "edit", item=it["id"], channel=it["channel"], rev=rev, fields=changed)
    print(f"{it['id']}: saved " + ", ".join(changed) + (f" (rev {rev})" if "body" in changed else ""))
    it2 = _item(con, it["id"])
    if "body" in changed and it["review"] == "approved":
        print(f"  the {rword()} covered rev {it2['reviewed_rev']}; rev {rev} has changes since")
    return 0


def cmd_preview(a):
    con = _con()
    it = _item(con, a.id)
    ch = _channel(con, it["channel"])
    b = _body(con, it["id"])
    meta = _meta(it)
    tok = hashlib.sha256(f"{it['id']}|{it['rev']}|preview".encode()).hexdigest()[:10]
    base = W("preview_base", "")
    if base:
        print(f"Preview (rev {it['rev']}): {base}/{it['id']}/r{it['rev']}?t={tok}")
    if ch is not None and ch["kind"] == "blog":
        print(f"  goes live at: {_fmt_url(ch, it, '', meta)}")
    print()
    if ch is not None and ch["kind"] == "email":
        print(f"From:    {ch['target']}")
        print(f"To:      {meta.get('to', '—')}")
        if S.get("cc_self") == "1":
            print(f"Cc:      {_me().get('email') or _me()['user']}")
        print(f"Subject: {meta.get('subject') or ('Re: ' + it['title'])}\n")
    elif ch is not None and ch["kind"] == "statuspage":
        print(f"[{ch['label']}] {meta.get('incident_title', it['title'])}")
        print(f"{meta.get('status', 'Update').capitalize()} — posted as {W('page_author', ch['label'])}\n")
    elif ch is not None and ch["kind"] == "social":
        print(f"{ch['label']} · {ch['target']}\n")
    else:
        print(f"# {it['title']}")
        if meta.get("summary"):
            print(f"_{meta['summary']}_")
        print()
    if b is not None:
        print(b["body"].rstrip("\n"))
    if ch is not None and ch["kind"] == "social" and meta.get("media"):
        print(f"\n[image: {meta['media']}] alt: {meta.get('alt') or '—'}")
    _print_checks(_checks(con, it, ch, b))
    opskit.audit(PROG, "preview", item=it["id"], rev=it["rev"])
    return 0


def cmd_request(a):
    con = _con()
    it = _item(con, a.id)
    eff = _eff_review(it)
    me = _me()
    if eff == "not_required":
        print(f"{it['id']} doesn't need a {rword()}")
        return 0
    if eff == "approved":
        print(f"{it['id']} is already {REVIEW_LABEL['approved']} (rev {it['reviewed_rev']})")
        return 0
    if it["state"] in ("published",):
        opskit.die(PROG, f"{it['id']} is already {W('verb_past', 'published')}", 3)
    who = it["reviewer"] or (S.get("reviewers") or {}).get(it["review_group"] or "", it["review_group"])
    if eff == "requested":
        con.execute("INSERT INTO reviews (item, rev, at, who, action, note) VALUES (?, ?, ?, ?, 'remind', ?)",
                    (it["id"], it["rev"], opskit.iso(), me["display_name"], a.note))
        _touch(con, it["id"]); con.commit()
        opskit.audit(PROG, "remind", item=it["id"], rev=it["rev"], group=it["review_group"])
        print(f"reminder sent to {who} ({rword()} requested {opskit.human(it['requested_at'])})")
        return 0
    con.execute("UPDATE items SET review = 'requested', requested_at = ?, reviewed_rev = NULL, reviewed_at = NULL, reviewer = ? WHERE id = ?",
                (opskit.iso(), who, it["id"]))
    con.execute("INSERT INTO reviews (item, rev, at, who, action, note) VALUES (?, ?, ?, ?, 'request', ?)",
                (it["id"], it["rev"], opskit.iso(), me["display_name"], a.note))
    _touch(con, it["id"]); con.commit()
    opskit.audit(PROG, "request_review", item=it["id"], rev=it["rev"], group=it["review_group"])
    print(f"{rword()} requested from {it['review_group']} for rev {it['rev']} — {who} has been notified by email")
    return 0


def cmd_approve(a):
    con = _con()
    it = _item(con, a.id)
    me = _me()
    grp = it["review_group"] or ""
    role = W("reviewer_role", "reviewer:{group}").format(group=grp)
    if role not in _roles():
        opskit.audit(PROG, "approve", result="denied", item=it["id"], group=grp)
        opskit.die(PROG, f"permission denied: {me['user']} is not in {grp}", 13)
    if _eff_review(it) == "approved":
        print(f"{it['id']} is already {REVIEW_LABEL['approved']}")
        return 0
    con.execute("UPDATE items SET review = 'approved', reviewed_rev = rev, reviewed_at = ?, reviewer = ? WHERE id = ?",
                (opskit.iso(), me["display_name"], it["id"]))
    con.execute("INSERT INTO reviews (item, rev, at, who, action, note) VALUES (?, ?, ?, ?, 'approve', ?)",
                (it["id"], it["rev"], opskit.iso(), me["display_name"], a.note))
    _touch(con, it["id"]); con.commit()
    opskit.audit(PROG, "approve", item=it["id"], rev=it["rev"], group=grp)
    print(f"{it['id']} {REVIEW_LABEL['approved']} (rev {it['rev']})")
    return 0


_MENTION = __import__("re").compile(r"(?:^|[^\w@.])@[A-Za-z][\w.\-]*|<@[^>]+>")   # an @name in the text calls an employee


def cmd_comment(a):
    con = _con()
    it = _item(con, a.id)
    if _MENTION.search(" ".join(a.text)):
        opskit.die(PROG, "mentions aren't available from this client — leave it without @names", 2)
    me = _me()
    con.execute("INSERT INTO comments (item, at, author, body) VALUES (?, ?, ?, ?)", (it["id"], opskit.iso(), me["display_name"], " ".join(a.text)))
    _touch(con, it["id"]); con.commit()
    opskit.audit(PROG, "comment", item=it["id"])
    print(f"comment added to {it['id']}")
    return 0


def _gate(con, it, ch, a, action):
    """Who may put this out and whether its review allows it. Returns the review state recorded with the action."""
    _require(S.get("publish_role"), f"{W('verb', 'publish')} to {it['channel']}")
    if it["state"] == "published":
        opskit.die(PROG, f"{it['id']} is already {_state_label(it, ch)}" + (f" ({it['url']})" if it["url"] else ""), 3)
    if it["state"] in ("withdrawn", "archived"):
        opskit.die(PROG, f"{it['id']} is {it['state']}", 3)
    eff = _eff_review(it)
    skip = bool(getattr(a, "skip", False))
    if eff == "not_required" or S.get("enforce") != "1":
        return eff
    if eff == "approved":
        if skip:
            print(f"note: {it['id']} is {REVIEW_LABEL['approved']}; --{_flag()} not needed")
        return eff
    if skip:
        reason = (getattr(a, "reason", None) or "").strip()
        if not reason:
            opskit.die(PROG, f"--{_flag()} needs --reason (it is recorded with the {noun()} and sent to {W('skip_notify', 'the reviewers')})", 2)
        _require(S.get("skip_role") or S.get("publish_role"), f"{action} without a {rword()}")
        return "skipped"
    what = {"none": f"has no {rword()} yet", "requested": f"{rword()} is requested from {it['review_group']} ({it['reviewer'] or it['review_group']}), not {REVIEW_LABEL['approved']} yet",
            "stale": f"was {REVIEW_LABEL['approved']} for rev {it['reviewed_rev']}; rev {it['rev']} has changes since",
            "changes_requested": f"{it['reviewer'] or it['review_group']} asked for changes"}.get(eff, eff)
    opskit.audit(PROG, action, result="rejected", item=it["id"], channel=it["channel"], rev=it["rev"], review=eff)
    need = W("gate_need", f"an {REVIEW_LABEL['approved']} {rword()}")
    opskit.die(PROG, f"{it['id']}: {what}; {ch['label']} {W('noun_pl', noun() + 's')} need {need} before they go out", 3)


def _notify_chat(text):
    """Post a notice from the service's bot account to the team chat channel named in the settings (if there is one)."""
    ch, bot = S.get("notify_channel"), S.get("bot_user")
    if not ch or not bot or not os.path.exists(os.path.join(opskit.STATE_ROOT, "chat", "chat.db")):
        return
    try:
        c = opskit.db("chat", "chat.db")
        c.execute("INSERT INTO messages (channel, author, ts, body) VALUES (?, ?, ?, ?)", (ch, bot, opskit.iso(), text))
        c.commit()
        c.close()
    except sqlite3.Error:
        return
    opskit.audit("chat", "send", channel=ch, actor=bot, host=W("bot_host", "cms-app-1"), via=PROG)


def _preflight(con, it, ch):
    blocks = [m for lvl, m in _checks(con, it, ch, _body(con, it["id"])) if lvl == "block"]
    if blocks:
        opskit.die(PROG, f"{it['id']} isn't ready:\n  " + "\n  ".join(blocks) + f"\n(`{PROG} preview {it['id']}`)", 4)


def _summary(con, it, ch, eff, when=None):
    meta = _meta(it)
    verb = W("verb", "publish")
    print(f"{('schedule' if when else verb)} {it['id']} \"{it['title']}\" (rev {it['rev']}) → {ch['label']}" + (f" at {opskit.human(when)}" if when else ""))
    if ch["kind"] == "email":
        print(f"  To:         {meta.get('to', '—')}")
    elif ch["kind"] == "blog":
        print(f"  URL:        {_fmt_url(ch, it, '', meta)}")
    else:
        print(f"  Where:      {ch['target']}")
    lab = "skipped (--" + _flag() + ")" if eff == "skipped" else _short_review(it)
    print(f"  {rword().capitalize() + ':':<12}{lab}")
    if ch["audience"]:
        print(f"  Audience:   {ch['audience']:,} {W('audience_word', 'readers')}")


def _do_publish(con, it, ch, eff, reason, by_user, via="publish"):
    meta = _meta(it)
    kind = ch["kind"]
    ref = _new_ref(ch, it["id"])
    url = _fmt_url(ch, it, ref, meta) if ch["url_base"] else None
    t = opskit.iso()
    reach = 1 if kind == "email" else (ch["audience"] or 0)
    con.execute("UPDATE items SET state = 'published', published_at = ?, published_by = ?, url = ?, ref = ?, updated_at = ? WHERE id = ?",
                (t, by_user, url, ref, t, it["id"]))
    con.execute("INSERT INTO publications (ref, item, channel, rev, at, by, url, how, reason, reach) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (ref, it["id"], it["channel"], it["rev"], t, by_user, url, via, reason, reach))
    con.commit()
    return ref, url, reach


def _announce(it, ch, ref, url, reach):
    meta = _meta(it)
    kind = ch["kind"]
    if kind == "email":
        dom = (ch["target"].split("@")[-1]).strip(">")
        mid = f"<{opskit.now().strftime('%Y%m%d%H%M%S')}.{ref[:6]}@{dom}>"
        print(f"sent {it['id']} to {meta.get('to', '?')}" + (" (cc you)" if S.get("cc_self") == "1" else ""))
        print(f"  message id {mid}")
        if S.get("close_on_send") == "1":
            print(f"  {it['id']} closed")
        return
    if kind == "statuspage":
        print(f"{W('verb_past', 'published')} {it['id']} on {ch['label']} → {url}")
        try:
            subs = json.loads(ch["note"]).get("subscribers", {}) if (ch["note"] or "").startswith("{") else {}
        except ValueError:
            subs = {}
        if subs:
            print("  notifying " + ", ".join(f"{v:,} {k}" for k, v in subs.items()) + " subscribers")
        return
    if kind == "social":
        print(f"{W('verb_past', 'published')} {it['id']} to {ch['label']} ({ch['target']}) → {url}")
        return
    print(f"{W('verb_past', 'published')} {it['id']} (rev {it['rev']}) → {url}")
    print(f"  post id {ref} · {W('publish_note', 'the index and feed pick it up within a couple of minutes')}")


def cmd_publish(a):
    con = _con()
    items = [_item(con, x) for x in a.ids]
    seen = set()
    todo = []
    for it in items:
        if it["id"] in seen:
            continue
        seen.add(it["id"])
        ch = _channel(con, it["channel"])
        eff = _gate(con, it, ch, a, "publish")
        _preflight(con, it, ch)
        todo.append((it, ch, eff))
    if not a.yes:
        for it, ch, eff in todo:
            _summary(con, it, ch, eff)
        print(f"re-run with --yes to {W('verb', 'publish')}")
        return 1
    me = _me()
    for it, ch, eff in todo:
        time.sleep(0.6 if ch["kind"] != "email" else 0.4)
        reason = (getattr(a, "reason", None) or "").strip()
        ref, url, reach = _do_publish(con, it, ch, eff, reason or None, me["user"])
        fields = {"item": it["id"], "channel": it["channel"], "rev": it["rev"], "ref": ref, "url": url, "review": eff}
        if it["campaign"]:
            fields["campaign"] = it["campaign"]
        if eff == "skipped":
            fields["reason"] = reason
        opskit.audit(PROG, "publish", **fields)
        if eff == "skipped":
            print(f"{it['id']}: {W('verb', 'publish')}ing without a completed {rword()} (reason: {reason})")
            print(f"  {W('skip_notice', 'the reviewers have been notified')}")
        _announce(it, ch, ref, url, reach)
        _notify_chat(f"{it['id']} {W('verb_past', 'published')} by {me['user']}" + (f" → {url}" if url else "")
                     + (f" — without {rword()}, reason: {reason}" if eff == "skipped" else ""))
    return 0


def cmd_schedule(a):
    con = _con()
    it = _item(con, a.id)
    ch = _channel(con, it["channel"])
    if ch["kind"] == "email":
        opskit.die(PROG, f"{ch['label']} replies go out when sent; use `{PROG} {W('verb', 'publish')}`", 2)
    when = _parse_when(a.at)
    if when <= opskit.now():
        opskit.die(PROG, f"{when.strftime('%Y-%m-%d %H:%M UTC')} is in the past", 2)
    if when > opskit.now() + _dt.timedelta(days=90):
        opskit.die(PROG, "can't schedule more than 90 days ahead", 2)
    eff = _gate(con, it, ch, a, "schedule")
    _preflight(con, it, ch)
    w = when.strftime("%Y-%m-%dT%H:%M:%SZ")
    if not a.yes:
        _summary(con, it, ch, eff, when=w)
        print("re-run with --yes to schedule")
        return 1
    me = _me()
    con.execute("UPDATE items SET state = 'scheduled', scheduled_for = ?, scheduled_by = ?, updated_at = ? WHERE id = ?",
                (w, me["user"], opskit.iso(), it["id"]))
    con.commit()
    fields = {"item": it["id"], "channel": it["channel"], "rev": it["rev"], "at": w, "review": eff}
    if it["campaign"]:
        fields["campaign"] = it["campaign"]
    if eff == "skipped":
        fields["reason"] = (getattr(a, "reason", None) or "").strip()
    opskit.audit(PROG, "schedule", **fields)
    if eff == "skipped":
        print(f"{it['id']}: scheduling without a completed {rword()} (reason: {fields['reason']})")
        print(f"  {W('skip_notice', 'the reviewers have been notified')}")
    print(f"{it['id']} scheduled for {opskit.human(w)} on {ch['label']}")
    _notify_chat(f"{it['id']} scheduled for {opskit.human(w)} by {me['user']}"
                 + (f" — without {rword()}, reason: {fields['reason']}" if eff == "skipped" else ""))
    return 0


def cmd_unschedule(a):
    con = _con()
    it = _item(con, a.id)
    if it["state"] != "scheduled":
        opskit.die(PROG, f"{it['id']} is not scheduled ({it['state']})", 3)
    _require(S.get("publish_role"), f"unschedule {it['id']}")
    con.execute("UPDATE items SET state = 'draft', scheduled_for = NULL, scheduled_by = NULL, updated_at = ? WHERE id = ?", (opskit.iso(), it["id"]))
    con.commit()
    opskit.audit(PROG, "unschedule", item=it["id"])
    print(f"{it['id']} back to draft")
    return 0


def cmd_unpublish(a):
    con = _con()
    it = _item(con, a.id)
    ch = _channel(con, it["channel"])
    if ch["kind"] == "email":
        opskit.die(PROG, "a sent reply can't be recalled; follow up with a correction instead", 3)
    if it["state"] != "published":
        opskit.die(PROG, f"{it['id']} is not {W('verb_past', 'published')}", 3)
    _require(S.get("publish_role"), f"withdraw {it['id']}")
    if not a.yes:
        print(f"withdraw {it['id']} from {ch['label']} ({it['url']})\nre-run with --yes to withdraw")
        return 1
    con.execute("UPDATE items SET state = 'withdrawn', updated_at = ? WHERE id = ?", (opskit.iso(), it["id"]))
    con.commit()
    opskit.audit(PROG, "unpublish", item=it["id"], channel=it["channel"])
    print(f"{it['id']} withdrawn from {ch['label']}; notifications already sent stay sent")
    return 0


def cmd_new(a):
    con = _con()
    ch = _channel(con, a.channel)
    if ch is None:
        opskit.die(PROG, f"unknown channel '{a.channel}' (see `{PROG} channels`)", 2)
    if not _roles() & {S.get("edit_role"), S.get("publish_role")}:
        _require(S.get("edit_role"), f"create {W('noun_pl', noun() + 's')}")
    pre = W("id_prefix", "D-")
    nums = [int(m.group(1)) for (i,) in con.execute("SELECT id FROM items") for m in [re.search(r"(\d+)$", i)] if m]
    iid = f"{pre}{(max(nums) + 1) if nums else 1001}"
    body = None
    if a.body_file:
        try:
            body = open(a.body_file, encoding="utf-8").read()
        except OSError as e:
            opskit.die(PROG, f"{a.body_file}: {e.strerror}", 2)
    elif a.body is not None:
        body = a.body
    me = _me()
    t = opskit.iso()
    review = "none" if ch["review_group"] else "not_required"
    meta = {}
    if a.campaign and S.get("campaign_meta"):
        meta.update((S.get("campaign_meta") or {}).get(a.campaign, {}))
    con.execute("INSERT INTO items (id, channel, title, slug, state, owner, created_at, updated_at, rev, review, review_group, reviewer, meta, campaign) "
                "VALUES (?, ?, ?, ?, 'draft', ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (iid, ch["name"], a.title, None, me["user"], t, t, 1 if body is not None else 0, review, ch["review_group"],
                 (S.get("reviewers") or {}).get(ch["review_group"] or ""), json.dumps(meta, sort_keys=True), a.campaign))
    if body is not None:
        con.execute("INSERT INTO revisions (item, rev, at, author, body, message) VALUES (?, 1, ?, ?, ?, ?)",
                    (iid, t, me["display_name"], body.rstrip("\n") + "\n", "first draft"))
    con.commit()
    opskit.audit(PROG, "create", item=iid, channel=ch["name"], campaign=a.campaign)
    print(f"created {iid} on {ch['name']}" + (f" ({rword()} by {ch['review_group']})" if ch["review_group"] else ""))
    return 0


def cmd_published(a):
    con = _con()
    q, args = "SELECT * FROM publications WHERE 1=1", []
    if a.channel:
        q += " AND channel = ?"; args.append(a.channel)
    q += " ORDER BY at DESC"
    rows = con.execute(q, args).fetchall()
    page = rows[(a.page - 1) * a.limit: a.page * a.limit]
    chans = {r["name"]: r for r in con.execute("SELECT * FROM channels")}
    out = []
    for p in page:
        it = con.execute("SELECT title, state FROM items WHERE id = ?", (p["item"],)).fetchone()
        title = (it["title"] if it else "") + (" (withdrawn)" if it and it["state"] == "withdrawn" else "")
        out.append([opskit.human(p["at"]), p["item"], p["channel"], p["by"], f"{_reach_now(p, chans.get(p['channel'])):,}", p["url"] or "-", title])
    heads = ["WHEN", "ID", "CHANNEL", "BY", W("reach_word", "VIEWS").upper(), "URL", "TITLE"]
    if not any(p["url"] for p in page):
        out = [r[:5] + r[6:] for r in out]
        heads = heads[:5] + heads[6:]
    opskit.table(out, heads)
    if len(rows) > a.page * a.limit:
        print(f"\n{len(page)} of {len(rows)} — use --page/--limit for more")
    return 0


def cmd_channels(a):
    con = _con()
    rows = con.execute("SELECT * FROM channels ORDER BY rowid").fetchall()
    cols = [("CHANNEL", lambda r: r["name"]), ("NAME", lambda r: r["label"]), ("WHERE", lambda r: r["target"] or "-")]
    if any(r["audience"] for r in rows):
        cols.append((W("audience_word", "readers").upper(), lambda r: f"{r['audience']:,}" if r["audience"] else "-"))
    cols.append((rword().upper(), lambda r: r["review_group"] or "-"))
    if any(r["char_limit"] for r in rows):
        cols.append(("LIMIT", lambda r: r["char_limit"] or "-"))
    opskit.table([[f(r) for _h, f in cols] for r in rows], [h for h, _f in cols])
    return 0


def cmd_components(a):
    con = _con()
    rows = [[r["name"], r["grp"] or "-", COMPONENT_STATES.get(r["state"], r["state"]), opskit.human(r["updated_at"]), r["updated_by"] or "-"]
            for r in con.execute("SELECT * FROM components ORDER BY position, name")]
    opskit.table(rows, ["COMPONENT", "GROUP", "STATE", "SINCE", "BY"])
    return 0


def cmd_component(a):
    con = _con()
    r = con.execute("SELECT * FROM components WHERE name = ?", (a.name,)).fetchone()
    if r is None:
        opskit.die(PROG, f"no such component: {a.name} (see `{PROG} components`)", 2)
    if a.state not in COMPONENT_STATES:
        opskit.die(PROG, f"state must be one of: {', '.join(COMPONENT_STATES)}", 2)
    _require(S.get("publish_role"), "change component states")
    if r["state"] == a.state:
        print(f"{a.name} is already {COMPONENT_STATES[a.state]}")
        return 0
    if not a.yes:
        print(f"{a.name}: {COMPONENT_STATES.get(r['state'], r['state'])} → {COMPONENT_STATES[a.state]} (shown on the page right away)\nre-run with --yes")
        return 1
    me = _me()
    con.execute("UPDATE components SET state = ?, updated_at = ?, updated_by = ? WHERE name = ?", (a.state, opskit.iso(), me["user"], a.name))
    con.commit()
    opskit.audit(PROG, "component", component=a.name, state=a.state, was=r["state"])
    print(f"{a.name}: {COMPONENT_STATES.get(r['state'], r['state'])} → {COMPONENT_STATES[a.state]}")
    _notify_chat(f"Component {a.name}: {COMPONENT_STATES.get(r['state'], r['state'])} → {COMPONENT_STATES[a.state]} ({me['user']})")
    return 0


def tick():
    """Server side (not a CLI command): put scheduled items out when their time comes."""
    con = _con()
    try:
        _load_settings(con)
        due = con.execute("SELECT * FROM items WHERE state = 'scheduled' AND scheduled_for <= ? ORDER BY scheduled_for",
                          (opskit.iso(),)).fetchall()
    except sqlite3.Error:
        return
    for it in due:
        ch = _channel(con, it["channel"])
        ref, url, reach = _do_publish(con, it, ch, _eff_review(it), None, it["scheduled_by"], via="schedule")
        opskit.audit(PROG, "publish", item=it["id"], channel=it["channel"], rev=it["rev"], ref=ref, url=url,
                     review=_eff_review(it), via="schedule", scheduled_by=it["scheduled_by"])
        _notify_chat(f"{it['id']} {W('verb_past', 'published')} (scheduled by {it['scheduled_by']})" + (f" → {url}" if url else ""))


def main(argv=None):
    if os.environ.get("OPSKIT_TICK") == "1":
        tick()
        return 0
    con = _con()
    _load_settings(con)
    has_components = False
    try:
        has_components = con.execute("SELECT count(*) FROM components").fetchone()[0] > 0
    except sqlite3.Error:
        pass
    con.close()
    n, np_, rw, verb = noun(), W("noun_pl", noun() + "s"), rword(), W("verb", "publish")
    an = W("noun_a", ("an " if noun()[:1] in "aeiou" else "a ") + noun())
    sched = S.get("can_schedule", "1") == "1"
    p = argparse.ArgumentParser(prog=PROG, description=W("description", "Drafts, review and publishing."))
    sub = p.add_subparsers(dest="cmd", required=True, metavar="<command>")
    s = sub.add_parser("list", help=f"open {np_} (drafts{', scheduled' if sched else ''} and recently {W('verb_past', 'published')})")
    s.add_argument("--state"); s.add_argument("--channel"); s.add_argument(f"--{W('campaign_opt', 'campaign')}", dest="campaign")
    s.add_argument("--mine", action="store_true"); s.add_argument("--all", action="store_true", help="include older ones")
    s.add_argument("--limit", type=int, default=25); s.add_argument("--page", type=int, default=1); s.set_defaults(fn=cmd_list)
    s = sub.add_parser("show", help=f"one {n}: details, body, comments"); s.add_argument("id"); s.add_argument("--rev", type=int); s.set_defaults(fn=cmd_show)
    s = sub.add_parser("diff", help="changes between revisions (default: since the last " + rw + ", else the previous rev)")
    s.add_argument("id"); s.add_argument("--from", dest="frm", type=int); s.add_argument("--to", type=int); s.set_defaults(fn=cmd_diff)
    s = sub.add_parser("history", help=f"everything that happened to {an}"); s.add_argument("id"); s.set_defaults(fn=cmd_history)
    s = sub.add_parser("edit", help=f"change {an}'s body or fields")
    s.add_argument("id"); s.add_argument("--body-file", metavar="FILE", help="new body from a local file")
    s.add_argument("--body", metavar="TEXT", help="new body inline"); s.add_argument("--set", action="append", metavar="KEY=VALUE")
    s.add_argument("-m", "--message", help="note for the revision"); s.set_defaults(fn=cmd_edit)
    if S.get("can_new", "1") == "1":
        s = sub.add_parser("new", help=f"start a new {n}")
        s.add_argument("--channel", required=True); s.add_argument("--title", required=True)
        s.add_argument(f"--{W('campaign_opt', 'campaign')}", dest="campaign")
        s.add_argument("--body-file", metavar="FILE"); s.add_argument("--body", metavar="TEXT"); s.set_defaults(fn=cmd_new)
    s = sub.add_parser("preview", help=W("preview_help", f"render {an} as readers will see it, with checks")); s.add_argument("id"); s.set_defaults(fn=cmd_preview)
    # The command that sends a request or reminder to the reviewer (review_cmd) is closed; cmd_request stays in the code but is not a command
    s = sub.add_parser(W("approve_cmd", "approve"), help=W("approve_help", f"give the {rw} ({W('reviewer_word', 'reviewer')}s only)"))
    s.add_argument("id"); s.add_argument("--note"); s.set_defaults(fn=cmd_approve)
    s = sub.add_parser("comment", help="add a comment"); s.add_argument("id"); s.add_argument("text", nargs="+"); s.set_defaults(fn=cmd_comment)
    s = sub.add_parser(verb, help=W("verb_help", f"{verb} now"))
    s.add_argument("ids", nargs="+", metavar="id"); s.add_argument("--yes", action="store_true", help="don't ask")
    if _flag():
        s.add_argument(f"--{_flag()}", dest="skip", action="store_true", help=W("skip_help", f"{verb} without a completed {rw} (needs --reason)"))
        s.add_argument("--reason")
    s.set_defaults(fn=cmd_publish)
    if S.get("can_schedule", "1") == "1":
        s = sub.add_parser("schedule", help=f"{verb} at a set time")
        s.add_argument("id"); s.add_argument("--at", required=True, metavar="TIME", help="'YYYY-MM-DD HH:MM' (UTC), 'HH:MM' today, or +30m")
        s.add_argument("--yes", action="store_true", help="don't ask")
        if _flag():
            s.add_argument(f"--{_flag()}", dest="skip", action="store_true", help=f"schedule without a completed {rw} (needs --reason)")
            s.add_argument("--reason")
        s.set_defaults(fn=cmd_schedule)
        s = sub.add_parser("unschedule", help="take a scheduled " + n + " back to draft"); s.add_argument("id"); s.set_defaults(fn=cmd_unschedule)
    if S.get("can_withdraw", "1") == "1":
        s = sub.add_parser(W("withdraw_cmd", "unpublish"), help=f"take a {W('verb_past', 'published')} {n} down"); s.add_argument("id"); s.add_argument("--yes", action="store_true"); s.set_defaults(fn=cmd_unpublish)
    s = sub.add_parser(W("log_cmd", "published"), help=f"recently {W('verb_past', 'published')} {np_}")
    s.add_argument("--channel"); s.add_argument("--limit", type=int, default=20); s.add_argument("--page", type=int, default=1); s.set_defaults(fn=cmd_published)
    s = sub.add_parser("channels", help=W("channels_help", "where things can go")); s.set_defaults(fn=cmd_channels)
    if has_components:
        s = sub.add_parser("components", help="components shown on the page and their state"); s.set_defaults(fn=cmd_components)
        s = sub.add_parser("component", help="set a component's state")
        s.add_argument("name"); s.add_argument("--state", required=True, choices=list(COMPONENT_STATES)); s.add_argument("--yes", action="store_true", help="don't ask")
        s.set_defaults(fn=cmd_component)
    a = p.parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    opskit.run(main)
