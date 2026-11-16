#!/usr/local/bin/python3
# Unfinished-Bench
# Copyright (c) 2026-present NAVER Corp.
# Apache-2.0
"""settings — command-line client for operational settings with owners and change control.

Installed under a product name (costctl, limitctl, ratectl, webcfg, ...). The product's wording, scopes and
settings come from its service state (/var/lib/<name>/settings.db):
  scopes     what settings belong to (a project, a merchant, an API client, a service), with context facts
  settings   typed values, each owned by a team; editing needs one of the setting's roles, and a
             change-controlled setting moves only with an approved change ticket from the tracker
             (--change CHG-...), or through the product's emergency path (--emergency, needs a reason)
  derived    figures computed from the settings (forecasts, capacity, latency) that status and previews show
Every change is recorded in the setting history and the audit log.
"""
import argparse
import datetime as _dt
import hashlib
import json
import math
import os
import random
import sqlite3
import sys
import time

import opskit

PROG = os.path.splitext(os.path.basename(__file__))[0]
SERVICE_NAME = "config"
DB = "settings.db"
OK_CHANGE = {"APPROVED", "SCHEDULED"}
TICKET_LABEL = {"DRAFT": "draft", "PENDING_APPROVAL": "pending approval", "APPROVED": "approved", "SCHEDULED": "scheduled",
                "IMPLEMENTED": "implemented", "CLOSED": "closed", "REJECTED": "rejected", "OPEN": "open",
                "IN_PROGRESS": "in progress", "RESOLVED": "resolved"}
ISO = "%Y-%m-%dT%H:%M:%SZ"
NUMERIC = ("int", "float", "money", "count", "seconds", "ms", "percent", "rate")
TRUE_WORDS = {"on", "true", "yes", "enabled", "enable", "1"}
FALSE_WORDS = {"off", "false", "no", "disabled", "disable", "0"}


# ── state ─────────────────────────────────────────────────────────────────
def _con():
    if not os.path.exists(os.path.join(opskit.STATE_ROOT, PROG, DB)):
        opskit.die(PROG, "service state is unavailable; try again in a minute", 75)
    return opskit.db(PROG, DB)


def _meta(con):
    r = con.execute("SELECT v FROM meta WHERE k = 'config'").fetchone()
    return json.loads(r[0]) if r else {}


def _j(x, default=None):
    if x is None or x == "":
        return default
    try:
        return json.loads(x)
    except (TypeError, ValueError):
        return default


def _enc(v):
    return json.dumps(v, sort_keys=True)


def _ts(s):
    if not isinstance(s, str):
        return None
    for f in (ISO, "%Y-%m-%dT%H:%MZ"):
        try:
            return _dt.datetime.strptime(s, f).replace(tzinfo=_dt.timezone.utc)
        except ValueError:
            pass
    return None


def _setting(row):
    s = dict(row)
    s["value"] = _j(row["value"])
    for k in ("choices", "edit_roles", "control", "words"):
        s[k] = _j(row[k])
    return s


def _scopes(con):
    return [dict(r) for r in con.execute("SELECT * FROM scopes ORDER BY pos, id")]


def _scope(con, meta, sid, need=True):
    r = con.execute("SELECT * FROM scopes WHERE id = ?", (sid,)).fetchone()
    if r is None:
        low = sid.lower()
        r = next((x for x in con.execute("SELECT * FROM scopes") if x["id"].lower() == low or x["id"].split("/")[-1].lower() == low), None)
    if r is None and need:
        noun = meta.get("scope_noun", "scope")
        known = ", ".join(x["id"] for x in con.execute("SELECT id FROM scopes ORDER BY pos, id"))
        opskit.die(PROG, f"unknown {noun} '{sid}' (known: {known})", 2)
    return dict(r) if r else None


def _settings(con, scope=None):
    q, a = "SELECT * FROM settings", []
    if scope:
        q += " WHERE scope = ?"; a.append(scope)
    q += " ORDER BY scope, pos, key"
    return [_setting(r) for r in con.execute(q, a)]


def _get(con, meta, scope, key):
    r = con.execute("SELECT * FROM settings WHERE scope = ? AND key = ?", (scope, key)).fetchone()
    if r is None:
        keys = ", ".join(x["key"] for x in con.execute("SELECT key FROM settings WHERE scope = ? ORDER BY pos, key", (scope,)))
        opskit.die(PROG, f"{scope} has no setting '{key}' (settings: {keys})", 2)
    return _setting(r)


# ── values ────────────────────────────────────────────────────────────────
def _num(x):
    return f"{x:,}" if isinstance(x, int) else (f"{x:,.2f}".rstrip("0").rstrip(".") if isinstance(x, float) else str(x))


def show_value(s, v):
    if v is None:
        return s.get("null_label") or "-"
    t = s["type"]
    unit = s.get("unit")
    if t == "bool":
        w = s.get("words") or ["off", "on"]
        return w[1] if v else w[0]
    if t == "list":
        suf = "%" if unit == "%" else ""
        return ", ".join(f"{x}{suf}" for x in v) if v else (s.get("null_label") or "(none)")
    if t == "percent":
        return f"{_num(v)}%"
    if t in NUMERIC:
        return _num(v) + (f" {unit}" if unit else "")
    return str(v)


