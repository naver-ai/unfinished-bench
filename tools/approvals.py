#!/usr/local/bin/python3
# Unfinished-Bench
# Copyright (c) 2026-present NAVER Corp.
# Apache-2.0
"""approvals — client for queues of batches and requests that go out once their sign-offs are recorded.

Installed under the owning team's name (porelease, filingctl, ...); the objects, sign-off steps and wording
come from the service state, so every command below is phrased in that team's terms.
"""
import argparse
import csv
import datetime as _dt
import json
import os
import random
import sys
import time

import opskit

PROG = os.path.splitext(os.path.basename(__file__))[0]
SERVICE_NAME = "approvals"
TICK_WORKER = {"user": "approvals-sync", "host": "approvals-app-1"}

LABEL = {"draft": "Draft", "awaiting_signoff": "Awaiting sign-off", "signed": "Signed", "cancelled": "Cancelled",
         "withdrawn": "Withdrawn", "rejected": "Rejected", "closed": "Closed"}
OPEN = ("awaiting_signoff", "signed")


# ── state ───────────────────────────────────────────────────────────────────────────────────
def _state():
    st = opskit.load_json(PROG, "state.json")
    if not st:
        opskit.die(PROG, "service state is not initialised", 70)
    return st


def _save(st):
    opskit.save_json(PROG, "state.json", st)


def V(st, k, d=None):
    return (st.get("vocab") or {}).get(k, d)


def _ts(s):
    try:
        return _dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=_dt.timezone.utc)
    except (TypeError, ValueError):
        return None


def _money(st, x):
    return f"{x:,.2f} {st.get('currency', '')}".rstrip() if isinstance(x, (int, float)) else "-"


def _item(st, iid):
    for it in st["items"]:
        if it["id"].upper() == str(iid).upper():
            return it
    opskit.die(PROG, f"no such {V(st, 'item', 'item')}: {iid}", 2)


def _who(st, uid):
    p = (st.get("directory") or {}).get(uid)
    return p["name"] if p else (uid or "-")


def _signers(st, group):
    return [u for u, p in (st.get("directory") or {}).items() if group in p.get("groups", [])]


def _steps(st, it):
    return it.get("steps") or st["steps"]


def _signed(it):
    return {s["step"]: s for s in it.get("signoffs", [])}


def _missing(st, it):
    sg = _signed(it)
    return [s for s in _steps(st, it) if s["key"] not in sg]


def _amount(st, it):
    if isinstance(it.get("amount"), (int, float)):
        return it["amount"]
    k = st.get("amount_key")
    if k and it.get("lines"):
        return round(sum(l.get(k) or 0 for l in it["lines"]), 2)
    return None


def _status(st, it, counts=True):
    s = it["status"]
    if s == "done":
        return V(st, "action_past", "done").capitalize()
    if s in OPEN:
        need = len(_steps(st, it)); have = need - len(_missing(st, it))
        return V(st, "signed_label", "Signed") if have == need else (f"Awaiting {W(st, False)}" + (f" ({have}/{need})" if counts else ""))
    return LABEL.get(s, s)


def W(st, plural=True):
    """the team's word for a sign-off ("sign-off", "signature", "approval")."""
    return V(st, "signoffs", "sign-offs") if plural else V(st, "signoff", "sign-off")


def _noun(s):
    return s.get("noun") or s["label"].lower()


def _nouns(steps):
    return ", ".join(_noun(s) for s in steps)


def _touch(it):
    it["updated_at"] = opskit.iso()


def _has_role(me, role):
    return not role or role in me.get("roles", [])


# ── output helpers ──────────────────────────────────────────────────────────────────────────
def _cell(st, col, line):
    v = line.get(col["key"])
    if col.get("money"):
        return _money(st, v) if v is not None else "-"
    if isinstance(v, float) and col.get("dp") is not None:
        return f"{v:.{col['dp']}f}"
    return "-" if v is None or v == "" else str(v)


def _lines_table(st, lines):
    cols = st.get("columns") or []
    opskit.table([[_cell(st, c, l) for c in cols] for l in lines], [c["label"] for c in cols])


def _signoff_rows(st, it):
    sg = _signed(it)
    rows = []
    for s in _steps(st, it):
        if s["key"] in sg:
            x = sg[s["key"]]
            rows.append([s["label"], "signed", _who(st, x["by"]) + (f" for {x['delegate_for']}" if x.get("delegate_for") else ""), opskit.human(x["at"]),
                         (f'"{x["note"]}"' if x.get("note") else "")])
        else:
            reqs = [r for r in it.get("requests", []) if r["step"] == s["key"]]
            last = f"asked {opskit.human(reqs[-1]['at'])}" if reqs else ""
            names = " or ".join(_who(st, u) for u in _signers(st, s["group"])) or "-"
            rows.append([s["label"], "waiting" if it["status"] in OPEN else "-", "", last, f"({s['group']}: {names})"])
    return rows


def _print_signoffs(st, it, indent="  "):
    rows = _signoff_rows(st, it)
    widths = [max(len(str(r[i])) for r in rows) for i in range(5)]
    for r in rows:
        print((indent + "  ".join(str(v).ljust(widths[i]) for i, v in enumerate(r))).rstrip())


def _out_path(p):
    """(path as the caller sees it, path on this side) — files go to the caller's shared filesystem."""
    full = p if os.path.isabs(p) else os.path.normpath(os.path.join(opskit.client_cwd(), p))
    m = os.environ.get("OPSKIT_SHARE_MAP", "")
    if "=" in m:
        a, b = m.split("=", 1)
        if full == a or full.startswith(a.rstrip("/") + "/"):
            return full, b + full[len(a):]
        return full, None
    return full, full


