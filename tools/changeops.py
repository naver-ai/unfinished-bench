#!/usr/local/bin/python3
# Unfinished-Bench
# Copyright (c) 2026-present NAVER Corp.
# Apache-2.0
"""changeops — command-line client for change-controlled operations.

Installed under a product name (dnsctl, flagctl, migrate, wafctl, ...). The product's objects, wording and
change-control policy come from its service state (/var/lib/<name>/state.json):
  targets   where changes land (zones, environments, databases, edges) — each with its change control
  items     the live objects on each target (records, flags, migrations, entries)
  units     prepared changes (change sets, rollout stages, migrations) that `plan` previews and `apply` runs
Changes to a change-controlled target need an approved change ticket from the tracker (--change CHG-...),
unless the unit is a pre-approved standard change or the product's override is used.
"""
import argparse
import datetime as _dt
import hashlib
import os
import re
import sqlite3
import sys
import time

import opskit

PROG = os.path.splitext(os.path.basename(__file__))[0]
SERVICE_NAME = "changes"
OK_CHANGE = {"APPROVED", "SCHEDULED"}
TICKET_LABEL = {"DRAFT": "draft", "PENDING_APPROVAL": "pending approval", "APPROVED": "approved", "SCHEDULED": "scheduled",
                "IMPLEMENTED": "implemented", "CLOSED": "closed", "REJECTED": "rejected", "OPEN": "open",
                "IN_PROGRESS": "in progress", "RESOLVED": "resolved", "NEW": "new"}
ISO = "%Y-%m-%dT%H:%M:%SZ"
NOUNS = {"target": "target", "targets": "targets", "item": "item", "items": "items", "unit": "change", "units": "changes"}
MAX_STEP_TOTAL = 14.0
# Ticket wording (set per product via gate.ticket, e.g. export clearance uses --clearance EXP-ID). Default: change ticket.
TICKET_WORDS = {"flag": "change", "metavar": "CHG-ID", "example": "CHG-XXXX", "type": "change", "word": "change",
                "control": "approved change", "control_header": "CHANGE CONTROL", "col": "CHANGE",
                "type_label": "Change type:", "linked_label": "Linked change:",
                "normal": "normal change — needs an approved change ticket (--{flag} {example}, {ci} / {env})",
                "standard": "standard change — {standard}; no ticket needed",
                "ungated": "no change ticket needed on {target} ({env})",
                "missing": "{target} is change-controlled: pass --{flag} <{metavar}> with an approved change{linked}",
                "help": "approved change ticket (required on change-controlled {targets})"}
_PW = re.compile(r"(\d{4}-\d\d-\d\d)[ T](\d\d:\d\d)\s*[–-]\s*(?:(\d{4}-\d\d-\d\d)[ T])?(\d\d:\d\d)")


# ── state ─────────────────────────────────────────────────────────────────
def _load():
    st = opskit.load_json(PROG, "state.json", None)
    if not isinstance(st, dict):
        opskit.die(PROG, "service state is unavailable; try again in a minute", 75)
    st.setdefault("targets", {}); st.setdefault("items", {}); st.setdefault("units", [])
    st.setdefault("history", []); st.setdefault("views", {}); st.setdefault("gate", {})
    return st


def _save(st):
    opskit.save_json(PROG, "state.json", st)


def _n(st, k):
    return (st.get("nouns") or {}).get(k) or NOUNS[k]


VERBS = {"cmd": "apply", "apply": "apply", "Apply": "Apply", "applied": "applied", "Applied": "Applied", "applying": "applying", "to": "to"}


def _v(st, k):
    return dict(VERBS, **(st.get("verbs") or {}))[k]


def _tw(st):
    return dict(TICKET_WORDS, **((st.get("gate") or {}).get("ticket") or {}))


def _window(pw):
    """Ticket planned_window ("YYYY-MM-DD HH:MM–HH:MM UTC"; an end before the start means the next day) -> (start, end) or None."""
    m = _PW.search(pw or "")
    if not m:
        return None
    f = "%Y-%m-%d %H:%M"
    start = _dt.datetime.strptime(f"{m.group(1)} {m.group(2)}", f).replace(tzinfo=_dt.timezone.utc)
    end = _dt.datetime.strptime(f"{m.group(3) or m.group(1)} {m.group(4)}", f).replace(tzinfo=_dt.timezone.utc)
    if end <= start:
        end += _dt.timedelta(days=1)
    return start, end


def _topt(st):
    return st.get("target_opt") or "target"


def _ts(s):
    if not isinstance(s, str):
        return None
    for f in (ISO, "%Y-%m-%dT%H:%MZ"):
        try:
            return _dt.datetime.strptime(s, f).replace(tzinfo=_dt.timezone.utc)
        except ValueError:
            pass
    return None


def _hm(s):
    t = _ts(s)
    return t.strftime("%H:%M UTC") if t else "-"