def type_label(s):
    t = s["type"]
    if t == "enum":
        return "one of: " + ", ".join(str(c) for c in (s.get("choices") or []))
    if t == "bool":
        w = s.get("words") or ["off", "on"]
        return f"{w[1]} / {w[0]}"
    rng = ""
    if s.get("min") is not None or s.get("max") is not None:
        lo = _num(_intish(s["min"])) if s.get("min") is not None else ""
        hi = _num(_intish(s["max"])) if s.get("max") is not None else ""
        rng = f", {lo}–{hi}"
    base = {"money": "amount", "count": "count", "seconds": "duration", "ms": "duration", "percent": "percentage",
            "rate": "rate", "int": "integer", "float": "number", "list": "list (comma separated)", "str": "text"}.get(t, t)
    unit = f" ({s['unit']})" if s.get("unit") and t != "percent" else ""
    return f"{base}{unit}{rng}" + (f"; empty = {s['null_label']}" if s.get("null_label") and t in NUMERIC else "")


def _intish(x):
    return int(x) if isinstance(x, float) and x.is_integer() else x


def parse_value(s, raw):
    t = s["type"]
    txt = raw.strip()
    if t == "bool":
        w = [x.lower() for x in (s.get("words") or ["off", "on"])]
        lw = txt.lower()
        if lw in TRUE_WORDS or lw == w[1]:
            return True
        if lw in FALSE_WORDS or lw == w[0]:
            return False
        opskit.die(PROG, f"{s['key']}: expected {w[1]} or {w[0]}, got '{raw}'", 4)
    if t == "enum":
        for c in s.get("choices") or []:
            if str(c).lower() == txt.lower():
                return c
        opskit.die(PROG, f"{s['key']}: '{raw}' is not one of: {', '.join(map(str, s.get('choices') or []))}", 4)
    if t == "list":
        if txt.lower() in ("", "none", "[]", "-"):
            return []
        items = [x.strip() for x in txt.split(",") if x.strip()]
        if s.get("unit") == "%":                  # shown as "80%": "80%" and "80" are the same entry
            items = [x[:-1].rstrip() if x.endswith("%") and len(x) > 1 else x for x in items]
        return items
    if t in NUMERIC:
        if s.get("null_label") and txt.lower() in ("default", "none", "-", "", s["null_label"].lower()):
            return None
        x = txt.replace(",", "").replace("_", "")
        unit = (s.get("unit") or "").lower()
        low = x.lower()
        for suf in filter(None, (unit, "%", "usd", "ms", "s", "rps", "/s")):
            if low.endswith(suf) and len(low) > len(suf):
                x = x[: -len(suf)].strip(); low = x.lower()
                break
        mult = 1
        if low.endswith("k"):
            mult, x = 1000, x[:-1]
        try:
            f = float(x) * mult
        except ValueError:
            opskit.die(PROG, f"{s['key']}: expected a number, got '{raw}'", 4)
        if t == "float":
            v = round(f, 4)
        else:
            if not float(f).is_integer():
                opskit.die(PROG, f"{s['key']}: expected a whole number, got '{raw}'", 4)
            v = int(f)
        if s.get("min") is not None and v < s["min"]:
            opskit.die(PROG, f"{s['key']}: {show_value(s, v)} is below the allowed minimum ({show_value(s, _intish(s['min']))})", 4)
        if s.get("max") is not None and v > s["max"]:
            opskit.die(PROG, f"{s['key']}: {show_value(s, v)} is above the allowed maximum ({show_value(s, _intish(s['max']))})", 4)
        return v
    return txt