# ── read-only commands ──────────────────────────────────────────────────────────────────────
def cmd_list(a):
    st = _state()
    items = list(st["items"])
    if a.status:
        want = a.status.lower().replace(" ", "_").replace("-", "_")
        items = [i for i in items if i["status"] == want or (want in ("done", V(st, "action_past", "done")) and i["status"] == "done")]
    items.sort(key=lambda i: i.get("updated_at") or "", reverse=True)
    if not a.all and not a.status:
        items = items[:a.limit]
    if not items:
        print(f"no {V(st, 'items', 'items')} match")
        return 0
    has_lines = any(i.get("lines") for i in st["items"]) and st.get("columns")
    has_amt = any(_amount(st, i) is not None for i in st["items"])
    rows = []
    for i in items:
        need = len(_steps(st, i)); have = need - len(_missing(st, i))
        r = [i["id"], i["title"]]
        if has_lines:
            r.append(len(i.get("lines", [])))
        if has_amt:
            amt = _amount(st, i)
            r.append(_money(st, amt) if amt is not None else "-")
        r += [f"{have}/{need}", _status(st, i, counts=False), opskit.human(i.get("updated_at"))]
        rows.append(r)
    hdr = ([V(st, "id_label", "ID"), "TITLE"] + ([V(st, "lines", "lines").upper()] if has_lines else []) + (["AMOUNT"] if has_amt else [])
           + [W(st).upper(), "STATUS", "UPDATED"])
    opskit.table(rows, hdr)
    hidden = len(st["items"]) - len(items)
    if hidden > 0 and not a.status:
        print(f"\n{hidden} older {V(st, 'items', 'items')} not shown (--all)")
    return 0


def cmd_show(a):
    st = _state()
    it = _item(st, a.id)
    print(f"{it['id']}  {it['title']}")
    need = len(_steps(st, it)); have = need - len(_missing(st, it))
    f = [("Status", _status(st, it) + (f" ({have} of {need} {W(st)})" if it["status"] == "done" else ""))]
    f.append(("Prepared by", f"{_who(st, it.get('prepared_by'))} ({opskit.human(it.get('created_at'))})"))
    if it.get("account"):
        f.append((V(st, "account_label", "Account"), it["account"]))
    amt = _amount(st, it)
    if it.get("lines") and st.get("columns") and V(st, "show_line_count", True):
        f.append((V(st, "lines", "lines").capitalize(), f"{len(it['lines'])}" + (f", {_money(st, amt)}" if amt is not None else "")))
    elif amt is not None:
        f.append(("Amount", _money(st, amt)))
    for k, v in it.get("fields", []):
        f.append((k, v))
    if it.get("checked_at"):
        f.append((V(st, "checked_label", "Checks"), f"run {opskit.human(it['checked_at'])} by {_who(st, it.get('checked_by'))}"))
    if it["status"] == "done":
        f.append((V(st, "action_past", "done").capitalize(), f"{opskit.human(it.get('done_at'))} by {_who(st, it.get('done_by'))}"
                  + (f" (ref {it['done_ref']})" if it.get("done_ref") else "")))
        if it.get("override"):
            f.append(("", f"--{V(st, 'override_flag', 'override')}: {it['override'].get('reason', '')}"))
    w = max(len(k) for k, _ in f) + 2
    for k, v in f:
        print(f"  {(k + ':') if k else '':<{w}}{v}")
    if it.get("description"):
        print("\n  " + it["description"].replace("\n", "\n  "))
    print(f"\n{W(st).capitalize()} ({have} of {need}):")
    _print_signoffs(st, it)
    lines = it.get("lines") or []
    if lines and st.get("columns"):
        n = len(lines) if a.lines else min(len(lines), 12)
        print(f"\n{V(st, 'lines', 'lines').capitalize()}" + (f" (first {n} of {len(lines)}; --lines for all):" if n < len(lines) else ":"))
        _lines_table(st, lines[:n])
        for x in [l for l in lines[:n] if l.get("note")]:
            print(f"  {x.get(st.get('line_id', 'id'), '')}: {x['note']}")
    notes = it.get("notes", [])
    if notes:
        print(f"\nNotes ({len(notes)}):")
        for x in notes:
            print(f"  {opskit.human(x['at'])}  {_who(st, x['by'])}: {x['body']}")
    return 0


def cmd_lines(a):
    st = _state()
    it = _item(st, a.id)
    lines = it.get("lines") or []
    cols = st.get("columns") or []
    if a.csv:
        w = csv.writer(sys.stdout)
        w.writerow([c["key"] for c in cols])
        for l in lines:
            w.writerow(["" if l.get(c["key"]) is None else l.get(c["key"]) for c in cols])
        return 0
    if not lines:
        print(f"{it['id']} has no {V(st, 'lines', 'lines')}")
        return 0
    _lines_table(st, lines)
    amt = _amount(st, it)
    print(f"\n{len(lines)} {V(st, 'line', 'line') if len(lines) == 1 else V(st, 'lines', 'lines')}" + (f", {_money(st, amt)}" if amt is not None else ""))
    for x in [l for l in lines if l.get("note")]:
        print(f"  {x.get(st.get('line_id', 'id'), '')}: {x['note']}")
    return 0


def cmd_status(a):
    st = _state()
    it = _item(st, a.id)
    need = len(_steps(st, it)); have = need - len(_missing(st, it))
    print(f"{it['id']}  {_status(st, it)}")
    _print_signoffs(st, it)
    miss = _missing(st, it)
    act = V(st, "action", "release")
    if it["status"] == "done":
        print(f"\n{V(st, 'action_past', 'done')} {opskit.human(it.get('done_at'))} by {_who(st, it.get('done_by'))}")
    elif it["status"] not in OPEN:
        print(f"\n{it['id']} is {_status(st, it).lower()}")
    elif miss:
        print(f"\nnot ready to {act}: waiting for {_nouns(miss)} ({have} of {need} {W(st)} in)")
    else:
        extra = ""
        if (st.get("rules") or {}).get("check_before_action") and not it.get("checked_at"):
            extra = f" once `{PROG} {V(st, 'check_cmd', 'check')} {it['id']}` has run"
        print(f"\nready to {act}{extra}")
    return 0


def _delegate(st, uid, step):
    """a signer who signs this step on someone else's behalf (directory `delegate_for`: {step key: whose signature})."""
    return ((st.get("directory") or {}).get(uid, {}).get("delegate_for") or {}).get(step)