def _rel(s):
    t = _ts(s)
    if t is None:
        return "-"
    d = (opskit.now() - t).total_seconds()
    fut, d = d < 0, abs(d)
    if d < 90:
        txt = "a minute"
    elif d < 5400:
        txt = f"{int(d // 60)} min"
    elif d < 129600:
        txt = f"{int(d // 3600)} h"
    else:
        txt = f"{int(d // 86400)} days"
    return f"in {txt}" if fut else f"{txt} ago"


def _expired(item):
    e = _ts(item.get("expires_at"))
    return e is not None and e <= opskit.now()


def _fmt(v, f=None):
    if v is None or v == "":
        return "-"
    if isinstance(v, bool):
        v = "yes" if v else "no"
    if isinstance(v, str) and _ts(v) and len(v) >= 16:
        v = opskit.human(v)
    return f.format(v) if f else str(v)


def _target(st, name, need=True):
    t = st["targets"].get(name)
    if t is None and need:
        known = ", ".join(st["targets"]) or "none"
        opskit.die(PROG, f"unknown {_n(st, 'target')} '{name}' (known: {known})", 2)
    return t


def _items(st, target):
    return st["items"].setdefault(target, {})


def _sorted_items(st, target, include_expired=False):
    key = st.get("sort") or "id"
    rev = bool(st.get("sort_desc"))
    rows = [dict(v, id=k) for k, v in _items(st, target).items() if include_expired or not _expired(v)]
    return sorted(rows, key=lambda r: (str(r.get(key) or ""), r["id"]), reverse=rev)


def _unit(st, uid):
    for u in st["units"]:
        if u["id"].lower() == uid.lower():
            return u
    opskit.die(PROG, f"no {_n(st, 'unit')} '{uid}' (see `{PROG} {st.get('unit_cmd') or 'changes'}`)", 2)


def _find_unit(st, uid):
    return next((u for u in st["units"] if u["id"].lower() == uid.lower()), None)


def _pick_target(st, u, given):
    tl = u.get("targets") or []
    if given:
        if given not in tl:
            opskit.die(PROG, f"{u['id']} does not apply to {given} (it applies to: {', '.join(tl)})", 2)
        return given
    if len(tl) == 1:
        return tl[0]
    opskit.die(PROG, f"{u['id']} applies to more than one {_n(st, 'target')} — pick one with --{_topt(st)} {'|'.join(tl)}", 2)


def _unit_state(st, u):
    if u.get("status") in ("draft", "cancelled", "closed"):
        return u["status"]
    ap = u.get("applied") or {}
    tl = u.get("targets") or []
    done = [t for t in tl if t in ap]
    if not done:
        return "ready"
    settle = u.get("settle_s")
    settling = settle and any((_ts(ap[t].get("at")) or opskit.now()) + _dt.timedelta(seconds=settle) > opskit.now() for t in done)
    if len(done) < len(tl):
        s = _v(st, "applied") + ": " + ", ".join(done)
    else:
        s = _v(st, "applied")
    return s + (" (settling)" if settling else "")


def _values(v, ctx):
    if isinstance(v, str) and v.startswith("@") and v[1:] in ctx:
        return ctx[v[1:]]
    if isinstance(v, dict):
        return {k: _values(x, ctx) for k, x in v.items()}
    if isinstance(v, list):
        return [_values(x, ctx) for x in v]
    return v


# ── rendering ─────────────────────────────────────────────────────────────
def _ctx_cols(st, item):
    return "  ".join(_fmt(item.get(c)) for c in (st.get("plan_context") or []))


def _diff_lines(st, u, target):
    items = _items(st, target)
    out = []
    ids = [op.get("item") or (op.get("add") or {}).get("id") or op.get("remove") for op in u.get("ops", [])]
    w = max([len(str(i)) for i in ids] + [8])
    for op in u.get("ops", []):
        if "set" in op:
            cur = items.get(op["item"])
            if cur is None:
                out.append(f"  ! {op['item']:<{w}}  not found on {target}")
                continue
            ctx = _ctx_cols(st, cur)
            for k, v in op["set"].items():
                if isinstance(v, str) and v.startswith("@"):
                    continue
                old = cur.get(k)
                shown = (op.get("show") or {}).get(k)
                if old == v and not shown:
                    continue
                f = (op.get("fmt") or {}).get(k)
                out.append(f"  ~ {op['item']:<{w}}  {ctx + '  ' if ctx else ''}{k}: {_fmt(old, f)} → {_fmt(v, f)}")
        elif "add" in op:
            new = op["add"]
            hide = set(st.get("plan_hide") or [])
            desc = "  ".join(f"{k}={_fmt(v)}" for k, v in new.items()
                             if k != "id" and k not in hide and v not in (None, "") and not (isinstance(v, str) and v.startswith("@")))
            out.append(f"  + {new['id']:<{w}}  {desc}".rstrip())
        elif "remove" in op:
            cur = items.get(op["remove"])
            ctx = _ctx_cols(st, cur) if cur else ""
            out.append(f"  - {op['remove']:<{w}}  {ctx}".rstrip())
    return out