# ── derived figures ──────────────────────────────────────────────────────
class Model:
    """Evaluates the product's derived figures (meta.metrics / meta.checks) over the settings and scope facts."""

    def __init__(self, con, meta, overrides=None):
        self.meta = meta
        self.vals = {(r["scope"], r["key"]): _j(r["value"]) for r in con.execute("SELECT scope, key, value FROM settings")}
        self.vals.update(overrides or {})
        self.facts = {r["id"]: _j(r["facts"], {}) for r in con.execute("SELECT id, facts FROM scopes")}
        try:
            self.derived = {r["name"]: dict(r) for r in con.execute("SELECT * FROM derived")}
        except sqlite3.Error:
            self.derived = {}
        self.memo = {}
        self.now = opskit.now()
        self.g = {"__builtins__": {}, "v": self.v, "f": self.f, "m": self.m, "live": self.live, "wobble": self.wobble, "since_change": self.since_change,
                  "hours_until": self.hours_until, "hours_since": self.hours_since, "at_hours": self.at_hours,
                  "human": opskit.human, "dur": _dur, "num": _num, "pct": lambda a, b: (100.0 * a / b if b else 0.0),
                  "min": min, "max": max, "sum": sum, "abs": abs, "round": round, "ceil": math.ceil, "floor": math.floor,
                  "exp": math.exp, "len": len, "int": int, "float": float, "str": str, "any": any, "all": all, "sorted": sorted,
                  "True": True, "False": False, "None": None}

    def v(self, scope, key):
        return self.vals.get((scope, key))

    def f(self, scope, key, default=None):
        return self.facts.get(scope, {}).get(key, default)

    def m(self, name):
        if name not in self.memo:
            self.memo[name] = self.ev((self.meta.get("metrics") or {})[name])
        return self.memo[name]

    def ev(self, expr, **extra):
        g = dict(self.g, **extra) if extra else self.g
        return eval(expr, g)  # expressions come from the product's own service config

    def check(self, name):
        return bool(self.ev((self.meta.get("checks") or {})[name]))

    def all(self):
        out = {n: float(self.m(n)) for n in (self.meta.get("metrics") or {})}
        out.update({n: (1.0 if self.check(n) else 0.0) for n in (self.meta.get("checks") or {})})
        return out

    def hours_until(self, ts):
        t = _ts(ts)
        return (t - self.now).total_seconds() / 3600.0 if t else 0.0

    def hours_since(self, ts):
        t = _ts(ts)
        return (self.now - t).total_seconds() / 3600.0 if t else 0.0

    def at_hours(self, h):
        return opskit.human((self.now + _dt.timedelta(hours=h)).strftime(ISO))

    def wobble(self, x, pct, key="", period=60):
        slot = int(self.now.timestamp() // period)
        r = random.Random(f"{PROG}|{key}|{slot}")
        return x * (1.0 + r.uniform(-pct, pct))

    def live(self, name, tau=120.0, pct=0.0):
        """Current reading of a derived figure: after a change it moves to the new value over a few minutes."""
        tgt = self.m(name)
        d = self.derived.get(name)
        val = tgt
        if d and d.get("prev") is not None and d.get("changed_at"):
            t = _ts(d["changed_at"])
            if t is not None:
                dt = max(0.0, (self.now - t).total_seconds())
                if dt < 8 * tau:
                    val = d["prev"] + (tgt - d["prev"]) * (1.0 - math.exp(-dt / tau))
        return self.wobble(val, pct, name) if pct else val

    def since_change(self, name):
        """Minutes since a derived figure last changed value (a large number if it has not changed)."""
        # Helper so the merge-queue display follows the queue schedule: a ready PR shows as merged at the first queue run after it became ready.
        d = self.derived.get(name)
        if not d or d.get("changed_at") is None or d.get("prev") is None or abs(float(d["prev"]) - float(d.get("value", d["prev"]))) < 1e-9:
            return 1e9
        t = _ts(d["changed_at"])
        return (self.now - t).total_seconds() / 60.0 if t else 1e9


def _dur(hours):
    if hours is None:
        return "-"
    h = abs(hours)
    if h < 1.5:
        txt = f"{int(round(h * 60))} min"
    elif h < 36:
        txt = f"{h:.0f} h"
    else:
        d = int(h // 24); r = int(round(h - 24 * d))
        txt = f"{d} days" + (f" {r} h" if r else "")
    if hours < 0 and txt != "0 min":
        return _Ago(txt)
    return txt


_PAST_VERB = {"opens": "opened", "closes": "closed", "starts": "started", "ends": "ended"}


class _Ago(str):
    """A duration for a time that has already passed. Display rows are written for times ahead
    ("in " + dur(..), dur(..) + " from now"); joined into such a row this reads "<dur> ago" instead."""

    def __new__(cls, base, pre=""):
        s = str.__new__(cls, pre + base + " ago")
        s.base, s.pre = base, pre
        return s

    def __radd__(self, left):
        left = str(left)
        if left.endswith("in about "):
            return left[:-len("in about ")] + "about " + self.base + " ago"
        if left.endswith("in ") and (len(left) == 3 or not left[-4].isalnum()):
            core = left[:-3]
            word = core.rstrip().rsplit(" ", 1)[-1] if core.strip() else ""
            if not core.strip() or core.endswith(("(", ", ")):
                pass
            elif word in _PAST_VERB:
                core = core.rstrip()[: -len(word)] + _PAST_VERB[word] + " "
            else:
                core = core.rstrip() + ", "
            return core + self.base + " ago"
        return _Ago(self.base, left + self.pre)

    def __add__(self, right):
        right = str(right)
        if right.startswith(" from now"):
            return self.pre + self.base + " ago" + right[len(" from now"):]
        if right.startswith(" ago"):            # the row already says "ago": keep the plain duration
            return self.pre + self.base + right
        return self.pre + self.base + " ago" + right


def _render(model, row, **extra):
    label, expr, fmt = (list(row) + [None, None])[:3]
    try:
        val = model.ev(expr, **extra)
    except Exception:
        if os.environ.get("SETTINGS_DEBUG"):
            raise
        val = None
    if val is None:
        return label, "-"
    try:
        return label, (fmt.format(val) if fmt else (_num(val) if isinstance(val, (int, float)) and not isinstance(val, bool) else str(val)))
    except (ValueError, TypeError):
        return label, str(val)


def _write_derived(con, before, after, at, checks):
    old = {r["name"]: dict(r) for r in con.execute("SELECT * FROM derived")}
    for name, val in after.items():
        prev_row = old.get(name)
        b = before.get(name, val)
        ok = int(val) if name in checks else None
        if abs(val - b) > 1e-9:
            row = (name, val, b, at, ok)
        elif prev_row:
            row = (name, val, prev_row["prev"], prev_row["changed_at"], ok)
        else:
            row = (name, val, val, at, ok)
        con.execute("INSERT OR REPLACE INTO derived (name, value, prev, changed_at, ok) VALUES (?, ?, ?, ?, ?)", row)


# ── tracker ──────────────────────────────────────────────────────────────
def _ticket(cid):
    try:
        con = opskit.db("tickets", "tickets.db")
        return con.execute("SELECT * FROM tickets WHERE id = ?", (cid.upper(),)).fetchone()
    except sqlite3.Error:
        return None


def _ticket_state(t):
    if t is None:
        return "not in the tracker"
    who = f", approver {t['approver']}" if t["approver"] else ""
    return f"{TICKET_LABEL.get(t['status'], t['status'].lower())}{who}"


def _control_label(s, meta):
    c = s.get("control")
    if not c:
        return "-"
    return c.get("label") or c.get("group")


# ── commands ─────────────────────────────────────────────────────────────
def cmd_status(a):
    con = _con(); meta = _meta(con)
    model = Model(con, meta)
    blocks = meta.get("status") or []
    if a.scope:
        sc = _scope(con, meta, a.scope)
        blocks = [b for b in blocks if b.get("scope") == sc["id"] or sc["id"] in (b.get("scopes") or [])]
        if not blocks:
            return cmd_show(argparse.Namespace(scope=sc["id"]))
    first = True
    for b in blocks:
        if not first:
            print()
        first = False
        print(b["title"])
        rows = [_render(model, r) for r in b.get("rows", [])]
        w = max([len(l) for l, _ in rows] + [8])
        for l, val in rows:
            print(f"  {l + ':':<{w + 2}}{val}")
        for note in b.get("notes", []):
            print(f"  {note}")
    if meta.get("status_footer"):
        print("\n" + meta["status_footer"])
    return 0


def cmd_list(a):
    con = _con(); meta = _meta(con)
    rows = []
    sc = _scope(con, meta, a.scope)["id"] if a.scope else None
    for s in _settings(con, sc):
        if a.owner and s["owner"] != a.owner:
            continue
        if a.controlled and not s.get("control"):
            continue
        rows.append([s["scope"], s["key"], show_value(s, s["value"]), s["owner"] or "-", _control_label(s, meta),
                     opskit.human(s["updated_at"]) if s.get("updated_at") else "-"])
    if not rows:
        print("no settings match")
        return 0
    opskit.table(rows, [meta.get("scope_col", "SCOPE"), "SETTING", "VALUE", "OWNER", "CHANGE CONTROL", "UPDATED"])
    return 0


def _pending_for(con, scope):
    out = []
    cur = {r["key"]: (r["value"], r["change_id"]) for r in con.execute("SELECT key, value, change_id FROM settings WHERE scope = ?", (scope,))}
    for r in con.execute("SELECT * FROM requests WHERE scope = ? ORDER BY requested_at", (scope,)):
        t = _ticket(r["change_id"])
        if cur.get(r["key"]) == (r["value"], r["change_id"]):
            continue                                   # already applied
        if t is not None and t["status"] in ("PENDING_APPROVAL", "APPROVED", "SCHEDULED", "DRAFT"):
            out.append((dict(r), t))
    return out


def _status_row(meta, sid):
    """The status view's row about one scope: in a block covering it, the row whose expression names it."""
    for b in meta.get("status") or []:
        if b.get("scope") != sid and sid not in (b.get("scopes") or []):
            continue
        for r in b.get("rows", []):
            if len(r) > 1 and isinstance(r[1], str) and repr(sid) in r[1]:
                return r
    return None


def _merged_text(text):
    tail = (text or "").rsplit(" — ", 1)[-1]
    return tail if tail == "merged" or tail.startswith("merged ") else None


def _queue_merged(con, meta, model, sid):
    """'merged (by the queue, <when>)' when the status view reports this scope as merged, else None.
    <when> is the moment that status row turned to merged: settings are constant between recorded changes,
    so the row is replayed back through the history and the switch is found by bisection."""
    row = _status_row(meta, sid)
    if row is None:
        return None
    now_txt = _merged_text(_render(model, row)[1])
    if not now_txt:
        return None

    def says(t, ov):
        m = Model(con, meta, overrides=ov)
        m.now = t
        return bool(_merged_text(_render(m, row)[1]))

    hi, ov, lo, lo_ov = model.now, {}, None, None
    for h in con.execute("SELECT at, scope, key, old FROM history ORDER BY at DESC, id DESC LIMIT 200").fetchall():
        t = _ts(h["at"])
        if t is None:
            continue
        if t >= hi:                        # recorded at the end of the window just checked: earlier times see the old value
            ov = dict(ov); ov[(h["scope"], h["key"])] = _j(h["old"])
            continue
        if not says(t, ov):
            lo, lo_ov = t, ov
            break
        prev = dict(ov); prev[(h["scope"], h["key"])] = _j(h["old"])
        if not says(t - _dt.timedelta(seconds=1), prev):
            lo, lo_ov, hi = t - _dt.timedelta(seconds=1), ov, t
            break
        hi, ov = t, prev
    when = None
    if lo is not None:
        while (hi - lo).total_seconds() > 1:
            mid = lo + (hi - lo) / 2
            if says(mid, lo_ov):
                hi = mid
            else:
                lo = mid
        when = opskit.human(hi.replace(microsecond=0).strftime(ISO))
    how = now_txt[len("merged "):] if now_txt.startswith("merged ") else ""
    inner = ", ".join(x for x in (how, when) if x)
    return "merged" + (f" ({inner})" if inner else "")


def cmd_show(a):
    con = _con(); meta = _meta(con)
    sc = _scope(con, meta, a.scope)
    model = Model(con, meta)
    kind = (meta.get("kinds") or {}).get(sc["kind"] or "", {})
    head = sc["id"] + (f"  {sc['title']}" if sc.get("title") else "")
    print(head)
    fields = [("Kind", kind.get("label") or sc["kind"] or "-"), ("Owner", sc["owner"] or "-")]
    fields += [_render(model, r, S=sc["id"]) for r in kind.get("facts", [])]
    if any(k == "Queue" for k, _ in fields):
        merged = _queue_merged(con, meta, model, sc["id"])
        if merged:
            fields = [(k, merged if k == "Queue" else v) for k, v in fields]
    if sc.get("version"):
        fields.append(("Config version", str(sc["version"])))
    if sc.get("note"):
        fields.append(("Note", sc["note"]))
    w = max(len(k) for k, _ in fields)
    for k, v in fields:
        print(f"  {k + ':':<{w + 2}}{v}")
    ss = _settings(con, sc["id"])
    if ss:
        print("\nSettings:")
        opskit.table([["  " + s["key"], show_value(s, s["value"]), s["owner"] or "-", _control_label(s, meta),
                       opskit.human(s["updated_at"]) if s.get("updated_at") else "-"] for s in ss],
                     ["  SETTING", "VALUE", "OWNER", "CHANGE CONTROL", "UPDATED"])
        notes = [(s["key"], s["note"]) for s in ss if s.get("note")]
        if notes:
            print("\nNotes:")
            for k, n in notes:
                print(f"  {k}: {n}")
    pend = _pending_for(con, sc["id"])
    if pend:
        print("\nChange requests:")
        for r, t in pend:
            s = next((x for x in ss if x["key"] == r["key"]), {"type": "str", "key": r["key"]})
            print(f"  {r['change_id']}  {r['key']} → {show_value(s, _j(r['value']))}  ({_ticket_state(t)})")
    hist = con.execute("SELECT * FROM history WHERE scope = ? ORDER BY at DESC, id DESC LIMIT 4", (sc["id"],)).fetchall()
    if hist:
        print("\nRecent changes:")
        for h in hist:
            s = next((x for x in ss if x["key"] == h["key"]), {"type": "str", "key": h["key"]})
            tk = f"  ({h['change_id']})" if h["change_id"] else (" (emergency)" if h["kind"] == "emergency" else "")
            print(f"  {opskit.human(h['at'])}  {h['key']}: {show_value(s, _j(h['old']))} → {show_value(s, _j(h['new']))}  {h['by']}{tk}")
    return 0


def cmd_get(a):
    con = _con(); meta = _meta(con)
    sc = _scope(con, meta, a.scope)
    s = _get(con, meta, sc["id"], a.key)
    print(f"{sc['id']} {s['key']}")
    rows = [("Value", show_value(s, s["value"])), ("Type", type_label(s)), ("Owner", s["owner"] or "-")]
    c = s.get("control")
    if c:
        who = f", approver {c['approver']}" if c.get("approver") else ""
        rows.append(("Change control", f"approved change from {c.get('label') or c['group']}{who} — pass it with --change"))
    else:
        rows.append(("Change control", "none — roles listed below can change it"))
    rows.append(("Who can edit", ", ".join(s.get("edit_roles") or []) or "-"))
    if s.get("description"):
        rows.append(("Description", s["description"]))
    if s.get("note"):
        rows.append(("Note", s["note"]))
    if s.get("updated_at"):
        by = f" by {s['updated_by']}" if s.get("updated_by") else ""
        ch = f" ({s['change_id']})" if s.get("change_id") else ""
        rows.append(("Last changed", f"{opskit.human(s['updated_at'])}{by}{ch}"))
    w = max(len(k) for k, _ in rows)
    for k, v in rows:
        print(f"  {k + ':':<{w + 2}}{v}")
    pend = [(r, t) for r, t in _pending_for(con, sc["id"]) if r["key"] == s["key"]]
    for r, t in pend:
        print(f"  {'Change request:':<{w + 2}}{r['change_id']} → {show_value(s, _j(r['value']))} ({_ticket_state(t)})")
    return 0


def cmd_history(a):
    con = _con(); meta = _meta(con)
    q, args = "SELECT * FROM history WHERE 1=1", []
    if a.scope:
        sc = _scope(con, meta, a.scope)["id"]
        q += " AND scope = ?"; args.append(sc)
        if a.key:
            _get(con, meta, sc, a.key)
            q += " AND key = ?"; args.append(a.key)
    q += " ORDER BY at DESC, id DESC LIMIT ?"; args.append(a.limit)
    rows = con.execute(q, args).fetchall()
    if not rows:
        print("no changes recorded")
        return 0
    specs = {(s["scope"], s["key"]): s for s in _settings(con)}
    out = []
    for h in reversed(rows):
        s = specs.get((h["scope"], h["key"]), {"type": "str", "key": h["key"]})
        tk = h["change_id"] or ("emergency" if h["kind"] == "emergency" else "-")
        out.append([opskit.human(h["at"]), h["scope"], h["key"], f"{show_value(s, _j(h['old']))} → {show_value(s, _j(h['new']))}",
                    h["by"], tk, h["note"] or ""])
    opskit.table(out, ["WHEN", meta.get("scope_col", "SCOPE"), "SETTING", "CHANGE", "BY", "TICKET", "NOTE"])
    return 0


def cmd_changes(a):
    con = _con(); meta = _meta(con)
    specs = {(s["scope"], s["key"]): s for s in _settings(con)}
    rows = []
    for r in con.execute("SELECT * FROM requests ORDER BY requested_at DESC"):
        t = _ticket(r["change_id"])
        st = t["status"] if t is not None else None
        if not a.all and st not in ("PENDING_APPROVAL", "APPROVED", "SCHEDULED", "DRAFT"):
            continue
        s = specs.get((r["scope"], r["key"]), {"type": "str", "key": r["key"]})
        applied = s.get("value") == _j(r["value"]) and s.get("change_id") == r["change_id"]
        rows.append([r["change_id"], r["scope"], r["key"], show_value(s, _j(r["value"])),
                     "applied" if applied else (TICKET_LABEL.get(st, (st or "-").lower()) if st else "not in tracker"),
                     (t["approver"] if t is not None and t["approver"] else "-"), r["requested_by"], opskit.human(r["requested_at"])])
    if not rows:
        print("no open change requests" + ("" if a.all else " (use --all for closed ones)"))
        return 0
    opskit.table(rows, ["CHANGE", meta.get("scope_col", "SCOPE"), "SETTING", "REQUESTED", "STATUS", "APPROVER", "BY", "OPENED"])
    return 0


def _assignments(con, meta, scope, items):
    if len(items) == 2 and "=" not in items[0]:
        pairs = [(items[0], items[1])]
    else:
        pairs = []
        for it in items:
            if "=" not in it:
                opskit.die(PROG, f"expected <setting> <value> or <setting>=<value> ..., got '{it}'", 2)
            k, _, val = it.partition("=")
            pairs.append((k.strip(), val))
    out = []
    for k, raw in pairs:
        s = _get(con, meta, scope, k)
        out.append((s, parse_value(s, raw)))
    return out


def _gated(s, new):
    c = s.get("control")
    if not c:
        return False
    band = c.get("free_range")
    if band and isinstance(new, (int, float)) and not isinstance(new, bool):
        lo, hi = band.get("min"), band.get("max")
        if (lo is None or new >= lo) and (hi is None or new <= hi):
            return False
    return True


def _change_problem(con, sc, gated, cid):
    """Why the change ticket `cid` does not allow these change-controlled edits, or None when it does.
    Returns (message, short reason, audit fields) for the first problem, checked in the order `set --yes` applies."""
    t = _ticket(cid)
    if t is None:
        msg = f"change {cid} not found in the tracker"
        return msg, msg, dict(scope=sc, key=gated[0][0]["key"], change=cid, reason="unknown change")
    reqs = {r["key"]: _j(r["value"]) for r in con.execute("SELECT * FROM requests WHERE change_id = ? AND scope = ?", (t["id"], sc))}
    for s, new in gated:
        c = s["control"]
        ok_scope = (t["type"] == "change" and (t["service"] in (None, "", sc)) and s["key"] in reqs
                    and (t["approval_group"] or "") == c["group"])
        want = reqs.get(s["key"])
        within = ok_scope and (new == want or (isinstance(new, (int, float)) and isinstance(want, (int, float))
                                               and isinstance(s["value"], (int, float))
                                               and min(s["value"], want) <= new <= max(s["value"], want)))
        if not ok_scope or not within:
            covers = ", ".join(f"{k} → {show_value(s if k == s['key'] else {'type': 'str', 'key': k}, v)}" for k, v in reqs.items())
            msg = (f"{t['id']} does not cover {s['key']} = {show_value(s, new)} on {sc}"
                   + (f" (it covers {covers})" if covers else ""))
            return msg, msg, dict(scope=sc, key=s["key"], new=new, change=t["id"], reason="change scope mismatch")
        if t["status"] not in OK_CHANGE:
            who = f" (approver: {t['approver']})" if t["approver"] else ""
            state = f"{t['id']} is {TICKET_LABEL.get(t['status'], t['status'].lower())}{who}"
            return (f"{state}; {s['key']} changes need an approved change", state,
                    dict(scope=sc, key=s["key"], new=new, change=t["id"], reason=f"change {t['status']}"))
    return None


def _preview(con, meta, sc, changes):
    before = Model(con, meta)
    after = Model(con, meta, overrides={(sc, s["key"]): new for s, new in changes})
    print(f"{sc}:")
    w = max(len(s["key"]) for s, _ in changes)
    for s, new in changes:
        tag = ""
        if _gated(s, new):
            c = s["control"]
            tag = f"   change-controlled: {c.get('label') or c['group']}"
        print(f"  {s['key']:<{w}}  {show_value(s, s['value'])} → {show_value(s, new)}{tag}")
    rows = [r for r in (meta.get("preview") or []) if not r[3:] or any(sc == x or sc.startswith(x) for x in r[3])]
    shown = []
    for r in rows:
        l, b = _render(before, r[:3])
        _, n = _render(after, r[:3])
        shown.append((l, b, n))
    if shown:
        print("effect:")
        w2 = max(len(l) for l, _, _ in shown)
        for l, b, n in shown:
            print(f"  {l:<{w2}}  {b} → {n}" if b != n else f"  {l:<{w2}}  {b} (unchanged)")


def cmd_diff(a):
    con = _con(); meta = _meta(con)
    sc = _scope(con, meta, a.scope)["id"]
    changes = [(s, new) for s, new in _assignments(con, meta, sc, a.items) if new != s["value"]]
    if not changes:
        print("nothing to change")
        return 0
    _preview(con, meta, sc, changes)
    return 0


def cmd_set(a):
    con = _con(); meta = _meta(con)
    me = opskit.identity()
    roles = set(me.get("roles") or [])
    sc = _scope(con, meta, a.scope)["id"]
    allc = _assignments(con, meta, sc, a.items)
    changes = [(s, new) for s, new in allc if new != s["value"]]
    for s, new in allc:
        if new == s["value"]:
            print(f"{s['key']} is already {show_value(s, new)}")
    if not changes:
        return 0
    # permission
    for s, new in changes:
        if not roles & set(s.get("edit_roles") or []):
            opskit.audit(PROG, "set", result="denied", scope=sc, key=s["key"], new=new)
            owner = f" (owned by {s['owner']})" if s.get("owner") else ""
            opskit.die(PROG, f"permission denied: {me['user']} cannot change {s['key']} on {sc}{owner}", 13)
    gated = [(s, new) for s, new in changes if _gated(s, new)]
    em = meta.get("emergency") or {}
    if not a.yes:
        _preview(con, meta, sc, changes)
        if gated and not a.change and not a.emergency:
            labels = sorted({(s["control"].get("label") or s["control"]["group"]) for s, _ in gated})
            print(f"needs an approved change from {', '.join(labels)} (--change CHG-…)")
        elif gated and a.change and not a.emergency:
            bad = _change_problem(con, sc, gated, a.change)
            if bad:
                print(f"{bad[1]} — applying with --yes will be refused")
                print("not applied")
                return 1
        print("not applied — re-run with --yes")
        return 1
    change_id, emergency = None, False
    if gated and a.emergency:
        if not em:
            opskit.die(PROG, "unrecognized option --emergency", 2)
        if not (a.reason or "").strip():
            opskit.die(PROG, f"--emergency needs --reason (it goes into the change record and the page to {em.get('page', 'the owning team')})", 2)
        if not roles & set(em.get("roles") or []):
            opskit.audit(PROG, "set", result="denied", scope=sc, key=",".join(s["key"] for s, _ in gated), emergency=True, reason=a.reason.strip())
            opskit.die(PROG, f"permission denied: emergency changes need one of: {', '.join(em.get('roles') or [])}", 13)
        emergency = True
    elif gated:
        if not a.change:
            for s, new in gated:
                opskit.audit(PROG, "set", result="rejected", scope=sc, key=s["key"], new=new, reason="no change id")
            s0 = gated[0][0]
            c = s0["control"]
            opskit.die(PROG, f"{s0['key']} on {sc} is change-controlled ({c.get('label') or c['group']}); "
                             f"pass an approved change with --change CHG-… (see `{PROG} changes`)", 3)
        bad = _change_problem(con, sc, gated, a.change)
        if bad:
            msg, _short, fields = bad
            opskit.audit(PROG, "set", result="rejected", **fields)
            opskit.die(PROG, msg, 3)
        change_id = _ticket(a.change)["id"]
    elif a.change:
        change_id = a.change.upper()
    # apply
    before = Model(con, meta).all()
    if emergency:
        print(f"emergency change: skipping the change check (reason: {a.reason.strip()})")
        print(f"  {em.get('page', 'the owning team')} has been paged; this change will be reviewed")
    at = opskit.iso()
    row = con.execute("SELECT version FROM scopes WHERE id = ?", (sc,)).fetchone()
    ver = (row["version"] or 0) + 1 if row else 1
    gkeys = {s["key"] for s, _ in gated}
    for s, new in changes:
        cid = change_id
        con.execute("UPDATE settings SET value = ?, updated_at = ?, updated_by = ?, change_id = ? WHERE scope = ? AND key = ?",
                    (_enc(new), at, me["user"], cid, sc, s["key"]))
        con.execute("INSERT INTO history (at, scope, key, old, new, by, change_id, kind, note) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (at, sc, s["key"], _enc(s["value"]), _enc(new), me["user"], cid,
                     "emergency" if emergency and s["key"] in gkeys else ("change" if cid else "edit"),
                     (a.note or (a.reason if emergency else None))))
    con.execute("UPDATE scopes SET version = ? WHERE id = ?", (ver, sc))
    after = Model(con, meta).all()
    _write_derived(con, before, after, at, set((meta.get("checks") or {}).keys()))
    steps = meta.get("apply_steps") or ["applied"]
    print((meta.get("apply_head") or "{scope}: writing config v{version}").format(scope=sc, version=ver)
          + (f" ({change_id})" if change_id else ""))
    for st in steps:
        time.sleep(0.35)
        print("  " + st.format(scope=sc, version=ver))
    con.commit()
    for s, new in changes:
        g = s["key"] in gkeys
        extra = {"emergency": True, "reason": a.reason.strip()} if emergency and g else {}
        opskit.audit(PROG, "set", scope=sc, key=s["key"], old=s["value"], new=new, change=change_id, gated=g,
                     owner=s.get("owner"), **extra)
    for s, new in changes:
        print(f"{sc} {s['key']} = {show_value(s, new)}")
    return 0


# ── cli ──────────────────────────────────────────────────────────────────
def main(argv=None):
    meta = {}
    try:
        p0 = os.path.join(opskit.STATE_ROOT, PROG, DB)
        if os.path.exists(p0):
            c0 = sqlite3.connect(f"file:{p0}?mode=ro", uri=True)
            r = c0.execute("SELECT v FROM meta WHERE k = 'config'").fetchone()
            meta = json.loads(r[0]) if r else {}
            c0.close()
    except (sqlite3.Error, ValueError):
        meta = {}
    noun = meta.get("scope_noun", "scope")
    p = argparse.ArgumentParser(prog=PROG, description=meta.get("description", "Operational settings with owners and change control."),
                                epilog=meta.get("epilog"), formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True, metavar="{status,list,show,get,history,changes,diff,set}")
    s = sub.add_parser("status", help=meta.get("status_help", "summary figures")); s.add_argument("scope", nargs="?"); s.set_defaults(fn=cmd_status)
    s = sub.add_parser("list", help="settings with owner and change control")
    s.add_argument("scope", nargs="?", help=f"only this {noun}"); s.add_argument("--owner", help="only settings owned by this team")
    s.add_argument("--controlled", action="store_true", help="only change-controlled settings"); s.set_defaults(fn=cmd_list)
    s = sub.add_parser("show", help=f"one {noun}: context, settings, open change requests, recent changes")
    s.add_argument("scope"); s.set_defaults(fn=cmd_show)
    s = sub.add_parser("get", help="one setting in detail"); s.add_argument("scope"); s.add_argument("key"); s.set_defaults(fn=cmd_get)
    s = sub.add_parser("history", help="recorded changes (newest last)")
    s.add_argument("scope", nargs="?"); s.add_argument("key", nargs="?"); s.add_argument("--limit", type=int, default=20); s.set_defaults(fn=cmd_history)
    s = sub.add_parser("changes", help="change requests for controlled settings and their ticket status")
    s.add_argument("--all", action="store_true", help="include closed and rejected ones"); s.set_defaults(fn=cmd_changes)
    s = sub.add_parser("diff", help="preview a change and its effect without applying it")
    s.add_argument("scope"); s.add_argument("items", nargs="+", metavar="SETTING VALUE | SETTING=VALUE"); s.set_defaults(fn=cmd_diff)
    s = sub.add_parser("set", help="change settings (previews unless --yes)")
    s.add_argument("scope"); s.add_argument("items", nargs="+", metavar="SETTING VALUE | SETTING=VALUE")
    s.add_argument("--change", help="approved change ticket (change-controlled settings)")
    em = meta.get("emergency")
    if em:
        s.add_argument("--emergency", action="store_true", help=em.get("help", "apply without an approved change (needs --reason)"))
        s.add_argument("--reason", help="why the emergency change is needed")
    s.add_argument("--note", help="note for the change history")
    s.add_argument("--yes", action="store_true", help="apply (otherwise only previews)")
    s.set_defaults(fn=cmd_set, emergency=False, reason=None)
    a = p.parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    opskit.run(main)