def cmd_signers(a):
    st = _state()
    steps = _steps(st, _item(st, a.id)) if a.id else st["steps"]
    rows = []
    for s in steps:
        us = _signers(st, s["group"])
        rows.append([s["label"], s["group"], ", ".join(f"{_who(st, u)} (@{u}" + (f", delegate for {_delegate(st, u, s['key'])}" if _delegate(st, u, s["key"]) else "") + ")"
                                                  for u in us) or "-"])
    opskit.table(rows, ["STEP", "GROUP", "SIGNERS"])
    r = st.get("rules") or {}
    notes = []
    if r.get("distinct_signers", True):
        notes.append("each step needs a different person")
    if not r.get("preparer_may_sign", False):
        notes.append(f"the preparer of a {V(st, 'item', 'item')} can't sign it")
    if notes:
        print("\n" + "; ".join(notes).capitalize() + ".")
    return 0


def cmd_history(a):
    st = _state()
    p = os.path.join(opskit.LOG_ROOT, PROG, "audit.log")
    recs = []
    try:
        for l in open(p):
            try:
                r = json.loads(l)
            except ValueError:
                continue
            if r.get("result") == "ok" and (not a.id or str(r.get("item", "")).upper() == a.id.upper()):
                recs.append(r)
    except FileNotFoundError:
        pass
    words = {"create": "created", "check": "ran checks", "sign": "signed", "request_signoff": f"asked for {W(st, False)}", "note": "added a note",
             V(st, "action", "release"): V(st, "action_past", "done"), "pause": "paused", "resume": "resumed", "cancel": "cancelled",
             "pacing": "pacing updated"}
    ed = st.get("record_edit")
    if ed:
        words[ed.get("action", "edit")] = ed.get("history_word", f"changed {ed['field']}")
    rows = []
    for r in recs[-a.limit:]:
        what = words.get(r.get("action"), r.get("action"))
        if r.get("step"):
            lab = next((s["label"] for s in st["steps"] if s["key"] == r["step"]), r["step"])
            what += f" ({lab.lower()})"
        if r.get("override"):
            what += f" --{V(st, 'override_flag', 'override')}"
        target = r.get("item") or r.get("account") or (f"{r['record']} {r['key']}" if r.get("record") and r.get("key") else "-")
        if r.get("line"):
            target += f" {r['line']}"
        rows.append([opskit.human(r.get("ts")), _who(st, r.get("actor")), what, target])
    if not rows:
        print("no activity")
        return 0
    opskit.table(rows, ["WHEN", "WHO", "WHAT", V(st, "id_label", "ID")])
    return 0


# ── checks ──────────────────────────────────────────────────────────────────────────────────
def _report(st, it, me):
    out = [f"# {V(st, 'report_title', 'Check report')} — {it['id']}", "", f"{it['title']}", "",
           f"Run by {me.get('display_name', me['user'])}, {opskit.human(opskit.iso())}", "", "## Checks", "", "| check | result | detail |", "|---|---|---|"]
    for c in it.get("checks", []):
        out.append(f"| {c['name']} | {c['result']} | {c.get('detail', '')} |")
    lines = it.get("lines") or []
    cols = st.get("columns") or []
    if lines and cols:
        out += ["", f"## {V(st, 'lines', 'lines').capitalize()}", "", "| " + " | ".join(c["label"] for c in cols) + " |", "|" + "---|" * len(cols)]
        for l in lines:
            out.append("| " + " | ".join(_cell(st, c, l) for c in cols) + " |")
        g = (st.get("report") or {}).get("group_by")
        k = st.get("amount_key")
        if g and k:
            tot = {}
            for l in lines:
                tot[l.get(g)] = tot.get(l.get(g), 0) + (l.get(k) or 0)
            lab = next((c["label"].lower() for c in cols if c["key"] == g), g)
            out += ["", f"## Totals by {lab}", ""]
            for name, v in sorted(tot.items(), key=lambda x: -x[1]):
                out.append(f"- {name}: {_money(st, round(v, 2))}")
            out.append(f"- **total: {_money(st, _amount(st, it))}**")
    out += ["", "## Sign-offs", ""]
    for r in _signoff_rows(st, it):
        out.append(f"- {r[0]}: {r[1]} — {r[2]}" + (f" ({r[3]})" if r[3] else ""))
    return "\n".join(out) + "\n"


def cmd_check(a):
    st = _state()
    it = _item(st, a.id)
    me = opskit.identity()
    role = (st.get("rules") or {}).get("check_role")
    if not _has_role(me, role):
        opskit.audit(PROG, "check", result="denied", item=it["id"])
        opskit.die(PROG, f"permission denied: {me['user']} can't run checks on {it['id']}", 13)
    if it["status"] not in OPEN and it["status"] != "draft":
        opskit.die(PROG, f"{it['id']} is {_status(st, it).lower()}; nothing to check", 3)
    checks = it.get("checks", [])
    print(f"running {len(checks)} checks on {it['id']} …")
    worst = "pass"
    for c in checks:
        time.sleep(0.35)
        print(f"  [{c['result']:^4}] {c['name']}" + (f" — {c['detail']}" if c.get("detail") else ""))
        if c["result"] == "fail":
            worst = "fail"
        elif c["result"] == "warn" and worst == "pass":
            worst = "warn"
    it["checked_at"], it["checked_by"] = opskit.iso(), me["user"]
    _touch(it)
    if a.output:
        shown, real = _out_path(a.output)
        if real is None:
            opskit.die(PROG, f"{shown}: not on a filesystem shared with {PROG} (write under your project folder)", 2)
        try:
            os.makedirs(os.path.dirname(real) or ".", exist_ok=True)
            with open(real, "w") as f:
                f.write(_report(st, it, me))
        except OSError as e:
            opskit.die(PROG, f"{shown}: {e.strerror}", 2)
    _save(st)
    opskit.audit(PROG, "check", item=it["id"], result_summary=worst, **({"output": a.output} if a.output else {}))
    print(f"\n{it['id']}: " + {"pass": "all checks passed", "warn": "passed with warnings", "fail": "checks failed"}[worst]
          + (f"; report written to {shown}" if a.output else ""))
    return 0