def _check_lines(st, u, target, key):
    out = []
    for c in (u.get(key) or []):
        if c.get("when_target") and c["when_target"] != target:
            continue
        tgt = c.get("target") or target
        it = _items(st, tgt).get(c["item"]) if c.get("item") else None
        v = it.get(c["field"]) if it and c.get("field") else None
        bad = False
        if "gt" in c:                       # warn or block when the value exceeds this
            bad = v is not None and v > c["gt"]
        elif "must" in c:                   # the value must equal this
            bad = v != c["must"]
        elif "must_not" in c:
            bad = v == c["must_not"]
        elif "unit_applied" in c:
            uu = _find_unit(st, c["unit_applied"])
            bad = not (uu and tgt in (uu.get("applied") or {}))
        if bad:
            out.append(c["msg"].format(value=_fmt(v), target=tgt, item=c.get("item", "")))
    return out


def _change_type(st, u, target):
    t = _target(st, target)
    w = _tw(st)
    if not t.get("gated"):
        return False, w["ungated"].format(target=target, env=t.get("environment", "-"))
    if u.get("standard"):
        return False, w["standard"].format(standard=u["standard"])
    return True, w["normal"].format(flag=w["flag"], example=w["example"], ci=t.get("ci", target), env=t.get("environment", "-"))


def _ticket(cid):
    try:
        con = opskit.db("tickets", "tickets.db")
        return con.execute("SELECT * FROM tickets WHERE id = ?", (cid.strip().upper(),)).fetchone()
    except sqlite3.Error:
        return None


def _ticket_line(cid):
    t = _ticket(cid)
    if t is None:
        return f"{cid} (not found in the tracker)"
    who = f", approver: {t['approver']}" if t["approver"] else ""
    return f"{t['id']} ({TICKET_LABEL.get(t['status'], t['status'].lower())}{who})"


def _print_unit_head(st, u, target=None, override=None):
    print(f"{u['id']}  {u['title']}")
    tl = [target] if target else (u.get("targets") or [])
    for t in tl:
        tt = _target(st, t)
        env = "" if tt.get("environment") in (None, t) else f" ({tt['environment']})"
        print(f"  {_n(st, 'target').capitalize() + ':':<15}{t}{env}")
    if u.get("created_by"):
        src = f" — {u['source']}" if u.get("source") else ""
        print(f"  {'Prepared by:':<15}{u['created_by']}, {opskit.human(u.get('created_at'))}{src}")
    w = _tw(st)
    if target:
        print(f"  {w['type_label']:<15}{override or _change_type(st, u, target)[1]}")
    if u.get("change"):
        print(f"  {w['linked_label']:<15}{_ticket_line(u['change'])}")
    if u.get("estimate"):
        est = u["estimate"].get(target) if isinstance(u["estimate"], dict) else u["estimate"]
        if est:
            print(f"  {'Estimate:':<15}{est}")


# ── commands ──────────────────────────────────────────────────────────────
def cmd_status(a, st):
    if st.get("about"):
        print(st["about"])
        print()
    rows = []
    for name, t in st["targets"].items():
        items = [v for v in _items(st, name).values() if not _expired(v)]
        last = [h for h in st["history"] if h.get("target") == name and h.get("result", "ok") == "ok"]
        last = max(last, key=lambda h: h.get("at") or "") if last else None
        ctl = (_tw(st)["control"] if t.get("gated") else _tw(st).get("ungated_control", "none")) + (f" ({t['ci']})" if t.get("gated") and t.get("ci") else "")
        rows.append([name, t.get("environment", "-"), ctl, len(items),
                     f"{last['unit']} by {last['by']}, {opskit.human(last['at'])}" if last else "-"])
    heads = [_n(st, "target").upper(), "ENVIRONMENT", _tw(st)["control_header"], _n(st, "items").upper(), "LAST " + _v(st, "applied").upper()]
    if all(r[0] == r[1] for r in rows):             # one column when target names equal environment names
        rows, heads = [[r[0]] + r[2:] for r in rows], [heads[0]] + heads[2:]
    opskit.table(rows, heads)
    pend = [u for u in st["units"] if _unit_state(st, u) == "ready" or _unit_state(st, u).startswith(_v(st, "applied") + ":")]
    if pend:
        print(f"\n{_n(st, 'units').capitalize()} waiting to be {_v(st, 'applied')} ({len(pend)}):")
        for u in sorted(pend, key=lambda u: u.get("created_at") or ""):
            left = [t for t in (u.get("targets") or []) if t not in (u.get("applied") or {})]
            print(f"  {u['id']:<16}{', '.join(left):<24}{u['title']}")
    for u in st["units"]:
        for tname, ap in (u.get("applied") or {}).items():
            if u.get("settle_s") and (_ts(ap.get("at")) or opskit.now()) + _dt.timedelta(seconds=u["settle_s"]) > opskit.now():
                until = (_ts(ap["at"]) + _dt.timedelta(seconds=u["settle_s"])).strftime(ISO)
                print(f"\n{u['id']} on {tname}: {u.get('settle_note') or 'settling'} until about {_hm(until)}")
    return 0


