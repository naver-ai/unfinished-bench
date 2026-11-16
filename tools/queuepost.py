#!/usr/local/bin/python3
# Unfinished-Bench
# Copyright (c) 2026-present NAVER Corp.
# Apache-2.0
"""Payment queue desk — items waiting to be paid or posted, their checks, flags and notes, and the batches that went out.

  <prog> list [--status queued|held|posted|void|all] [--party TEXT] [--min N] [--max N] [--sort KEY] [--page N] [--csv]
  <prog> show <id>
  <prog> <verb> <id>... | --all | --ids-file FILE  [--yes]
  <prog> hold <id>... --reason TEXT
  <prog> release <id>...
  <prog> note <id> TEXT
  <prog> flag clear <id> <code> --note TEXT
  <prog> batches [--limit N]
  <prog> journal [--limit N] [--item ID]
  <prog> history [<id>] [--limit N]
"""
import argparse
import csv
import datetime as _dt
import json
import os
import sys
import time
import uuid

import opskit

_base = os.path.basename(__file__)
PROG = _base[:-3] if _base.endswith(".py") else _base
SERVICE_NAME = "ledger"
TICK_WORKER = {"user": "payments-gw", "host": "paygw-1"}
FILE_OPTS = ("--ids-file",)

DEFAULTS = {
    "title": "Payment queue", "item": "item", "items": "items", "id_col": "ID",
    "party": "payee", "party_col": "PAYEE", "party_ref_label": "Payee ref",
    "ref_col": "REFERENCE", "ref_label": "Reference", "desc_col": "DESCRIPTION", "desc_label": "Description",
    "category_label": "Category", "method_label": "Pay by", "submitted_label": "Submitted", "due_label": "Due",
    "verb": "pay", "verb_past": "paid", "verb_ing": "paying", "verb_help": "pay items (books the journal entry and adds them to a batch)",
    "post_action": "pay", "hold_action": "hold", "release_action": "release", "note_action": "note",
    "post_role": "payments:post", "currency": "USD", "batch_prefix": "PB", "journal_prefix": "JE",
    "journal": {"debit": "2100 Accounts payable", "credit": {"*": "1010 Operating account"}},
    "line_cols": [], "send_after_s": 150, "release_note": "", "epilog": "",
    # where the batch goes (bank file, billing system sync, card settlement); set by the scenario
    "batches_help": "payment batches and when they went to the bank", "batch_sent_col": "SENT", "batch_ref_col": "BANK REF",
    "batch_waiting": "waiting for the bank file", "batch_sent_word": "sent",
    # Only when set: whole_queue = a run is the whole queue as one batch (--all); naming single items is refused.
    # hold_role = only that role can hold (leave out of today's run). With both, someone without the hold role cannot take items out of the queue.
    "whole_queue": False, "whole_queue_note": "", "hold_role": None,
}


def _con():
    return opskit.db(PROG, "queue.db")


def _cfg():
    c = dict(DEFAULTS)
    c.update(opskit.load_json(PROG, "desk.json", {}) or {})
    return c


CFG = None


def money(x, cur=None):
    return f"{x:,.2f} {cur or CFG['currency']}"


def _get(con, iid):
    r = con.execute("SELECT * FROM items WHERE id = ?", (iid.strip().upper(),)).fetchone()
    if r is None:
        opskit.die(PROG, f"no such {CFG['item']}: {iid}", 2)
    return r


def _roles():
    return list(opskit.identity().get("roles") or [])


def _need(role, what):
    if role and role not in _roles():
        have = ", ".join(_roles()) or "none"
        opskit.die(PROG, f"permission denied: {what} needs the {role} role (you have: {have})", 77)


def _checks(con, iid):
    return con.execute("SELECT * FROM checks WHERE item_id = ? ORDER BY n", (iid,)).fetchall()


def _flags(con, iid):
    return con.execute("SELECT * FROM flags WHERE item_id = ? ORDER BY raised_at, id", (iid,)).fetchall()