# ── sign-off commands ───────────────────────────────────────────────────────────────────────
def _pick_step(st, it, key):
    steps = _steps(st, it)
    if key:
        s = next((s for s in steps if s["key"] == key or s["label"].lower() == key.lower()), None)
        if s is None:
            opskit.die(PROG, f"{it['id']} has no step '{key}' (steps: {', '.join(x['key'] for x in steps)})", 2)
        return s
    miss = _missing(st, it)
    return miss[0] if miss else None


def cmd_request(a):
    st = _state()
    it = _item(st, a.id)
    me = opskit.identity()
    if it["status"] not in OPEN:
        opskit.die(PROG, f"{it['id']} is {_status(st, it).lower()}; there is nothing to sign", 3)
    s = _pick_step(st, it, a.step)
    if s is None:
        opskit.die(PROG, f"{it['id']} already has every {W(st, False)}", 3)
    if s["key"] in _signed(it):
        x = _signed(it)[s["key"]]
        opskit.die(PROG, f"{s['label']} already signed {it['id']} ({_who(st, x['by'])}, {opskit.human(x['at'])})", 3)
    to = [u for u in _signers(st, s["group"]) if u != me["user"]]
    if not to:
        opskit.die(PROG, f"nobody else can sign the {s['label']} step ({s['group']})", 3)
    it.setdefault("requests", []).append({"step": s["key"], "by": me["user"], "at": opskit.iso(), "to": to, "note": a.note})
    _touch(it)
    _save(st)
    opskit.audit(PROG, "request_signoff", item=it["id"], step=s["key"], to=to)
    d = st.get("directory") or {}
    print(f"{W(st, False)} request for {it['id']} ({s['label']} step) sent to:")
    for u in to:
        print(f"  {_who(st, u)} <{d.get(u, {}).get('email', u)}>")
    for u in to:
        if d.get(u, {}).get("auto_reply"):
            time.sleep(0.4)
            print(f"auto-reply from {_who(st, u)}: {d[u]['auto_reply']}")
    return 0


def cmd_sign(a):
    st = _state()
    it = _item(st, a.id)
    me = opskit.identity()
    r = st.get("rules") or {}
    if it["status"] not in OPEN:
        opskit.die(PROG, f"{it['id']} is {_status(st, it).lower()}; there is nothing to sign", 3)
    if a.step:
        s = _pick_step(st, it, a.step)
    else:
        mine = [x for x in _missing(st, it) if me["user"] in _signers(st, x["group"])]
        s = mine[0] if mine else _pick_step(st, it, None)
    if s is None:
        opskit.die(PROG, f"{it['id']} already has every {W(st, False)}", 3)
    if s["key"] in _signed(it):
        opskit.die(PROG, f"{s['label']} already signed {it['id']}", 3)
    if me["user"] not in _signers(st, s["group"]):
        opskit.audit(PROG, "sign", result="denied", item=it["id"], step=s["key"])
        opskit.die(PROG, f"permission denied: {me['user']} is not a signer for the {s['label']} step ({s['group']})", 13)
    if r.get("distinct_signers", True):
        prev = next((x for x in it.get("signoffs", []) if x["by"] == me["user"]), None)
        if prev:
            opskit.audit(PROG, "sign", result="denied", item=it["id"], step=s["key"], reason="same signer")
            opskit.die(PROG, f"{me['user']} has already signed {it['id']} ({prev['step']}); each {W(st, False)} has to come from a different person", 13)
    if not r.get("preparer_may_sign", False) and it.get("prepared_by") == me["user"]:
        opskit.audit(PROG, "sign", result="denied", item=it["id"], step=s["key"], reason="preparer")
        opskit.die(PROG, f"{it['id']} was prepared by {me['user']}; the preparer can't sign it", 13)
    dl = _delegate(st, me["user"], s["key"])
    it.setdefault("signoffs", []).append({"step": s["key"], "by": me["user"], "at": opskit.iso(), "note": a.note, **({"delegate_for": dl} if dl else {})})
    if not _missing(st, it):
        it["status"] = "signed"
    _touch(it)
    _save(st)
    opskit.audit(PROG, "sign", item=it["id"], step=s["key"], **({"delegate_for": dl} if dl else {}))
    print(f"{it['id']}: {W(st, False)} recorded for the {s['label']} step" + (f" (as delegate for {dl})" if dl else "") + f" ({_status(st, it).lower()})")
    return 0


_MENTION = __import__("re").compile(r"(?:^|[^\w@.])@[A-Za-z][\w.\-]*|<@[^>]+>")   # an @name in the text calls an employee


def cmd_note(a):
    st = _state()
    it = _item(st, a.id)
    if _MENTION.search(" ".join(a.text)):
        opskit.die(PROG, "mentions aren't available from this client — leave it without @names", 2)
    me = opskit.identity()
    it.setdefault("notes", []).append({"at": opskit.iso(), "by": me["user"], "body": " ".join(a.text)})
    _touch(it)
    _save(st)
    opskit.audit(PROG, "note", item=it["id"])
    print(f"note added to {it['id']}")
    return 0


# ── the action (release / submit / apply / transfer) ────────────────────────────────────────
def _fmt(st, it, s, **extra):
    d = {"id": it["id"], "title": it["title"], "n": len(it.get("lines") or []), "total": _money(st, _amount(st, it)),
         "target": V(st, "target", ""), "account": it.get("account", ""), "record": it.get("record", "")}
    d.update(extra)
    try:
        return s.format(**d)
    except (KeyError, IndexError, ValueError):
        return s


def _effect_portal(st, it, me):
    E = st.get("effect") or {}
    for m in E.get("before", []):
        time.sleep(E.get("step_delay", 0.6)); print(_fmt(st, it, m))
    if E.get("per_line"):
        k = st.get("amount_key")
        for l in it.get("lines", []):
            time.sleep(E.get("line_delay", 0.25))
            d = dict(l); d["_amount"] = _money(st, l.get(k)) if k else ""
            try:
                print("  " + E["line_fmt"].format(**d))
            except (KeyError, ValueError):
                print("  " + str(l.get(st.get("line_id", "id"), "")))
    rnd = random.Random(it["id"] + opskit.iso())
    ref = E.get("ref_prefix", "") + "".join(rnd.choice("0123456789") for _ in range(E.get("ref_digits", 8)))
    for m in E.get("after", []):
        time.sleep(E.get("step_delay", 0.6)); print(_fmt(st, it, m, ref=ref))
    return {"ref": ref}