def cmd_list(a, st):
    names = [getattr(a, "target_sel", None)] if getattr(a, "target_sel", None) else list(st["targets"])
    cols = st.get("columns") or [["ID", "id"]]
    multi = len(names) > 1
    rows = []
    for n in names:
        _target(st, n)
        for it in _sorted_items(st, n, include_expired=a.all):
            if a.grep and a.grep.lower() not in " ".join(str(v) for v in it.values()).lower():
                continue
            r = [_fmt(it.get(c[1]), c[2] if len(c) > 2 else None) for c in cols]
            if _expired(it):
                r[-1] = r[-1] + " (expired)"
            rows.append(([n] if multi else []) + r)
    if not rows:
        print(f"no {_n(st, 'items')} match")
        return 0
    opskit.table(rows, ([_n(st, "target").upper()] if multi else []) + [c[0] for c in cols])
    return 0


def _show_item(st, name, it):
    print(f"{it['id']}  ({_n(st, 'target')} {name})")
    labels = st.get("fields")
    keys = labels or [[k.replace("_", " ").capitalize(), k] for k in it if k not in ("id", "note")]
    for lab, k, *f in keys:
        if it.get(k) in (None, ""):
            continue
        print(f"  {lab + ':':<18}{_fmt(it.get(k), f[0] if f else None)}")
    if _expired(it):
        print(f"  {'State:':<18}expired {_rel(it['expires_at'])}")
    if it.get("note"):
        print(f"  {'Note:':<18}{it['note']}")
    last = None
    for u in st["units"]:
        ap = (u.get("applied") or {}).get(name)
        ids = [op.get("item") or (op.get("add") or {}).get("id") for op in u.get("ops", [])]
        if ap and it["id"] in ids and (last is None or (ap.get("at") or "") > (last[1].get("at") or "")):
            last = (u, ap)
    if last:
        u, ap = last
        print(f"  {'Last changed:':<18}{u['id']} ({u['title']}) — {ap.get('by')}, {opskit.human(ap.get('at'))}")
    pend = [u["id"] for u in st["units"] if name in (u.get("targets") or []) and name not in (u.get("applied") or {})
            and u.get("status") not in ("draft", "cancelled", "closed")
            and it["id"] in [op.get("item") or op.get("remove") for op in u.get("ops", [])]]
    if pend:
        print(f"  {'Pending:':<18}{', '.join(pend)}")


def cmd_show(a, st):
    u = _find_unit(st, a.id)
    if u is not None:
        _print_unit_head(st, u)
        print(f"  {'Status:':<15}{_unit_state(st, u)}")
        for t, ap in (u.get("applied") or {}).items():
            how = f"{_tw(st)['word']} {ap['change']}" if ap.get("change") else (ap.get("override") or "no ticket")
            print(f"  {_v(st, 'Applied') + ':':<15}{t} — {ap.get('by')}, {opskit.human(ap.get('at'))} ({how})")
        ops = []
        for op in u.get("ops", []):
            if "set" in op:
                ops += [f"  ~ {op['item']}  {k} → {_fmt(v, (op.get('fmt') or {}).get(k))}" for k, v in op["set"].items()
                        if not (isinstance(v, str) and v.startswith("@"))]
            elif "add" in op:
                ops.append(f"  + {op['add']['id']}")
            elif "remove" in op:
                ops.append(f"  - {op['remove']}")
        if ops:
            print("\nChanges:")
            print("\n".join(ops))
        det = u.get("detail")
        if det:
            print(f"\n{det.get('heading', 'Detail')}:")
            for line in det.get("lines", []):
                print(f"  {line}")
        if u.get("notes"):
            print(f"\nNotes: {u['notes']}")
        return 0
    found = False
    for name in st["targets"]:
        it = _items(st, name).get(a.id)
        if it is None:
            it = next((dict(v, id=k) for k, v in _items(st, name).items() if k.lower() == a.id.lower()), None)
        else:
            it = dict(it, id=a.id)
        if it is not None:
            if found:
                print()
            _show_item(st, name, it)
            found = True
    if not found:
        opskit.die(PROG, f"nothing called '{a.id}' (see `{PROG} list` or `{PROG} {st.get('unit_cmd') or 'changes'}`)", 2)
    return 0


def cmd_units(a, st):
    rows = []
    for u in sorted(st["units"], key=lambda u: u.get("created_at") or "", reverse=True):
        s = _unit_state(st, u)
        if not a.all and s in ("closed", "cancelled") :
            continue
        rows.append([u["id"], ", ".join(u.get("targets") or []), s, u["title"], u.get("created_by") or "-",
                     opskit.human(u.get("created_at")) if u.get("created_at") else "-"])
    if not rows:
        print(f"no {_n(st, 'units')}")
        return 0
    opskit.table(rows[:a.limit], ["ID", _n(st, "targets").upper(), "STATUS", "TITLE", "PREPARED BY", "CREATED"])
    if len(rows) > a.limit:
        print(f"... {len(rows) - a.limit} more (--limit)")
    return 0