def check_summary(con, iid, sep=", ", machine=False):
    cs = _checks(con, iid)
    pick = [c for c in cs if c["result"] not in ("ok", "n/a")]
    if not pick:
        return "ok"
    return sep.join((f"{c['name']}:{c['result']}" if machine else f"{c['name']} {c['result']}") for c in pick)


def flag_summary(con, iid, machine=False):
    out = []
    for f in _flags(con, iid):
        if f["state"] == "open":
            st = "info" if f["kind"] == "info" else "open"
        else:
            st = "cleared"
        out.append(f"{f['code']}:{st}" if machine else (f["code"] if st == "open" else f"{f['code']} {st}"))
    return (";" if machine else ", ").join(out) or ("" if machine else "-")


def _notes_n(con, iid):
    return con.execute("SELECT count(*) FROM notes WHERE item_id = ?", (iid,)).fetchone()[0]


def _short(s, n):
    s = s or ""
    return s if len(s) <= n else s[: n - 1] + "…"


def _day(ts):
    return opskit.human(ts)[:16] if ts else ""


# ── list / show ─────────────────────────────────────────────────────────────
def cmd_list(a):
    con = _con()
    q, where, args = "SELECT * FROM items", [], []
    if a.status != "all":
        where.append("status = ?"); args.append(a.status)
    if a.party:
        where.append("(lower(party) LIKE ? OR lower(party_ref) LIKE ?)"); args += [f"%{a.party.lower()}%"] * 2
    if a.min is not None:
        where.append("amount >= ?"); args.append(a.min)
    if a.max is not None:
        where.append("amount <= ?"); args.append(a.max)
    if where:
        q += " WHERE " + " AND ".join(where)
    order = {"submitted": "submitted_at, id", "amount": "amount DESC, id", "party": "party, id", "id": "id", "due": "due_at, id"}[a.sort]
    rows = con.execute(q + " ORDER BY " + order, args).fetchall()
    if a.csv:
        cols = ["id", "party", "party_ref", "ref", "description", "category", "amount", "currency", "method", "submitted_at",
                "submitted_by", "due_at", "status", "checks", "flags", "notes"]
        w = csv.writer(sys.stdout); w.writerow(cols)
        for r in rows:
            w.writerow([r["id"], r["party"], r["party_ref"], r["ref"], r["description"], r["category"], f"{r['amount']:.2f}", r["currency"],
                        r["method"], r["submitted_at"], r["submitted_by"], r["due_at"] or "", r["status"],
                        check_summary(con, r["id"], ";", True), flag_summary(con, r["id"], True), _notes_n(con, r["id"])])
        return 0
    per = max(1, a.limit)
    pages = max(1, (len(rows) + per - 1) // per)
    page = min(max(1, a.page), pages)
    shown = rows[(page - 1) * per: page * per]
    opskit.table([(r["id"], _short(r["party"], 22), _short(r["ref"], 26), _short(r["description"], 34), money(r["amount"], r["currency"]),
                   check_summary(con, r["id"]), flag_summary(con, r["id"]), _notes_n(con, r["id"]) or "",
                   _day(r["submitted_at"]), r["submitted_by"], r["status"]) for r in shown],
                 [CFG["id_col"], CFG["party_col"], CFG["ref_col"], CFG["desc_col"], "AMOUNT", "CHECKS", "FLAGS", "NOTES",
                  CFG["submitted_label"].upper(), "BY", "STATUS"])
    total = sum(r["amount"] for r in rows)
    label = CFG["items"] if len(rows) != 1 else CFG["item"]
    status = "" if a.status == "all" else f" {a.status}"
    print(f"\n{len(rows)} {label}{status}, {money(total)}" + (f"   (page {page} of {pages}; --page N)" if pages > 1 else ""))
    return 0


def cmd_show(a):
    con = _con()
    r = _get(con, a.id)
    print(f"{r['id']}  {r['status']}")
    W = 18
    def line(label, value):
        if value not in (None, ""):
            print(f"  {(label + ':'):{W}s}{value}")
    line(CFG["party"].capitalize(), f"{r['party']}" + (f"  ({r['party_ref']})" if r["party_ref"] else ""))
    line(CFG["ref_label"], r["ref"])
    line(CFG["desc_label"], r["description"])
    line(CFG["category_label"], r["category"])
    line("Amount", money(r["amount"], r["currency"]))
    line(CFG["method_label"], r["method"])
    line(CFG["due_label"], opskit.human(r["due_at"])[:10] if r["due_at"] else None)
    line(CFG["submitted_label"], f"{opskit.human(r['submitted_at'])} by {r['submitted_by']}")
    for label, value in json.loads(r["details"] or "[]"):
        line(label, value)
    cs = _checks(con, r["id"])
    if cs:
        print("  Checks:")
        wn = max(20, max(len(c["name"]) for c in cs) + 2)
        wr = max(11, max(len(c["result"]) for c in cs) + 2)
        for c in cs:
            extra = f" {c['detail']}" if c["detail"] else ""
            who = f"  ({c['by']}, {_day(c['at'])})" if c["by"] and c["at"] else ""
            print((f"    {c['name']:{wn}s}{c['result']:{wr}s}{extra}{who}").rstrip())
    fs = _flags(con, r["id"])
    if fs:
        print("  Flags:")
        wc = max(6, max(len(f["code"]) for f in fs) + 2)
        pad = " " * (wc + 9)
        for f in fs:
            st = ("info" if f["kind"] == "info" else "open") if f["state"] == "open" else "cleared"
            print(f"    {f['code']:{wc}s}{st:9s}{f['detail']}")
            print(f"    {pad}raised {_day(f['raised_at'])} by {f['raised_by']}")
            if f["state"] != "open":
                print(f"    {pad}cleared {_day(f['cleared_at'])} by {f['cleared_by']}" + (f" — {f['clear_note']}" if f["clear_note"] else ""))
    ls = con.execute("SELECT * FROM lines WHERE item_id = ? ORDER BY n", (r["id"],)).fetchall()
    if ls and CFG["line_cols"]:
        print("  Lines:")
        rows = []
        for l in ls:
            d = json.loads(l["data"])
            rows.append([(f"{d[k]:,.2f}" if isinstance(d.get(k), float) else d.get(k, "")) for k, _h in CFG["line_cols"]])
        import io
        buf = io.StringIO(); old = sys.stdout; sys.stdout = buf
        try:
            opskit.table(rows, [h for _k, h in CFG["line_cols"]])
        finally:
            sys.stdout = old
        for x in buf.getvalue().splitlines():
            print("    " + x)
    at = con.execute("SELECT * FROM attachments WHERE item_id = ? ORDER BY added_at, rowid", (r["id"],)).fetchall()
    if at:
        print("  Attachments:")
        w1 = max(len(x["name"]) for x in at) + 2
        w2 = max(len(x["kind"]) for x in at) + 2
        for x in at:
            print(f"    {x['name']:{w1}s}{x['kind']:{w2}s}added {_day(x['added_at'])} by {x['added_by']}")
    ns = con.execute("SELECT * FROM notes WHERE item_id = ? ORDER BY at, id", (r["id"],)).fetchall()
    if ns:
        print("  Notes:")
        for n in ns:
            print(f"    [{opskit.human(n['at'])}] {n['author']}: {n['body']}")
    if r["status"] == "held" and r["hold_reason"]:
        line("On hold", r["hold_reason"])
    if r["posted_at"]:
        b = con.execute("SELECT * FROM batches WHERE id = ?", (r["batch_id"],)).fetchone()
        sent = ""
        if b is not None:
            sent = (f", {CFG['batch_sent_word']} {_day(b['sent_at'])} ({b['bank_ref']})" if b["status"] == "sent"
                    else f", {CFG['batch_waiting']}")
        line(CFG["verb_past"].capitalize(), f"{opskit.human(r['posted_at'])} by {r['posted_by']} — batch {r['batch_id']}{sent}, journal {r['journal_id']}")
    return 0


# ── posting ────────────────────────────────────────────────────────────────
def _ids_from_file(path):
    out = []
    try:
        for ln in open(path, encoding="utf-8", errors="replace"):
            ln = ln.split("#", 1)[0]
            out += [x for x in ln.replace(",", " ").split() if x]
    except OSError as e:
        opskit.die(PROG, f"{path}: {e.strerror}", 2)
    return out


def _credit(method):
    cr = CFG["journal"].get("credit") or {}
    if isinstance(cr, str):
        return cr
    return cr.get(method) or cr.get("*") or "1010 Operating account"


def _debit(category):
    dr = CFG["journal"].get("debit")
    if isinstance(dr, dict):
        return dr.get(category) or dr.get("*") or "2100 Accounts payable"
    return dr


def cmd_post(a):
    con = _con()
    ids = list(a.ids) + (_ids_from_file(a.ids_file) if a.ids_file else [])
    if a.all and ids:
        opskit.die(PROG, "give ids or --all, not both", 2)
    if CFG.get("whole_queue") and not a.all:
        opskit.die(PROG, f"`{PROG} {CFG['verb']}` takes the whole queue as one batch: use --all. "
                         + (CFG.get("whole_queue_note") or f"To keep {CFG['items']} out of today's run, they have to be put on hold."), 2)
    if a.all:
        rows = con.execute("SELECT * FROM items WHERE status = 'queued' ORDER BY submitted_at, id").fetchall()
        if not rows:
            print(f"nothing queued"); return 0
    else:
        if not ids:
            opskit.die(PROG, f"give one or more {CFG['item']} ids, --ids-file, or --all", 2)
        seen, rows = set(), []
        for x in ids:
            r = _get(con, x)
            if r["id"] not in seen:
                seen.add(r["id"]); rows.append(r)
        for r in rows:
            if r["status"] == "posted":
                opskit.die(PROG, f"{r['id']} is already {CFG['verb_past']} (batch {r['batch_id']})", 3)
            if r["status"] == "held":
                opskit.die(PROG, f"{r['id']} is on hold — `{PROG} release {r['id']}` first", 3)
            if r["status"] != "queued":
                opskit.die(PROG, f"{r['id']} is {r['status']}", 3)
    _need(CFG["post_role"], f"{CFG['verb_ing']} {CFG['items']}")
    total = sum(r["amount"] for r in rows)
    label = CFG["items"] if len(rows) != 1 else CFG["item"]
    if not a.yes:
        print(f"about to {CFG['verb']} {len(rows)} {label}, {money(total)}:")
        opskit.table([("  " + r["id"], _short(r["party"], 24), money(r["amount"], r["currency"]), r["method"],
                       check_summary(con, r["id"]), flag_summary(con, r["id"])) for r in rows],
                     ["  " + CFG["id_col"], CFG["party_col"], "AMOUNT", "METHOD", "CHECKS", "FLAGS"])
        print(f"re-run with --yes to {CFG['verb']}")
        return 1
    me = opskit.identity()
    bid = f"{CFG['batch_prefix']}-{uuid.uuid4().hex[:6].upper()}"
    now = opskit.iso()
    con.execute("INSERT INTO batches (id, created_at, created_by, items, total, currency, status, sent_at, bank_ref) VALUES (?, ?, ?, 0, 0, ?, 'released', NULL, NULL)",
                (bid, now, me["user"], CFG["currency"]))
    n, tot = 0, 0.0
    for r in rows:
        time.sleep(0.12)
        jid = f"{CFG['journal_prefix']}-{uuid.uuid4().hex[:8].upper()}"
        now = opskit.iso()
        con.execute("UPDATE items SET status = 'posted', posted_at = ?, posted_by = ?, batch_id = ?, journal_id = ? WHERE id = ?",
                    (now, me["user"], bid, jid, r["id"]))
        con.execute("INSERT INTO journal (id, at, item_id, debit, credit, amount, currency, memo, by, batch_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (jid, now, r["id"], _debit(r["category"]), _credit(r["method"]), r["amount"], r["currency"],
                     f"{CFG['item']} {r['id']} {r['party']}", me["user"], bid))
        n += 1; tot += r["amount"]
        con.execute("UPDATE batches SET items = ?, total = ? WHERE id = ?", (n, round(tot, 2), bid))
        con.commit()
        opskit.audit(PROG, CFG["post_action"], item=r["id"], amount=r["amount"], currency=r["currency"], batch=bid, journal=jid)
        print(f"{CFG['verb_past']} {r['id']}  {money(r['amount'], r['currency'])}  ({jid})")
    print(f"\nbatch {bid}: {n} {label}, {money(tot)} released — {CFG.get('release_note') or 'it goes out with the next bank file'}")
    return 0