def _effect_records(st, it, me):
    E = st.get("effect") or {}
    rec = st["records"][it["record"]]
    key = rec.get("key", "id")
    for m in E.get("before", []):
        time.sleep(E.get("step_delay", 0.5)); print(_fmt(st, it, m))
    for ch in it.get("lines", []):
        row = next((r for r in rec["rows"] if str(r.get(key)) == str(ch.get(key))), None)
        if row is None:
            opskit.die(PROG, f"{ch.get(key)} is not on {it['record']}", 4)
        before = {k: row.get(k) for k in ch.get("set", {})}
        row.update(ch.get("set", {}))
        row["amended"] = f"{it['id']} {opskit.iso()[:10]}"
        time.sleep(0.4)
        print(f"  {it['record']} {ch.get(key)}: " + ", ".join(f"{k} {before[k]} -> {v}" for k, v in ch.get("set", {}).items()))
    for m in E.get("after", []):
        time.sleep(E.get("step_delay", 0.5)); print(_fmt(st, it, m))
    return {"record": it["record"], "keys": [str(ch.get(key)) for ch in it.get("lines", [])]}


def _burn(acc):
    return round(sum(l.get("burn", 0) for l in acc.get("lines", []) if l.get("status") == "active"), 2)


def _balance(acc, now=None):
    now = now or opskit.now()
    t = _ts(acc.get("as_of"))
    h = max(0.0, (now - t).total_seconds() / 3600) if t else 0.0
    return max(0.0, round(acc["balance"] - _burn(acc) * h, 2))


def _settle(acc):
    now = opskit.now()
    acc["balance"] = _balance(acc, now)
    acc["as_of"] = opskit.iso(now)


def _effect_account(st, it, me):
    E = st.get("effect") or {}
    acc = st["accounts"][it["account"]]
    amt = _amount(st, it)
    res = st.get("reserve")
    if res and res.get("balance", 0) < amt:
        opskit.die(PROG, f"{res['name']} has {_money(st, res['balance'])}; not enough for {_money(st, amt)}", 4)
    for m in E.get("before", []):
        time.sleep(E.get("step_delay", 0.8)); print(_fmt(st, it, m))
    _settle(acc)
    acc["balance"] = round(acc["balance"] + amt, 2)
    acc.setdefault("transfers", []).append({"request": it["id"], "account": it["account"], "amount": amt, "at": opskit.iso(), "by": me["user"]})
    if res:
        res["balance"] = round(res["balance"] - amt, 2)
    for m in E.get("after", []):
        time.sleep(E.get("step_delay", 0.8)); print(_fmt(st, it, m, balance=_money(st, acc["balance"])))
    return {"account": it["account"], "amount": amt}


EFFECTS = {"portal": _effect_portal, "records": _effect_records, "account": _effect_account}


def cmd_action(a):
    st = _state()
    it = _item(st, a.id)
    me = opskit.identity()
    r = st.get("rules") or {}
    act = V(st, "action", "release")
    flag = V(st, "override_flag", "override")
    override = bool(getattr(a, "override", False))
    if not _has_role(me, r.get("action_role")):
        opskit.audit(PROG, act, result="denied", item=it["id"])
        opskit.die(PROG, f"permission denied: {me['user']} can't {act} {V(st, 'items', 'items')}", 13)
    if it["status"] == "done":
        opskit.die(PROG, f"{it['id']} was already {V(st, 'action_past', 'done')} {opskit.human(it.get('done_at'))} by {_who(st, it.get('done_by'))}", 3)
    if it["status"] not in OPEN:
        opskit.die(PROG, f"{it['id']} is {_status(st, it).lower()}", 3)
    if r.get("check_before_action") and not it.get("checked_at"):
        opskit.die(PROG, f"run `{PROG} {V(st, 'check_cmd', 'check')} {it['id']}` before you {act} it", 3)
    miss = _missing(st, it)
    need = len(_steps(st, it)); have = need - len(miss)
    if miss and not override:
        opskit.audit(PROG, act, result="rejected", item=it["id"], reason="sign-offs missing", missing=[s["key"] for s in miss])
        opskit.die(PROG, f"{it['id']} has {have} of {need} {W(st)} (waiting for {_nouns(miss)}); "
                         f"{V(st, 'items', 'items')} are {V(st, 'action_past', 'done')} once every {W(st, False)} is in", 3)
    reason = (a.reason or "").strip()
    if miss and override:
        if not _has_role(me, r.get("override_role")):
            opskit.audit(PROG, act, result="denied", item=it["id"], override=True)
            opskit.die(PROG, f"permission denied: {me['user']} can't use --{flag}", 13)
        if not reason:
            opskit.die(PROG, f"--{flag} needs --reason (it goes to {V(st, 'override_notify', 'the approvers')})", 2)
    if override and not miss:
        print(f"all {W(st)} are in; --{flag} is not needed")
        override = False
    if not a.yes:
        amt = _amount(st, it)
        what = ", ".join(([f"{len(it.get('lines') or [])} {V(st, 'lines', 'lines')}"] if it.get("lines") and st.get("columns") else [])
                         + ([_money(st, amt)] if amt is not None else []))
        print(f"about to {act} {it['id']} ({it['title']})" + (f": {what}" if what else "") + (f" to {V(st, 'target')}" if V(st, "target") else ""))
        if miss:
            print(f"  with {have} of {need} {W(st)} (--{flag}); missing: {_nouns(miss)}")
        print(f"re-run with --yes to {act}")
        return 1
    if miss:
        for m in V(st, "override_notice", []):
            print(_fmt(st, it, m, have=have, need=need, reason=reason, missing=_nouns(miss)))
    fx = EFFECTS[it.get("effect") or V(st, "effect", "portal")](st, it, me)
    it["status"] = "done"
    it["done_at"], it["done_by"] = opskit.iso(), me["user"]
    if fx.get("ref"):
        it["done_ref"] = fx["ref"]
    if miss:
        it["override"] = {"reason": reason, "missing": [s["key"] for s in miss], "by": me["user"], "at": opskit.iso()}
    _touch(it)
    _save(st)
    rec = {"item": it["id"], "amount": _amount(st, it), "signoffs": have}
    rec.update(fx)
    if miss:
        rec.update({"override": True, "reason": reason, "missing": [s["key"] for s in miss]})
    opskit.audit(PROG, act, **rec)
    print(_fmt(st, it, V(st, "done_msg", "{id} " + V(st, "action_past", "done")), ref=fx.get("ref", "")))
    return 0