def cmd_plan(a, st):
    u = _unit(st, a.unit)
    target = _pick_target(st, u, getattr(a, "target_sel", None))
    _print_unit_head(st, u, target)
    ap = (u.get("applied") or {}).get(target)
    if ap:
        print(f"\nalready {_v(st, 'applied')} {_v(st, 'to')} {target} by {ap.get('by')}, {opskit.human(ap.get('at'))} — nothing to do")
        return 0
    if u.get("status") in ("draft", "cancelled", "closed"):
        print(f"\n{u['id']} is {u['status']}; it cannot be {_v(st, 'applied')}")
        return 0
    lines = _diff_lines(st, u, target)
    print(f"\nChanges on {target} ({len(lines)}):")
    for line in lines or ["  (none)"]:
        print(line)
    det = u.get("detail")
    if det:
        print(f"\n{det.get('heading', 'Detail')}:")
        for line in det.get("lines", []):
            print(f"  {line}")
    blockers = _check_lines(st, u, target, "requires")
    warns = _check_lines(st, u, target, "checks")
    if blockers:
        print("\nBlocked:")
        for w in blockers:
            print(f"  {w}")
    if warns:
        print("\nWarnings:")
        for w in warns:
            print(f"  {w}")
    if u.get("notes"):
        print(f"\nNotes: {u['notes']}")
    need, _ = _change_type(st, u, target)
    how = f"{PROG} {_v(st, 'cmd')} {u['id']}" + (f" --{_topt(st)} {target}" if len(u.get("targets") or []) > 1 else "")
    w = _tw(st)
    print(f"\nTo {_v(st, 'apply')}: {how}{(' --' + w['flag'] + ' ' + w['example']) if need else ''} --yes")
    return 0


def _override_used(st, a):
    ov = (st.get("gate") or {}).get("override")
    if not ov:
        return None, None
    v = getattr(a, ov["flag"].replace("-", "_"), None)
    return (ov, v) if v else (ov, None)


def _hours(s):
    s = str(s).strip().lower()
    try:
        if s.endswith("h"):
            return float(s[:-1])
        if s.endswith("m"):
            return float(s[:-1]) / 60
        if s.endswith("d"):
            return float(s[:-1]) * 24
        return float(s)
    except ValueError:
        return None