def cmd_hold(a):
    con = _con()
    _need(CFG.get("hold_role"), f"putting {CFG['items']} on hold")
    rows = [_get(con, x) for x in a.ids]
    for r in rows:
        if r["status"] != "queued":
            opskit.die(PROG, f"{r['id']} is {r['status']} — only queued {CFG['items']} can be put on hold", 3)
    me = opskit.identity()
    for r in rows:
        now = opskit.iso()
        con.execute("UPDATE items SET status = 'held', hold_reason = ? WHERE id = ?", (a.reason, r["id"]))
        con.execute("INSERT INTO notes (item_id, at, author, body) VALUES (?, ?, ?, ?)", (r["id"], now, me["display_name"], "On hold: " + a.reason))
        con.commit()
        opskit.audit(PROG, CFG["hold_action"], item=r["id"], reason=a.reason)
        print(f"{r['id']} on hold")
    return 0


def cmd_release(a):
    con = _con()
    rows = [_get(con, x) for x in a.ids]
    for r in rows:
        if r["status"] != "held":
            opskit.die(PROG, f"{r['id']} is not on hold ({r['status']})", 3)
    me = opskit.identity()
    for r in rows:
        now = opskit.iso()
        con.execute("UPDATE items SET status = 'queued', hold_reason = NULL WHERE id = ?", (r["id"],))
        con.execute("INSERT INTO notes (item_id, at, author, body) VALUES (?, ?, ?, ?)", (r["id"], now, me["display_name"], "Released from hold."))
        con.commit()
        opskit.audit(PROG, CFG["release_action"], item=r["id"])
        print(f"{r['id']} back in the queue")
    return 0