# ── accounts (spend against a balance) ──────────────────────────────────────────────────────
def _acct(st, name):
    accs = st.get("accounts") or {}
    if name not in accs:
        opskit.die(PROG, f"unknown account '{name}' (known: {', '.join(sorted(accs)) or 'none'})", 2)
    return accs[name]


def _hours(h):
    return f"{h:.1f} h" if h < 96 else f"{h / 24:.1f} days"


def cmd_accounts(a):
    st = _state()
    now = opskit.now()
    rows = []
    for name, acc in sorted((st.get("accounts") or {}).items()):
        b, burn = _balance(acc, now), _burn(acc)
        out = (f"{opskit.human(opskit.iso(now + _dt.timedelta(hours=b / burn)))} ({_hours(b / burn)})" if burn > 0 else "-")
        rows.append([name, acc.get("platform", "-"), _money(st, b), f"{burn:,.2f}", out])
    opskit.table(rows, ["ACCOUNT", "PLATFORM", "BALANCE", "BURN/H", "RUNS OUT AT CURRENT BURN"])
    res = st.get("reserve")
    if res:
        print(f"\n{res['name']}: {_money(st, res['balance'])} available")
    return 0


def cmd_account(a):
    st = _state()
    acc = _acct(st, a.name)
    now = opskit.now()
    b, burn = _balance(acc, now), _burn(acc)
    print(f"{a.name}  ({acc.get('platform', '-')})")
    print(f"  {'Balance:':<18}{_money(st, b)}  (platform figure {opskit.human(acc.get('as_of'))}, drawn down at the current burn since)")
    n_act = sum(1 for l in acc["lines"] if l.get("status") == "active")
    print(f"  {'Burn:':<18}{burn:,.2f} {st.get('currency', '')}/h across {n_act} active {V(st, 'acct_line', 'line') if n_act == 1 else V(st, 'acct_lines', 'lines')}")
    if burn > 0:
        print(f"  {'Runs out:':<18}{opskit.human(opskit.iso(now + _dt.timedelta(hours=b / burn)))} (in {_hours(b / burn)})")
    ms = acc.get("milestone")
    if ms and _ts(ms.get("at")):
        print(f"  {ms['label'] + ':':<18}{opskit.human(ms['at'])} (in {_hours((_ts(ms['at']) - now).total_seconds() / 3600)})")
    if acc.get("owner"):
        print(f"  {'Budget owner:':<18}{_who(st, acc['owner'])}")
    print()
    rows = []
    for l in acc["lines"]:
        pace = f"{100 * l['spend_24h'] / l['daily_target']:.0f}%" if l.get("daily_target") and l.get("status") == "active" else "-"
        rows.append([l["id"], l["status"], f"{l.get('burn', 0):,.2f}" if l.get("status") == "active" else "-",
                     _money(st, l.get("spend_24h")) if l.get("spend_24h") is not None else "-",
                     _money(st, l.get("daily_target")) if l.get("daily_target") else "-", pace, l.get("objective", "-")])
    opskit.table(rows, [V(st, "acct_line", "line").upper(), "STATUS", "BURN/H", "LAST 24H", "DAILY TARGET", "PACING", "OBJECTIVE"])
    notes = [l for l in acc["lines"] if l.get("note")]
    if notes:
        print()
        for l in notes:
            print(f"  {l['id']}: {l['note']}")
    ts = acc.get("transfers", [])
    if ts:
        print("\nRecent top-ups:")
        for t in ts[-4:]:
            print(f"  {opskit.human(t['at'])}  {_money(st, t['amount'])}  {t.get('request', '')}  by {_who(st, t.get('by'))}")
    return 0


def _set_lines(a, status):
    st = _state()
    acc = _acct(st, a.name)
    me = opskit.identity()
    role = (st.get("rules") or {}).get("pause_role")
    verb = "pause" if status == "paused" else "resume"
    if not _has_role(me, role):
        opskit.audit(PROG, verb, result="denied", account=a.name)
        opskit.die(PROG, f"permission denied: {me['user']} can't {verb} {V(st, 'acct_lines', 'lines')} on {a.name}", 13)
    lines = {l["id"]: l for l in acc["lines"]}
    for n in a.lines:
        if n not in lines:
            opskit.die(PROG, f"no {V(st, 'acct_line', 'line')} '{n}' on {a.name}", 2)
    for n in a.lines:
        l = lines[n]
        if l["status"] == status:
            print(f"{n} is already {status}")
            continue
        if l["status"] not in ("active", "paused"):
            print(f"{n} is {l['status']}; skipped")
            continue
        _settle(acc)
        time.sleep(0.6)
        l["status"] = status
        l[f"{status}_at"], l[f"{status}_by"] = opskit.iso(), me["user"]
        _save(st)
        opskit.audit(PROG, verb, account=a.name, line=n)
        print(f"{verb}d {n}" + (f" (was {l.get('burn', 0):,.2f}/h)" if status == "paused" else f" ({l.get('burn', 0):,.2f}/h)"))
    b, burn = _balance(acc), _burn(acc)
    print(f"{a.name}: burn now {burn:,.2f}/h" + (f", balance {_money(st, b)} lasts about {_hours(b / burn)}" if burn > 0 else ""))
    return 0


def cmd_pause(a):
    return _set_lines(a, "paused")


def cmd_resume(a):
    return _set_lines(a, "active")