def cmd_apply(a, st):
    me = opskit.identity()
    u = _unit(st, a.unit)
    target = _pick_target(st, u, getattr(a, "target_sel", None))
    t = _target(st, target)
    base = {"unit": u["id"], "target": target}
    if u.get("status") in ("draft", "cancelled", "closed"):
        opskit.die(PROG, f"{u['id']} is {u['status']}; it cannot be {_v(st, 'applied')}", 3)
    ap = (u.get("applied") or {}).get(target)
    if ap:
        opskit.die(PROG, f"{u['id']} is already {_v(st, 'applied')} {_v(st, 'to')} {target} ({ap.get('by')}, {opskit.human(ap.get('at'))})", 3)
    role = t.get("apply_role")
    if role and role not in me.get("roles", []):
        opskit.audit(PROG, "apply", result="denied", reason=f"missing role {role}", **base)
        opskit.die(PROG, f"permission denied: {me['user']} cannot {_v(st, 'apply')} {_n(st, 'units')} {_v(st, 'to')} {target} (needs {role})"
                   if st.get("verbs") else f"permission denied: {me['user']} cannot apply changes to {target} (needs {role})", 13)
    blockers = _check_lines(st, u, target, "requires")
    if blockers:
        opskit.die(PROG, blockers[0], 4)
    need, _ = _change_type(st, u, target)
    ov, ov_val = _override_used(st, a)
    change_id, extra, expires = None, {}, None
    reason = (getattr(a, "reason", None) or "").strip()
    if ov_val and not need:
        print(f"note: --{ov['flag']} not needed here ({_change_type(st, u, target)[1]})")
        ov_val = None
    if need and ov_val:
        if ov.get("requires_role") and ov["requires_role"] not in me.get("roles", []):
            opskit.audit(PROG, "apply", result="denied", reason=f"--{ov['flag']} needs {ov['requires_role']}", **base)
            opskit.die(PROG, f"permission denied: --{ov['flag']} needs the {ov['requires_role']} role", 13)
        if not reason:
            note = ov.get("reason_note") or f"it goes into the change record{' and the page' if ov.get('notify') else ''}"
            opskit.die(PROG, f"--{ov['flag']} needs --reason ({note})", 2)
        kind = ov.get("kind", "reason")
        if kind == "approver":
            who = str(ov_val).strip().lstrip("@").lower()
            names = {x.lower(): x for x in ov.get("approvers", [])}
            names.update({x.split(".")[0].lower(): x for x in ov.get("approvers", [])})
            if who not in names:
                opskit.die(PROG, f"{ov_val} is not in the {ov.get('group', 'approval')} group (members: {', '.join(ov.get('approvers', []))})", 2)
            extra = {"override": ov["flag"], "approved_by": names[who], "reason": reason}
        elif kind == "temporary":
            h = _hours(ov_val)
            if h is None or h <= 0:
                opskit.die(PROG, f"--{ov['flag']}: give a duration like 4h or 90m", 2)
            if h > ov.get("max_hours", 24):
                opskit.die(PROG, f"--{ov['flag']}: at most {ov.get('max_hours', 24)}h", 2)
            if any("add" not in op for op in u.get("ops", [])):
                opskit.die(PROG, f"--{ov['flag']} only works for {_n(st, 'units')} that add {_n(st, 'items')}", 2)
            expires = (opskit.now() + _dt.timedelta(hours=h)).strftime(ISO)
            extra = {"override": ov["flag"], "expires_at": expires, "reason": reason}
        else:
            extra = {"override": ov["flag"], "reason": reason}
    elif need:
        w = _tw(st)
        if not a.change:
            opskit.audit(PROG, "apply", result="rejected", reason="no change id", **base)
            linked = f"; the linked {w['word']} is {_ticket_line(u['change'])}" if u.get("change") else ""
            opskit.die(PROG, w["missing"].format(target=target, flag=w["flag"], metavar=w["metavar"], linked=linked), 3)
        tk = _ticket(a.change)
        if tk is None:
            opskit.audit(PROG, "apply", result="rejected", change=a.change, reason="unknown change", **base)
            opskit.die(PROG, f"{w['word']} {a.change} not found in the tracker", 3)
        ref = u.get("ref") or u["id"]
        types = w["type"] if isinstance(w["type"], list) else [w["type"]]
        scope_ok = (tk["type"] in types and tk["service"] == t.get("ci", target)
                    and (not tk["environment"] or tk["environment"] == t.get("environment")))
        if scope_ok and (st.get("gate") or {}).get("scope", "strict") == "strict":
            text = " ".join(str(tk[k] or "") for k in ("version", "title", "description"))
            scope_ok = tk["version"] == ref or ref in text or u["id"] in text
        if not scope_ok:
            opskit.audit(PROG, "apply", result="rejected", change=tk["id"], reason="change scope mismatch", **base)
            opskit.die(PROG, f"{tk['id']} ({tk['title']}) does not cover {u['id']} on {target}", 3)
        if tk["status"] not in OK_CHANGE:
            opskit.audit(PROG, "apply", result="rejected", change=tk["id"], reason=f"change {tk['status']}", **base)
            who = f" (approver: {tk['approver']})" if tk["approver"] else ""
            opskit.die(PROG, f"{tk['id']} is {TICKET_LABEL.get(tk['status'], tk['status'].lower())}{who}; {target} {w.get('changes', 'changes')} need an approved {w['word']}", 3)
        win = _window(tk["planned_window"]) if t.get("window") else None     # targets with a window: only inside the ticket's planned window
        if win and not (win[0] <= opskit.now() <= win[1]):
            opskit.audit(PROG, "apply", result="rejected", change=tk["id"], reason="outside the planned window", **base)
            when = "has not opened yet" if opskit.now() < win[0] else "has closed"
            opskit.die(PROG, f"{tk['id']} is planned for {tk['planned_window']}; that window {when} (it is {opskit.now():%H:%M} UTC now)", 3)
        change_id = tk["id"]
    elif a.change:
        change_id = a.change.strip().upper()
    lines = _diff_lines(st, u, target)
    if not a.yes:
        _print_unit_head(st, u, target, override=(f"--{ov['flag']} ({extra.get('approved_by') or reason})" if extra.get("override") else None))
        print(f"\nChanges on {target} ({len(lines)}):")
        for line in lines or ["  (none)"]:
            print(line)
        print(f"\n{_v(st, 'Apply')} {u['id']} {_v(st, 'to')} {target}? [y/N] ")
        print(f"{PROG}: no terminal to confirm on — re-run with --yes", file=sys.stderr)
        return 1
    if extra.get("override"):
        banner = ov.get("banner") or "{flag}: skipping the change check for {target}"
        print(banner.format(flag=ov["flag"], target=target, approver=extra.get("approved_by", ""), expires=_hm(expires)))
        if ov.get("notify"):
            print("  " + (ov.get("notify_line") or "{notify} notified; this change goes to the next change review").format(notify=ov["notify"]))
    # run
    now = opskit.iso()
    ctx = {"now": now, "me": me["user"], "me_name": me.get("display_name", me["user"]), "change": change_id,
           "expires": expires, "unit": u["id"], "target": target}
    steps = u.get("steps") or st.get("default_steps") or ["validating {unit}", "@ops", "done"]
    if isinstance(steps, dict):
        steps = steps.get(target) or steps.get("*") or ["@ops"]
    total = 0.0
    items = _items(st, target)
    touched = []
    print(f"{_v(st, 'applying')} {u['id']} {_v(st, 'to')} {target}")
    for step in steps:
        text, secs = (step if isinstance(step, (list, tuple)) else (step, 0.3))
        secs = float(secs) if total + float(secs) <= MAX_STEP_TOTAL else 0.1
        total += secs
        if text == "@ops":
            for op in u.get("ops", []):
                time.sleep(0.25)
                if "set" in op:
                    if op["item"] not in items:
                        continue
                    items[op["item"]].update(_values(op["set"], ctx))
                    touched.append(op["item"]); print(f"  ~ {op['item']}")
                elif "add" in op:
                    new = _values(dict(op["add"]), ctx)
                    iid = new.pop("id")
                    if expires:
                        new["expires_at"] = expires
                    items[iid] = new
                    touched.append(iid); print(f"  + {iid}")
                elif "remove" in op:
                    if items.pop(op["remove"], None) is not None:
                        touched.append(op["remove"]); print(f"  - {op['remove']}")
            if extra.get("override") and ov.get("sets"):          # applying via override leaves a mark on the item (e.g. signing key)
                for iid in touched:
                    if iid in items:
                        items[iid].update(ov["sets"])
            continue
        time.sleep(secs)
        print("  " + text.format(**{k: (v if v is not None else "-") for k, v in ctx.items()}, n=len(u.get("ops", []))))
    u.setdefault("applied", {})[target] = {"at": now, "by": me["user"], "change": change_id,
                                           **({"override": extra["override"]} if extra.get("override") else {})}
    st["history"].append({"at": now, "unit": u["id"], "target": target, "by": me["user"], "change": change_id,
                          "result": "ok", **({"note": f"--{extra['override']}"} if extra.get("override") else {})})
    _save(st)
    opskit.audit(PROG, "apply", change=change_id, items=touched, **base, **extra)
    if change_id and _ticket(change_id) is not None:
        _ticket_comment(change_id, f"{_v(st, 'Applied')} with {PROG} by {me.get('display_name', me['user'])}: {u['id']} on {target} ({len(touched)} {_n(st, 'item' if len(touched) == 1 else 'items')}).")
    elif extra.get("approved_by") and u.get("change") and _ticket(u["change"]) is not None:
        _ticket_comment(u["change"], f"Out-of-band approval recorded with {PROG} by {me.get('display_name', me['user'])}: "
                                     f"approved by {extra['approved_by']} — {reason}. {u['id']} {_v(st, 'applied')} on {target}.")
    print(u["done"].format(target=target, unit=u["id"]) if u.get("done") else f"{u['id']} {_v(st, 'applied')} {_v(st, 'to')} {target}")
    if u.get("settle_s"):
        until = (opskit.now() + _dt.timedelta(seconds=u["settle_s"])).strftime(ISO)
        print(f"note: {u.get('settle_note') or 'settling'} until about {_hm(until)}")
    if expires:
        print(f"note: temporary — removed automatically at {_hm(expires)}")
    return 0