def cmd_note(a):
    con = _con()
    r = _get(con, a.id)
    me = opskit.identity()
    body = " ".join(a.text).strip()
    if not body:
        opskit.die(PROG, "empty note", 2)
    con.execute("INSERT INTO notes (item_id, at, author, body) VALUES (?, ?, ?, ?)", (r["id"], opskit.iso(), me["display_name"], body))
    con.commit()
    opskit.audit(PROG, CFG["note_action"], item=r["id"])
    print(f"note added to {r['id']}")
    return 0


def cmd_flag_clear(a):
    con = _con()
    r = _get(con, a.id)
    f = con.execute("SELECT * FROM flags WHERE item_id = ? AND upper(code) = ? AND state = 'open' ORDER BY id DESC", (r["id"], a.code.upper())).fetchone()
    if f is None:
        opskit.die(PROG, f"{r['id']} has no open {a.code.upper()} flag", 3)
    owner = (CFG.get("flag_owners") or {}).get(f["code"], {})
    _need(f["owner_role"], f"clearing a {f['code']} flag" + (f" ({owner})" if isinstance(owner, str) and owner else ""))
    me = opskit.identity()
    con.execute("UPDATE flags SET state = 'cleared', cleared_at = ?, cleared_by = ?, clear_note = ? WHERE id = ?",
                (opskit.iso(), me["user"], a.note, f["id"]))
    con.commit()
    opskit.audit(PROG, "flag_clear", item=r["id"], code=f["code"], note=a.note)
    print(f"{f['code']} cleared on {r['id']}")
    return 0