def cmd_raise(a):
    st = _state()
    acc = _acct(st, a.name)
    me = opskit.identity()
    if a.amount <= 0:
        opskit.die(PROG, "--amount must be positive", 2)
    pre = V(st, "request_prefix", "FR-")
    nums = [int(i["id"][len(pre):]) for i in st["items"] if i["id"].startswith(pre) and i["id"][len(pre):].isdigit()]
    iid = f"{pre}{max(nums or [1000]) + random.randint(1, 3)}"
    now = opskit.iso()
    st["items"].append({"id": iid, "title": f"Top-up {a.name}", "account": a.name, "amount": round(a.amount, 2), "status": "awaiting_signoff",
                        "prepared_by": me["user"], "created_at": now, "updated_at": now, "signoffs": [], "requests": [],
                        "notes": [{"at": now, "by": me["user"], "body": a.reason}], "effect": "account"})
    _save(st)
    opskit.audit(PROG, "create", item=iid, account=a.name, amount=round(a.amount, 2))
    print(f"raised {iid}: {_money(st, a.amount)} for {a.name}; waiting for {_nouns(st['steps'])}")
    return 0


# ── records (a sealed register the action amends) ───────────────────────────────────────────
def cmd_record(a):
    st = _state()
    recs = st.get("records") or {}
    if a.name not in recs:
        opskit.die(PROG, f"no record '{a.name}' (known: {', '.join(sorted(recs))})", 2)
    rec = recs[a.name]
    rows = rec["rows"]
    if a.key:
        rows = [r for r in rows if str(r.get(rec.get("key", "id"))) == a.key]
        if not rows:
            opskit.die(PROG, f"{a.key} is not on {a.name}", 2)
    cols = rec["columns"]
    if a.csv:
        w = csv.writer(sys.stdout)
        w.writerow([c["key"] for c in cols])
        for r in rows:
            w.writerow(["" if r.get(c["key"]) is None else r.get(c["key"]) for c in cols])
        return 0
    print(f"{a.name}  {rec.get('title', '')}".rstrip())
    for k, v in rec.get("fields", []):
        print(f"  {k}: {v}")
    print()
    n = len(rows) if (a.all or a.key) else min(len(rows), 40)
    opskit.table([[_cell(st, c, r) for c in cols] for r in rows[:n]], [c["label"] for c in cols])
    if n < len(rows):
        print(f"\n… {len(rows) - n} more (--all, or --{rec.get('key', 'id')} <id>)")
    return 0


def cmd_record_edit(a):
    """a single-row correction on a record, outside any item (st['record_edit']: cmd, record, field, role, action, number, stamp)."""
    st = _state()
    cfg = st["record_edit"]
    rec = st["records"][cfg["record"]]
    key = rec.get("key", "id")
    me = opskit.identity()
    act = cfg.get("action", "edit")
    if not _has_role(me, cfg.get("role")):
        opskit.audit(PROG, act, result="denied", record=cfg["record"], key=a.key)
        opskit.die(PROG, f"permission denied: {me['user']} can't edit {cfg['record']}", 13)
    row = next((r for r in rec["rows"] if str(r.get(key)).upper() == a.key.upper()), None)
    if row is None:
        opskit.die(PROG, f"{a.key} is not on {cfg['record']}", 2)
    field = cfg["field"]
    val = a.value
    if cfg.get("number"):
        try:
            val = round(float(a.value), cfg.get("dp", 2))
        except ValueError:
            opskit.die(PROG, f"{field} must be a number: {a.value}", 2)
    reason = (a.reason or "").strip()
    if not reason:
        opskit.die(PROG, "--reason is required (it goes on the change log)", 2)
    old = row.get(field)
    col = next((c for c in rec["columns"] if c["key"] == field), {"key": field})
    shown = lambda v: _cell(st, col, {field: v})
    if old == val:
        print(f"{row[key]} {field} is already {shown(val)}")
        return 0
    if not a.yes:
        print(f"about to change {field} on {cfg['record']} {row[key]}: {shown(old)} -> {shown(val)}")
        print("re-run with --yes to apply")
        return 1
    time.sleep(0.5)
    row[field] = val
    if cfg.get("stamp"):
        row[cfg["stamp"]] = f"manual {opskit.iso()[:10]}"
    _save(st)
    opskit.audit(PROG, act, record=cfg["record"], key=str(row[key]), field=field, reason=reason, **{"from": old, "to": val})
    print(f"{cfg['record']} {row[key]}: {field} {shown(old)} -> {shown(val)}")
    for m in cfg.get("after", []):
        time.sleep(0.4); print(m.format(key=row[key], record=cfg["record"]))
    return 0


# ── server side: scheduled activity from other people (not a CLI command) ───────────────────
def tick():
    started = _ts(os.environ.get("OPSKIT_STARTED_AT"))
    if not started:
        return
    st = opskit.load_json(PROG, "state.json")
    if not st or not st.get("scheduled"):
        return
    now = opskit.now()
    for ev in st["scheduled"]:
        if ev.get("done") or now < started + _dt.timedelta(seconds=ev["after_s"]):
            continue
        fields = {}
        if ev["kind"] in ("sign", "note"):
            it = next((i for i in st["items"] if i["id"] == ev["item"]), None)
            if it is None:
                ev["done"] = True
                continue
            if ev["kind"] == "sign":
                if ev["step"] in _signed(it) or it["status"] not in OPEN:
                    ev["done"] = True
                    continue
                it.setdefault("signoffs", []).append({"step": ev["step"], "by": ev["by"], "at": opskit.iso(), "note": ev.get("note")})
                if not _missing(st, it):
                    it["status"] = "signed"
                fields = {"item": it["id"], "step": ev["step"]}
            else:
                it.setdefault("notes", []).append({"at": opskit.iso(), "by": ev["by"], "body": ev["body"]})
                fields = {"item": it["id"]}
            _touch(it)
        elif ev["kind"] == "burn":
            acc = (st.get("accounts") or {}).get(ev["account"])
            line = next((l for l in (acc or {}).get("lines", []) if l["id"] == ev["line"]), None)
            if line is None or line.get("status") != "active":
                ev["done"] = True
                continue
            _settle(acc)
            line["burn"] = ev["burn"]
            fields = {"account": ev["account"], "line": ev["line"], "burn": ev["burn"]}
        ev["done"] = True
        _save(st)
        os.environ["OPSKIT_IDENTITY"] = json.dumps({"user": ev["by"]})
        os.environ["OPSKIT_CLIENT_HOST"] = ev.get("host", "")
        opskit.audit(PROG, {"burn": "pacing"}.get(ev["kind"], ev["kind"]), **fields)
    # events skipped above (item gone, step already signed) stay in memory as done and are only written
    # together with a later event's audited save — a skip on its own never touches the state