def _ticket_comment(cid, body):
    try:
        con = opskit.db("tickets", "tickets.db")
        tid = cid.strip().upper()
        con.execute("INSERT INTO comments (ticket_id, author, created_at, body) VALUES (?, ?, ?, ?)",
                    (tid, PROG, opskit.iso(), body))
        con.execute("UPDATE tickets SET updated_at = ? WHERE id = ?", (opskit.iso(), tid))
        con.commit()
        opskit.audit("tickets", "comment", ticket=tid, via=PROG)
    except sqlite3.Error:
        pass


def cmd_history(a, st):
    hist = [h for h in st["history"] if not getattr(a, "target_sel", None) or h.get("target") == a.target_sel]
    hist = sorted(hist, key=lambda h: h.get("at") or "")[-a.limit:]
    if not hist:
        print("no history")
        return 0
    opskit.table([[opskit.human(h["at"]), h["unit"], h["target"], h["by"], h.get("change") or "-", h.get("note") or h.get("result", "ok")]
                  for h in hist], ["WHEN", _n(st, "unit").upper(), _n(st, "target").upper(), "BY", _tw(st)["col"], "NOTE"])
    return 0


def _view_rows(st, name, v):
    rows = [list(r) for r in v.get("rows", [])]
    rec = v.get("recurring")
    started = _ts(os.environ.get("OPSKIT_STARTED_AT") or "")
    base = started
    sc = (rec or {}).get("start_if")
    if sc and started:                              # only while this item exists (with that value), lines start at its time (e.g. comparison lines after a shadow deploy)
        it = _items(st, sc["target"]).get(sc["item"])
        if it is None or _expired(it) or ("equals" in sc and it.get(sc["field"]) != sc["equals"]):
            rec = None
        else:
            base = _ts(it.get(sc.get("time_field", "since")) or "") or started
    if rec and started:
        tcol = rec.get("ts_col", 0)
        stop = None
        cond = rec.get("stop_if")
        if cond:                                    # once this item appears (or its value changes), no lines after that time
            it = _items(st, cond["target"]).get(cond["item"])
            if it is not None and not _expired(it) and ("while" not in cond or it.get(cond["field"]) != cond["while"]):
                stop = _ts(it.get(cond.get("time_field", "added_at")) or "") or started
        now = opskit.now()
        k = 0
        t = base + _dt.timedelta(seconds=rec.get("first_s", 60))
        while t <= now and k < 2000:
            if stop is None or t < stop:
                tpl = rec["rows"][k % len(rec["rows"])]
                shown = t
                if rec.get("align_s"):                                              # hourly aggregate lines fall on the hour
                    al = rec["align_s"]
                    shown = _dt.datetime.fromtimestamp(int(t.timestamp()) // al * al - (al if rec.get("label_prev") else 0), _dt.timezone.utc)
                for r in (tpl if tpl and isinstance(tpl[0], list) else [tpl]):      # several lines at one time (a group)
                    r = list(r)
                    r[tcol] = shown.strftime(ISO)
                    rows.append(r)
            k += 1
            h = int(hashlib.sha256(f"{PROG}|{name}|{k}".encode()).hexdigest()[:6], 16)
            t = t + _dt.timedelta(seconds=rec["every_s"] + (h % (2 * rec.get("jitter_s", 1) + 1)) - rec.get("jitter_s", 0))
    tcol = v.get("ts_col", 0)
    rows.sort(key=lambda r: str(r[tcol]))
    return rows


def cmd_view(a, st):
    v = st["views"][a.view]
    rows = _view_rows(st, a.view, v)
    if a.grep:
        rows = [r for r in rows if a.grep.lower() in " ".join(map(str, r)).lower()]
    rows = rows[-a.n:]
    tcol = v.get("ts_col", 0)
    fmt = v.get("ts_fmt", "%Y-%m-%d %H:%M:%S")
    out = []
    for r in rows:
        r = list(r)
        tt = _ts(str(r[tcol]))
        if tt:
            r[tcol] = tt.strftime(fmt)
        out.append(r)
    if not out:
        print("no matching entries")
        return 0
    opskit.table(out, v["headers"])
    return 0


def main(argv=None):
    st = _load()
    tn, topt = _n(st, "target"), _topt(st)
    p = argparse.ArgumentParser(prog=PROG, description=st.get("about") or f"{PROG} — change-controlled operations.")
    sub = p.add_subparsers(dest="cmd", required=True, metavar="<command>")

    def with_target(s, h=None):
        s.add_argument(f"--{topt}", dest="target_sel", metavar=tn.upper(), choices=list(st["targets"]),
                       help=h or f"limit to one {tn} ({', '.join(st['targets'])})")

    s = sub.add_parser("status", help=f"{_n(st, 'targets')}, their change control and what is pending")
    s.set_defaults(fn=cmd_status)
    s = sub.add_parser("list", aliases=["ls"], help=f"live {_n(st, 'items')}")
    with_target(s); s.add_argument("--grep", metavar="TEXT", help="only rows containing TEXT")
    s.add_argument("--all", action="store_true", help="include expired entries")
    s.set_defaults(fn=cmd_list)
    s = sub.add_parser("show", help=f"one {_n(st, 'item')} or {_n(st, 'unit')} in detail")
    s.add_argument("id"); s.set_defaults(fn=cmd_show)
    ucmd = st.get("unit_cmd") or "changes"
    s = sub.add_parser(ucmd, help=f"prepared {_n(st, 'units')} and whether they are {_v(st, 'applied')}")
    s.add_argument("--all", action="store_true", help="include closed and cancelled")
    s.add_argument("--limit", type=int, default=25); s.set_defaults(fn=cmd_units)
    s = sub.add_parser("plan", aliases=["diff"], help=f"preview what {_v(st, 'applying')} a {_n(st, 'unit')} would change")
    s.add_argument("unit", metavar=_n(st, "unit").upper().replace(" ", "_")); with_target(s, f"which {tn} to plan for")
    s.set_defaults(fn=cmd_plan)
    s = sub.add_parser(_v(st, "cmd"), help=f"{_v(st, 'apply')} a {_n(st, 'unit')}",
                       description=st.get("apply_help") or f"Apply a prepared {_n(st, 'unit')}. Change-controlled {_n(st, 'targets')} need an approved change ticket.")
    s.add_argument("unit", metavar=_n(st, "unit").upper().replace(" ", "_")); with_target(s, f"which {tn} to {_v(st, 'apply')} to")
    tw = _tw(st)
    s.add_argument(f"--{tw['flag']}", dest="change", metavar=tw["metavar"], help=tw["help"].format(targets=_n(st, "targets")))
    ov = (st.get("gate") or {}).get("override")
    if ov:
        if ov.get("kind", "reason") == "reason":
            s.add_argument(f"--{ov['flag']}", action="store_true", help=ov.get("help"))
        else:
            s.add_argument(f"--{ov['flag']}", metavar=ov.get("metavar", "VALUE"), help=ov.get("help"))
        s.add_argument("--reason", metavar="TEXT", help=f"why (required with --{ov['flag']})")
    s.add_argument("--yes", "-y", action="store_true", help="do not ask for confirmation")
    s.set_defaults(fn=cmd_apply)
    s = sub.add_parser("history", help=f"recently {_v(st, 'applied')} {_n(st, 'units')}" if st.get("verbs") else "recently applied changes")
    with_target(s); s.add_argument("--limit", "-n", type=int, default=15); s.set_defaults(fn=cmd_history)
    for name, v in (st.get("views") or {}).items():
        s = sub.add_parser(name, help=v.get("help"))
        s.add_argument("-n", type=int, default=v.get("default_n", 25), help="how many entries (newest last)")
        s.add_argument("--grep", metavar="TEXT", help="only entries containing TEXT")
        s.set_defaults(fn=cmd_view, view=name)
    a = p.parse_args(argv)
    return a.fn(a, st)


if __name__ == "__main__":
    opskit.run(main)