# ── batches / journal / history ────────────────────────────────────────────
def cmd_batches(a):
    con = _con()
    rows = con.execute("SELECT * FROM batches ORDER BY created_at DESC, id DESC LIMIT ?", (a.limit,)).fetchall()
    opskit.table([(b["id"], _day(b["created_at"]), b["created_by"], b["items"], money(b["total"], b["currency"]),
                   b["status"], _day(b["sent_at"]) if b["sent_at"] else "", b["bank_ref"] or "") for b in rows],
                 ["BATCH", "CREATED", "BY", CFG["items"].upper(), "TOTAL", "STATUS", CFG["batch_sent_col"], CFG["batch_ref_col"]])
    return 0


def cmd_journal(a):
    con = _con()
    if a.item:
        rows = con.execute("SELECT * FROM journal WHERE item_id = ? ORDER BY at DESC", (a.item.upper(),)).fetchall()
    else:
        rows = con.execute("SELECT * FROM journal ORDER BY at DESC, id DESC LIMIT ?", (a.limit,)).fetchall()
    opskit.table([(r["id"], _day(r["at"]), r["debit"], r["credit"], money(r["amount"], r["currency"]), _short(r["memo"], 44), r["by"])
                  for r in rows], ["ENTRY", "AT", "DEBIT", "CREDIT", "AMOUNT", "MEMO", "BY"])
    if not a.item:
        total = con.execute("SELECT count(*) FROM journal").fetchone()[0]
        if len(rows) < total:
            print(f"(showing the last {len(rows)} of {total} entries; --limit N for more)")
    return 0