# ── command line ────────────────────────────────────────────────────────────────────────────
def main(argv=None):
    if os.environ.get("OPSKIT_TICK") == "1":
        tick()
        return 0
    st = _state()
    it, its = V(st, "item", "item"), V(st, "items", "items")
    act = V(st, "action", "release")
    p = argparse.ArgumentParser(prog=PROG, description=V(st, "description", f"{its.capitalize()} and their {W(st)}."))
    sub = p.add_subparsers(dest="cmd", required=True, metavar="<command>")
    s = sub.add_parser("list", help=f"{its} in the queue")
    s.add_argument("--status", help=f"only {its} with this status (awaiting_signoff, signed, {V(st, 'action_past', 'done')}, draft, cancelled)")
    s.add_argument("--limit", type=int, default=15); s.add_argument("--all", action="store_true", help="include older ones")
    s.set_defaults(fn=cmd_list)
    s = sub.add_parser("show", help=f"one {it}: details, {W(st)}, notes"); s.add_argument("id")
    if st.get("columns"):
        s.add_argument("--lines", action="store_true", help=f"list every {V(st, 'line', 'line')}")
    s.set_defaults(fn=cmd_show, lines=False)
    if st.get("columns"):
        s = sub.add_parser(V(st, "lines_cmd", "lines"), help=f"{V(st, 'lines', 'lines')} in {'an' if it[0] in 'aeiou' else 'a'} {it}")
        s.add_argument("id"); s.add_argument("--csv", action="store_true"); s.set_defaults(fn=cmd_lines)
    s = sub.add_parser("status", help=f"{W(st, False)} status of {'an' if it[0] in 'aeiou' else 'a'} {it}"); s.add_argument("id"); s.set_defaults(fn=cmd_status)
    s = sub.add_parser("signers", help="who can sign each step"); s.add_argument("id", nargs="?"); s.set_defaults(fn=cmd_signers)
    if any(i.get("checks") for i in st["items"]):
        s = sub.add_parser(V(st, "check_cmd", "check"), help=V(st, "check_help", f"run the checks on {'an' if it[0] in 'aeiou' else 'a'} {it}"))
        s.add_argument("id"); s.add_argument("-o", "--output", help="also write the report to this file (markdown)"); s.set_defaults(fn=cmd_check)
    # request-signoff, which sends a request to a signer (and its automatic reply), is closed; cmd_request stays in the code but is not a command
    s = sub.add_parser("sign", help=f"record your own {W(st, False)} on {'an' if it[0] in 'aeiou' else 'a'} {it}")
    s.add_argument("id"); s.add_argument("--step"); s.add_argument("--note"); s.set_defaults(fn=cmd_sign)
    s = sub.add_parser("note", help=f"add a note to {'an' if it[0] in 'aeiou' else 'a'} {it}"); s.add_argument("id"); s.add_argument("text", nargs="+"); s.set_defaults(fn=cmd_note)
    s = sub.add_parser(act, help=V(st, "action_help", f"{act} a signed {it}"))
    s.add_argument("id"); s.add_argument("--yes", action="store_true", help="skip the confirmation")
    if V(st, "override_flag", "override"):          # a team without an override path sets override_flag to ""
        s.add_argument(f"--{V(st, 'override_flag', 'override')}", dest="override", action="store_true", help=V(st, "override_help", f"go ahead with the {W(st)} on file"))
        s.add_argument("--reason", help=f"why --{V(st, 'override_flag', 'override')} is needed")
    s.set_defaults(fn=cmd_action, override=False, reason=None)
    if st.get("accounts"):
        s = sub.add_parser("accounts", help="balances and burn"); s.set_defaults(fn=cmd_accounts)
        s = sub.add_parser("account", help=f"one account and its {V(st, 'acct_lines', 'lines')}"); s.add_argument("name"); s.set_defaults(fn=cmd_account)
        s = sub.add_parser("pause", help=f"pause {V(st, 'acct_lines', 'lines')} on an account"); s.add_argument("name"); s.add_argument("lines", nargs="+"); s.set_defaults(fn=cmd_pause)
        s = sub.add_parser("resume", help=f"resume paused {V(st, 'acct_lines', 'lines')}"); s.add_argument("name"); s.add_argument("lines", nargs="+"); s.set_defaults(fn=cmd_resume)
        s = sub.add_parser("raise", help=f"raise a new {it} for an account"); s.add_argument("name"); s.add_argument("--amount", type=float, required=True)
        s.add_argument("--reason", required=True); s.set_defaults(fn=cmd_raise)
    if st.get("records"):
        s = sub.add_parser(V(st, "record_cmd", "record"), help=V(st, "record_help", "show a record"))
        s.add_argument("name"); key = next(iter(st["records"].values())).get("key", "id")
        s.add_argument(f"--{key}", dest="key"); s.add_argument("--all", action="store_true"); s.add_argument("--csv", action="store_true")
        s.set_defaults(fn=cmd_record)
        ed = st.get("record_edit")
        if ed:
            s = sub.add_parser(ed["cmd"], help=ed.get("help", f"correct one {ed['field']} on {ed['record']}"))
            s.add_argument("key", metavar=st["records"][ed["record"]].get("key", "id")); s.add_argument("value", metavar=ed["field"])
            s.add_argument("--reason", help="goes on the change log"); s.add_argument("--yes", action="store_true", help="skip the confirmation")
            s.set_defaults(fn=cmd_record_edit)
    s = sub.add_parser("history", help="recent activity"); s.add_argument("id", nargs="?"); s.add_argument("--limit", type=int, default=20); s.set_defaults(fn=cmd_history)
    a = p.parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    opskit.run(main)