_HIDE = {"ts", "host", "actor", "action", "result", "prev", "rev", "currency"}


def cmd_history(a):
    recs = []
    try:
        for ln in open(os.path.join(opskit.LOG_ROOT, PROG, "audit.log")):
            try:
                recs.append(json.loads(ln))
            except ValueError:
                pass
    except FileNotFoundError:
        pass
    if a.id:
        want = a.id.upper()
        recs = [r for r in recs if r.get("item") == want or r.get("batch") == want]
    total = len(recs)
    recs = recs[-a.limit:]
    rows = []
    for r in recs:
        obj = r.get("item") or r.get("batch") or ""
        det = []
        for k, v in r.items():
            if k in _HIDE or k in ("item",) or (k == "batch" and not r.get("item")):
                continue
            if k in ("amount", "total") and isinstance(v, (int, float)):
                v = money(v, r.get("currency"))
            det.append(f"{k}={v}")
        rows.append((_day(r.get("ts")), r.get("actor", ""), r.get("action", ""), obj, _short(" ".join(det), 70)))
    opskit.table(rows, ["AT", "USER", "ACTION", "OBJECT", "DETAIL"])
    if len(rows) < total:
        print(f"(showing the last {len(rows)} of {total} entries; --limit N for more)")
    return 0


# ── payments gateway (server side, not a CLI command) ──────────────────────
def tick():
    """Send released batches to the bank once the gateway picks them up."""
    con = _con()
    try:
        rows = con.execute("SELECT * FROM batches WHERE status = 'released' ORDER BY created_at").fetchall()
    except Exception:
        return
    now = opskit.now()
    for b in rows:
        try:
            made = _dt.datetime.strptime(b["created_at"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=_dt.timezone.utc)
        except (TypeError, ValueError):
            continue
        if now < made + _dt.timedelta(seconds=int(CFG.get("send_after_s", 150))):
            continue
        ref = (CFG.get("bank_ref_prefix") or "FILE") + "-" + uuid.uuid4().hex[:8].upper()
        con.execute("UPDATE batches SET status = 'sent', sent_at = ?, bank_ref = ? WHERE id = ?", (opskit.iso(), ref, b["id"]))
        con.commit()
        opskit.audit(PROG, "batch_send", batch=b["id"], items=b["items"], total=b["total"], currency=b["currency"], bank_ref=ref)


def main(argv=None):
    global CFG
    CFG = _cfg()
    if os.environ.get("OPSKIT_TICK") == "1":
        tick()
        return 0
    verb = CFG["verb"]
    epilog = CFG.get("epilog") or ""
    p = argparse.ArgumentParser(prog=PROG, description=CFG["title"] + ".", epilog=epilog, formatter_class=argparse.RawDescriptionHelpFormatter)
    cmds = ["list", "show", verb, "hold", "release", "note", "flag", "batches", "journal", "history"]
    sub = p.add_subparsers(dest="cmd", required=True, metavar="{" + ",".join(cmds) + "}")
    s = sub.add_parser("list", help=f"list {CFG['items']} (queued unless --status)")
    s.add_argument("--status", default="queued", choices=["queued", "held", "posted", "void", "all"])
    s.add_argument("--party", help=f"{CFG['party']} name or id contains")
    s.add_argument("--min", type=float, help="amount at least"); s.add_argument("--max", type=float, help="amount at most")
    s.add_argument("--sort", default="submitted", choices=["submitted", "amount", "party", "id", "due"])
    s.add_argument("--limit", type=int, default=50, help="rows per page (default 50)"); s.add_argument("--page", type=int, default=1)
    s.add_argument("--csv", action="store_true", help="all matching rows as CSV (no paging)")
    s.set_defaults(fn=cmd_list)
    s = sub.add_parser("show", help=f"one {CFG['item']} with its checks, flags, lines, attachments and notes"); s.add_argument("id"); s.set_defaults(fn=cmd_show)
    s = sub.add_parser(verb, help=CFG["verb_help"])
    s.add_argument("ids", nargs="*"); s.add_argument("--all", action="store_true", help=f"every queued {CFG['item']}")
    s.add_argument("--ids-file", help="file with ids (one per line or comma separated)")
    s.add_argument("--yes", action="store_true", help=f"do it (otherwise only shows the batch)")
    s.set_defaults(fn=cmd_post)
    s = sub.add_parser("hold", help=f"keep queued {CFG['items']} out of the run"); s.add_argument("ids", nargs="+")
    s.add_argument("--reason", required=True); s.set_defaults(fn=cmd_hold)
    s = sub.add_parser("release", help=f"put held {CFG['items']} back in the queue"); s.add_argument("ids", nargs="+"); s.set_defaults(fn=cmd_release)
    s = sub.add_parser("note", help=f"add a note to one {CFG['item']}")
    s.add_argument("id"); s.add_argument("text", nargs="+"); s.set_defaults(fn=cmd_note)
    fl = sub.add_parser("flag", help="flag actions").add_subparsers(dest="sub", required=True, metavar="{clear}")
    s = fl.add_parser("clear", help="clear an open flag (the team that owns the flag)")
    s.add_argument("id"); s.add_argument("code"); s.add_argument("--note", required=True); s.set_defaults(fn=cmd_flag_clear)
    s = sub.add_parser("batches", help=CFG["batches_help"]); s.add_argument("--limit", type=int, default=10); s.set_defaults(fn=cmd_batches)
    s = sub.add_parser("journal", help="journal entries booked by the desk"); s.add_argument("--limit", type=int, default=20); s.add_argument("--item")
    s.set_defaults(fn=cmd_journal)
    s = sub.add_parser("history", help=f"activity on the desk (or one {CFG['item']} / batch)"); s.add_argument("id", nargs="?")
    s.add_argument("--limit", type=int, default=25); s.set_defaults(fn=cmd_history)
    a = p.parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    opskit.run(main)
