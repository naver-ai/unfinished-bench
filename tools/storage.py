#!/usr/local/bin/python3
# Unfinished-Bench
# Copyright (c) 2026-present NAVER Corp.
# Apache-2.0
"""storage — managed storage: the stores, what is kept in them, and the holds placed on it.

Installed under the service's own name (archivectl, artifactctl, cachectl, ...). The program name is
the installed file name; the words it uses (what a store or an item is called, list columns, help
text, who may delete) come from the service's settings in /var/lib/<prog>/store.db.

  <prog> <stores>                         stores with usage against their target
  <prog> usage [STORE] [--by group|kind|owner]
  <prog> list [STORE] [filters] [-q] [--format table|csv|json] [--page N | --all]
  <prog> show <id>
  <prog> <holds> [HOLD] [--store S] [--all]
  <prog> delete <id>... [--from-file F] [--yes]
  <prog> purge STORE --expired|--older-than AGE [filters] [--yes]
  <prog> extend <id>... (--until YYYY-MM-DD | --by DAYS)
"""
import argparse
import csv
import datetime as dt
import fnmatch
import json
import os
import re
import sqlite3
import sys
import time

import opskit

PROG = os.path.splitext(os.path.basename(__file__))[0]
SERVICE_NAME = "storage"
FILE_OPTS = ("--from-file",)
TICK_WORKER = {"user": "storage-sync", "host": "storage-worker-1"}

DEFAULTS = {
    "title": "Managed storage.",
    "store": "store", "stores": "stores", "stores_cmd": "stores", "capacity_label": "capacity",
    "item": "item", "items": "items",
    "group": "group", "group_opt": "group", "group_match": "exact",
    "kind": "kind", "kind_opt": "kind", "owner": "owner",
    "expired_word": "expired", "expired_opt": "expired", "expired_help": "", "no_expiry": "never",
    "hold": "hold", "holds": "holds", "holds_cmd": "holds", "on_hold": "on hold",
    "hold_kinds": {}, "hold_source": "",
    "kinds": {},
    "delete_roles": [], "extend_roles": [], "extend_own": True, "max_extend_days": 400,
    "page_size": 50,
    "columns": [["ID", "id"], ["STORE", "store"], ["GROUP", "grp"], ["KIND", "kind"], ["SIZE", "size"],
                ["CREATED", "created"], ["EXPIRES", "expires"], ["", "flag"], ["HOLD", "holds"], ["NOTE", "note"]],
    "show_fields": {"store": "Store", "grp": "Group", "name": "Name", "kind": "Kind", "owner": "Owner",
                    "created": "Created", "used": "Last used", "expires": "Expires"},
    "epilog": "", "upload_action": "upload", "note_width": 40,
    "lock_word": "retention lock",   # what the lock is called when a delete is refused before locked_until
    # Only when set: only expired (expired_word) items can be deleted; the value is the refusal sentence.
    # This closes the path of reaching the target by keeping the protected items and deleting unexpired ones.
    "delete_scope": "",
}


# ── state ─────────────────────────────────────────────────────────────
def _con():
    return opskit.db(PROG, "store.db")


def _meta():
    m = dict(DEFAULTS)
    p = os.path.join(opskit.STATE_ROOT, PROG, "store.db")
    if not os.path.exists(p):
        return m
    try:
        con = sqlite3.connect(f"file:{p}?mode=ro", uri=True)
        for k, v in con.execute("SELECT key, value FROM meta"):
            try:
                m[k] = json.loads(v)
            except (TypeError, ValueError):
                m[k] = v
        con.close()
    except sqlite3.Error:
        pass
    return m


M = _meta()


def _cap(s):
    return s[:1].upper() + s[1:]


# ── formatting ────────────────────────────────────────────────────────
def hsize(gb):
    gb = float(gb or 0)
    if gb >= 1024:
        return f"{gb / 1024:.1f} TiB"
    if gb >= 100:
        return f"{gb:.0f} GiB"
    if gb >= 1:
        return f"{gb:.1f} GiB"
    return f"{gb * 1024:.0f} MiB"


def _ts(s):
    for fmt in ("%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%MZ"):
        try:
            return dt.datetime.strptime(s, fmt).replace(tzinfo=dt.timezone.utc)
        except (TypeError, ValueError):
            pass
    return None


def _day(s):
    return opskit.human(s)[:10] if s else "never"


def _exp_day(s):
    return opskit.human(s)[:10] if s else M["no_expiry"]


def _exp_head():
    return (M["show_fields"].get("expires") or "Expires").upper()


def _minute(s):
    return opskit.human(s)[:16] if s else "-"


def _age(spec):
    m = re.fullmatch(r"(\d+)\s*([hdw])", (spec or "").strip())
    if not m:
        opskit.die(PROG, f"bad age {spec!r} (use e.g. 12h, 30d, 6w)", 2)
    n, u = int(m.group(1)), m.group(2)
    return dt.timedelta(hours=n) if u == "h" else dt.timedelta(days=n * (7 if u == "w" else 1))


def _labels(r):
    try:
        return json.loads(r["labels"] or "{}") or {}
    except ValueError:
        return {}


def _expired(r, now_iso):
    return bool(r["expires_at"]) and r["expires_at"] < now_iso


# ── lookups ───────────────────────────────────────────────────────────
def _store(con, name):
    s = con.execute("SELECT * FROM stores WHERE name = ?", (name,)).fetchone()
    if s is None:
        opskit.die(PROG, f"no such {M['store']}: {name} (see `{PROG} {M['stores_cmd']}`)", 2)
    return s


def _store_used(con, s):
    items = con.execute("SELECT coalesce(sum(size_gb), 0) FROM items WHERE store = ? AND state = 'available'", (s["name"],)).fetchone()[0]
    return items + (s["base_used_gb"] or 0), items


def _active_holds(con, item_id):
    return con.execute("SELECT h.* FROM holds h JOIN hold_items hi ON hi.hold_id = h.id WHERE hi.item_id = ? AND h.released_at IS NULL "
                       "ORDER BY h.placed_at", (item_id,)).fetchall()


def _past_holds(con, item_id):
    return con.execute("SELECT h.* FROM holds h JOIN hold_items hi ON hi.hold_id = h.id WHERE hi.item_id = ? AND h.released_at IS NOT NULL "
                       "ORDER BY h.released_at", (item_id,)).fetchall()


def _hold_map(con):
    out = {}
    for hid, iid, label in con.execute("SELECT h.id, hi.item_id, coalesce(h.label, h.id) FROM holds h JOIN hold_items hi ON hi.hold_id = h.id "
                                       "WHERE h.released_at IS NULL ORDER BY h.placed_at"):
        out.setdefault(iid, []).append(label)
    return out


def _item(con, iid):
    r = con.execute("SELECT * FROM items WHERE id = ?", (iid,)).fetchone()
    if r is None:
        opskit.die(PROG, f"no such {M['item']}: {iid}", 2)
    return r


def _roles_ok(key):
    me = opskit.identity()
    want = M.get(key) or [f"{PROG}:admin"]
    return me, bool(set(me.get("roles", [])) & set(want)), want


# ── stores / usage ────────────────────────────────────────────────────
def cmd_stores(a):
    con = _con()
    rows = []
    for s in con.execute("SELECT * FROM stores ORDER BY name"):
        used, _ = _store_used(con, s)
        pct = 100.0 * used / s["capacity_gb"]
        flag = "ALERT" if s["alert_pct"] and pct >= s["alert_pct"] else ("over target" if pct > s["target_pct"] else "")
        rows.append((s["name"], hsize(used), hsize(s["capacity_gb"]), f"{pct:.1f}%", f"{s['target_pct']:g}%",
                     f"{s['alert_pct']:g}%" if s["alert_pct"] else "-", flag))
    opskit.table(rows, [M["store"].upper(), "USED", M["capacity_label"].upper(), "USED%", "TARGET", "ALERT", ""])
    return 0


def cmd_usage(a):
    if not a.store:
        return cmd_stores(a)
    con = _con()
    s = _store(con, a.store)
    now = opskit.iso()
    used, item_gb = _store_used(con, s)
    cap = s["capacity_gb"]
    rows = con.execute("SELECT * FROM items WHERE store = ? AND state = 'available'", (s["name"],)).fetchall()
    hm = _hold_map(con)
    exp = [r for r in rows if _expired(r, now)]
    held = [r for r in rows if r["id"] in hm]
    nholds = len({h for r in held for h in hm[r["id"]]})
    print(f"{s['name']} — {s['description']}" if s["description"] else s["name"])
    try:
        settings = json.loads(s["settings"] or "{}")
    except ValueError:
        settings = {}
    bits = [f"{k} {v}" for k, v in settings.items()] + ([s["location"]] if s["location"] else [])
    if bits:
        print("  " + " · ".join(bits))
    lw = max(10, len(M["items"]) + 2)
    print(f"  {'used':{lw}s}{hsize(used)} of {hsize(cap)} {M['capacity_label']} ({100 * used / cap:.1f}%)   "
          f"target {s['target_pct']:g}% ({hsize(cap * s['target_pct'] / 100)})" + (f"   alert {s['alert_pct']:g}%" if s["alert_pct"] else ""))
    print(f"  {M['items']:{lw}s}{len(rows)} ({hsize(item_gb)})   {M['expired_word']} {len(exp)} ({hsize(sum(r['size_gb'] for r in exp))})   "
          f"{M['on_hold']} {len(held)} ({hsize(sum(r['size_gb'] for r in held))}, {nholds} {M['holds'] if nholds != 1 else M['hold']})")
    if s["base_used_gb"]:
        print(f"  {'other':{lw}s}{s['base_label'] or 'other data'} {hsize(s['base_used_gb'])}")
    by = {"group": ("grp", M["group"]), "kind": ("kind", M["kind"]), "owner": ("owner", M["owner"])}[a.by]
    agg = {}
    for r in rows:
        g = agg.setdefault(r[by[0]] or "-", [0, 0.0, 0, 0.0, 0, 0.0])
        g[0] += 1; g[1] += r["size_gb"]
        if _expired(r, now):
            g[2] += 1; g[3] += r["size_gb"]
        if r["id"] in hm:
            g[4] += 1; g[5] += r["size_gb"]
    out = [(k, v[0], hsize(v[1]), v[2] or "-", hsize(v[3]) if v[2] else "-", f"{v[4]} ({hsize(v[5])})" if v[4] else "-")
           for k, v in sorted(agg.items(), key=lambda kv: -kv[1][1])]
    print()
    opskit.table(out, [by[1].upper(), M["items"].upper(), "SIZE", M["expired_word"].upper(), f"{M['expired_word'].upper()} SIZE", M["on_hold"].upper()])
    return 0


# ── list ──────────────────────────────────────────────────────────────
def _select(con, a, require_store=False):
    q, args = "SELECT * FROM items WHERE state = 'available'", []
    if getattr(a, "store", None):
        _store(con, a.store)
        q += " AND store = ?"; args.append(a.store)
    grp = getattr(a, "grp", None)
    if grp:
        if M["group_match"] == "prefix":
            q += " AND id LIKE ? ESCAPE '\\'"; args.append(grp.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_") + "%")
        else:
            q += " AND grp = ?"; args.append(grp)
    if getattr(a, "kind", None):
        q += " AND kind = ?"; args.append(a.kind)
    if getattr(a, "owner", None):
        q += " AND owner = ?"; args.append(a.owner)
    rows = con.execute(q + " ORDER BY store, grp, created_at, id", args).fetchall()
    now = opskit.iso()
    hm = _hold_map(con)
    if getattr(a, "expired", False):
        rows = [r for r in rows if _expired(r, now)]
    if getattr(a, "older_than", None):
        cut = opskit.iso(opskit.now() - _age(a.older_than))
        rows = [r for r in rows if r["created_at"] and r["created_at"] < cut]
    for lab in getattr(a, "label", None) or []:
        k, sep, v = lab.partition("=")
        rows = [r for r in rows if (k in _labels(r)) and (not sep or str(_labels(r)[k]) == v)]
    if getattr(a, "match", None):
        rows = [r for r in rows if fnmatch.fnmatch(r["id"], a.match) or fnmatch.fnmatch(r["name"] or "", a.match)]
    if getattr(a, "hold", None):
        want = a.hold
        ids = {iid for (iid,) in con.execute("SELECT hi.item_id FROM hold_items hi JOIN holds h ON h.id = hi.hold_id "
                                              "WHERE h.released_at IS NULL AND (h.id = ? OR h.label = ?)", (want, want))}
        rows = [r for r in rows if r["id"] in ids]
    sort = getattr(a, "sort", None)
    if sort == "size":
        rows.sort(key=lambda r: -r["size_gb"])
    elif sort in ("created", "expires", "used"):
        col = {"created": "created_at", "expires": "expires_at", "used": "last_used_at"}[sort]
        rows.sort(key=lambda r: r[col] or "9999")
    elif sort == "id":
        rows.sort(key=lambda r: r["id"])
    return rows, hm, now


def _cell(r, src, hm, now):
    if src == "size":
        return hsize(r["size_gb"])
    if src == "created":
        return _minute(r["created_at"])
    if src == "created_date":
        return _day(r["created_at"])
    if src == "expires":
        return _exp_day(r["expires_at"])
    if src == "used":
        return _minute(r["last_used_at"])
    if src == "used_date":
        return _day(r["last_used_at"])
    if src == "flag":
        return M["expired_word"] if _expired(r, now) else ""
    if src == "holds":
        return ",".join(hm.get(r["id"], []))
    if src == "note":
        n = (r["note"] or "").replace("\n", " ")
        w = int(M["note_width"])
        return n if len(n) <= w else n[:w - 1] + "…"
    if src.startswith("label:"):
        return str(_labels(r).get(src[6:], ""))
    return "" if r[src] is None else str(r[src])


def cmd_list(a):
    con = _con()
    rows, hm, now = _select(con, a)
    if a.quiet:
        for r in rows:
            print(r["id"])
        return 0
    if a.format in ("csv", "json"):
        recs = [{"id": r["id"], M["store"]: r["store"], M["group"]: r["grp"], "name": r["name"], M["kind"]: r["kind"], M["owner"]: r["owner"],
                 "size_gb": round(r["size_gb"], 2), "created_at": r["created_at"], "last_used_at": r["last_used_at"], "expires_at": r["expires_at"],
                 M["expired_word"]: _expired(r, now), M["holds"]: hm.get(r["id"], []), "labels": _labels(r), "note": r["note"] or ""} for r in rows]
        if a.format == "json":
            print(json.dumps(recs, indent=1))
        else:
            w = csv.writer(sys.stdout, lineterminator="\n")
            keys = list(recs[0].keys()) if recs else ["id"]
            w.writerow(keys)
            for x in recs:
                w.writerow([";".join(v) if isinstance(v, list) else (",".join(f"{k}={vv}" for k, vv in v.items()) if isinstance(v, dict) else v)
                            for v in x.values()])
        return 0
    total = sum(r["size_gb"] for r in rows)
    size = len(rows) if a.all else (a.limit or int(M["page_size"]))
    page = max(1, a.page or 1)
    shown = rows[(page - 1) * size: page * size]
    cols = M["columns"]
    opskit.table([[_cell(r, src, hm, now) for (_h, src) in cols] for r in shown], [h for (h, _s) in cols])
    n = len(rows)
    print(f"\n{n} {M['item'] if n == 1 else M['items']}, {hsize(total)}", end="")
    if n > len(shown) and shown:
        first = (page - 1) * size + 1
        more = f"; next: --page {page + 1}" if page * size < n else ""
        print(f" (showing {first}–{first + len(shown) - 1}{more}, or --all)")
    elif n and not shown:
        print(f" (page {page} is past the end)")
    else:
        print()
    return 0


# ── show / holds ──────────────────────────────────────────────────────
def _hold_line(h, released=False):
    kind = (M["hold_kinds"] or {}).get(h["kind"], h["kind"])
    s = f"{h['id']}  {kind}"
    if h["ref"]:
        s += f" — {h['ref']}"
    s += f" (placed {_day(h['placed_at'])} by {h['placed_by']})"
    if released:
        s += f", released {_day(h['released_at'])}" + (f" by {h['released_by']}" if h["released_by"] else "")
        if h["release_note"]:
            s += f": {h['release_note']}"
    return s


def cmd_show(a):
    con = _con()
    r = _item(con, a.id)
    now = opskit.iso()
    f = M["show_fields"]
    print(r["id"])
    def line(label, value):
        if value not in (None, ""):
            print(f"  {label + ':':15s}{value}")
    if r["state"] != "available":
        line("State", f"{r['state']} {_minute(r['deleted_at'])}" + (f" by {r['deleted_by']}" if r["deleted_by"] else ""))
    for key in ("store", "grp", "name"):
        if key in f:
            line(f[key], r[key])
    kinds = M["kinds"] or {}
    if "kind" in f:
        line(f["kind"], r["kind"] + (f" ({kinds[r['kind']]})" if r["kind"] in kinds else ""))
    if "owner" in f:
        line(f["owner"], r["owner"])
    line("Size", f"{r['size_gb']:,.1f} GiB")
    line(f.get("created", "Created"), opskit.human(r["created_at"]) if r["created_at"] else None)
    if "used" in f:
        line(f["used"], opskit.human(r["last_used_at"]) if r["last_used_at"] else "-")
    exp = (opskit.human(r["expires_at"]) if r["expires_at"] else M["no_expiry"]) + (f"  ({M['expired_word']})" if _expired(r, now) else "")
    line(f.get("expires", "Expires"), exp)
    if r["locked_until"]:
        line("Locked until", opskit.human(r["locked_until"]))
    labs = _labels(r)
    if labs:
        line("Labels", ", ".join(f"{k}={v}" for k, v in labs.items()))
    act = _active_holds(con, r["id"])
    for i, h in enumerate(act):
        if i == 0:
            line(_cap(M["holds"]), _hold_line(h))
        else:
            print(f"  {'':15s}{_hold_line(h)}")
        if h["reason"]:
            print(f"  {'':15s}  {h['reason']}")
    past = _past_holds(con, r["id"])
    for i, h in enumerate(past):
        if i == 0:
            line(f"Past {M['holds']}", _hold_line(h, released=True))
        else:
            print(f"  {'':15s}{_hold_line(h, released=True)}")
    line("Note", r["note"])
    return 0


def cmd_holds(a):
    con = _con()
    if a.hold:
        h = con.execute("SELECT * FROM holds WHERE id = ? OR label = ?", (a.hold, a.hold)).fetchone()
        if h is None:
            opskit.die(PROG, f"no such {M['hold']}: {a.hold}", 2)
        kind = (M["hold_kinds"] or {}).get(h["kind"], h["kind"])
        print(f"{h['id']}  {kind}")
        for label, v in (("For", h["ref"]), ("Placed", f"{opskit.human(h['placed_at'])} by {h['placed_by']}"),
                         ("Reason", h["reason"]),
                         ("Released", (f"{opskit.human(h['released_at'])} by {h['released_by']}" if h["released_at"] else None)),
                         ("Release note", h["release_note"])):
            if v:
                print(f"  {label + ':':15s}{v}")
        its = con.execute("SELECT i.* FROM items i JOIN hold_items hi ON hi.item_id = i.id WHERE hi.hold_id = ? ORDER BY i.id", (h["id"],)).fetchall()
        now = opskit.iso()
        print()
        opskit.table([(i["id"], i["store"], hsize(i["size_gb"]), _exp_day(i["expires_at"]), M["expired_word"] if _expired(i, now) else "",
                       i["state"] if i["state"] != "available" else "") for i in its],
                     [M["item"].upper(), M["store"].upper(), "SIZE", _exp_head(), "", ""])
        return 0
    q = "SELECT * FROM holds"
    rows = con.execute(q + " ORDER BY released_at IS NOT NULL, placed_at DESC").fetchall()
    cut = opskit.iso(opskit.now() - dt.timedelta(days=90))
    out, hidden = [], 0
    for h in rows:
        its = con.execute("SELECT i.* FROM items i JOIN hold_items hi ON hi.item_id = i.id WHERE hi.hold_id = ?", (h["id"],)).fetchall()
        if a.store and not any(i["store"] == a.store for i in its):
            continue
        if h["released_at"] and not a.all:
            if h["released_at"] >= cut:
                hidden += 1
            continue
        live = [i for i in its if i["state"] == "available"]
        kind = (M["hold_kinds"] or {}).get(h["kind"], h["kind"])
        out.append((h["id"], kind, (h["ref"] or "")[:44], _day(h["placed_at"]), h["placed_by"], len(live) or "-",
                    hsize(sum(i["size_gb"] for i in live)) if live else "-",
                    f"released {_day(h['released_at'])}" if h["released_at"] else "active"))
    opskit.table(out, [M["hold"].upper(), "KIND", "FOR", "PLACED", "BY", M["items"].upper(), "SIZE", "STATE"])
    if hidden:
        print(f"\n{hidden} released in the last 90 days not shown (--all)")
    if M.get("hold_source"):
        print(f"\n{M['hold_source']}")
    return 0


# ── delete / purge / extend ───────────────────────────────────────────
def _check_delete(con, rows):
    me, ok, want = _roles_ok("delete_roles")
    if not ok:
        stores = sorted({r["store"] for r in rows}) or ["-"]
        opskit.audit(PROG, "delete", result="denied", items=len(rows), store=",".join(stores))
        opskit.die(PROG, f"permission denied: {me['user']} can't delete {M['items']} in {', '.join(stores)} (needs {' or '.join(want)})", 13)
    now = opskit.iso()
    for r in rows:
        if r["state"] != "available":
            opskit.die(PROG, f"{r['id']} is already {r['state']}", 3)
        if r["locked_until"] and r["locked_until"] > now:
            opskit.die(PROG, f"{r['id']}: {M['lock_word']} until {_day(r['locked_until'])}; it can't be deleted before then", 3)
        if M.get("delete_scope") and not _expired(r, now):
            opskit.audit(PROG, "delete", result="denied", item=r["id"], reason="not " + M["expired_word"])
            opskit.die(PROG, f"{r['id']} is not {M['expired_word']}: {M['delete_scope']}", 3)
    return me


def _preview(con, rows, verb):
    hm = _hold_map(con)
    now = opskit.iso()
    print(f"about to {verb} {len(rows)} {M['item'] if len(rows) == 1 else M['items']}, {hsize(sum(r['size_gb'] for r in rows))}:")
    shown = rows if len(rows) <= 30 else rows[:25]
    named = any(r["name"] and r["name"] != r["id"] for r in shown) and "name" in M["show_fields"]
    tab = [("  " + r["id"],) + ((r["name"] or "",) if named else ()) + (hsize(r["size_gb"]), _exp_day(r["expires_at"]),
            M["expired_word"] if _expired(r, now) else "", ",".join(hm.get(r["id"], []))) for r in shown]
    opskit.table(tab, [f"  {M['item'].upper()}"] + ([M["show_fields"]["name"].upper()] if named else []) +
                 ["SIZE", _exp_head(), "", M["hold"].upper() if any(t[-1] for t in tab) else ""])
    if len(rows) > len(shown):
        print(f"  … and {len(rows) - len(shown)} more (`{PROG} list` with the same filters shows them all)")
    print("re-run with --yes to delete")


def _do_delete(con, rows, via):
    me = opskit.identity()
    freed = 0.0
    stores = {}
    for r in rows:
        time.sleep(min(0.3, 0.04 + r["size_gb"] / 2500))
        hs = [h["id"] for h in _active_holds(con, r["id"])]
        con.execute("UPDATE items SET state = 'deleted', deleted_at = ?, deleted_by = ? WHERE id = ?", (opskit.iso(), me["user"], r["id"]))
        con.commit()
        opskit.audit(PROG, "delete", item=r["id"], store=r["store"], group=r["grp"], size_gb=r["size_gb"], holds=hs, via=via)
        print(f"deleted {r['id']}  ({hsize(r['size_gb'])})")
        freed += r["size_gb"]
        stores[r["store"]] = 1
    for name in stores:
        s = _store(con, name)
        used, _ = _store_used(con, s)
        pct = 100 * used / s["capacity_gb"]
        print(f"\nfreed {hsize(freed)}; {name} now {hsize(used)} of {hsize(s['capacity_gb'])} ({pct:.1f}%, target {s['target_pct']:g}%)")
    return 0


def _ids_from(a):
    ids = list(a.ids or [])
    if a.from_file:
        try:
            with open(a.from_file) as f:
                ids += [l.strip() for l in f if l.strip() and not l.lstrip().startswith("#")]
        except OSError as e:
            opskit.die(PROG, f"{a.from_file}: {e.strerror}", 2)
    seen, out = set(), []
    for i in ids:
        if i not in seen:
            seen.add(i); out.append(i)
    if not out:
        opskit.die(PROG, f"nothing to delete (give {M['item']} ids or --from-file)", 2)
    return out


def cmd_delete(a):
    con = _con()
    rows = [_item(con, i) for i in _ids_from(a)]
    _check_delete(con, rows)
    if not a.yes:
        _preview(con, rows, "delete")
        return 1
    return _do_delete(con, rows, "delete")


def cmd_purge(a):
    con = _con()
    if not (a.expired or a.older_than):
        opskit.die(PROG, f"purge needs --{M['expired_opt']} or --older-than (use delete for single {M['items']})", 2)
    rows, _hm, _now = _select(con, a)
    if not rows:
        print(f"nothing matches in {a.store}")
        return 0
    _check_delete(con, rows)
    if not a.yes:
        _preview(con, rows, "purge")
        return 1
    return _do_delete(con, rows, "purge")


def cmd_extend(a):
    con = _con()
    me = opskit.identity()
    _m, ok, want = _roles_ok("extend_roles")
    rows = [_item(con, i) for i in a.ids]
    if a.until:
        try:
            until = dt.datetime.strptime(a.until, "%Y-%m-%d").replace(hour=23, minute=59, second=59, tzinfo=dt.timezone.utc)
        except ValueError:
            opskit.die(PROG, "--until must be YYYY-MM-DD", 2)
    elif a.by:
        until = None
    else:
        opskit.die(PROG, "give --until YYYY-MM-DD or --by DAYS", 2)
    limit = opskit.now() + dt.timedelta(days=int(M["max_extend_days"]))
    for r in rows:
        if r["state"] != "available":
            opskit.die(PROG, f"{r['id']} is {r['state']}", 3)
        if not ok and not (M["extend_own"] and r["owner"] == me["user"]):
            opskit.audit(PROG, "extend", result="denied", item=r["id"])
            opskit.die(PROG, f"permission denied: {r['id']} belongs to {r['owner']} (extending other people's {M['items']} needs {' or '.join(want)})", 13)
    for r in rows:
        base = _ts(r["expires_at"]) or opskit.now()
        new = until or (max(base, opskit.now()) + dt.timedelta(days=int(a.by)))
        if new > limit:
            opskit.die(PROG, f"{r['id']}: can't extend past {limit.strftime('%Y-%m-%d')} ({M['max_extend_days']} days from now)", 2)
        if M.get("delete_scope") and new < max(base, opskit.now()):
            opskit.die(PROG, f"{r['id']}: extend only moves the date later (now {_exp_day(r['expires_at'])})", 2)
        iso_new = new.strftime("%Y-%m-%dT%H:%M:%SZ")
        # In a store with retention locks (items with locked_until) the lock moves to the new date too, as the help says
        # ('cannot be deleted before the extended date'). Pulling the date forward does not shorten the lock (lock = the later of the two).
        lock = r["locked_until"]
        if _store_locks(con, r["store"]) and (not lock or iso_new > lock):
            lock = iso_new
        con.execute("UPDATE items SET expires_at = ?, locked_until = ? WHERE id = ?", (iso_new, lock, r["id"]))
        con.commit()
        opskit.audit(PROG, "extend", item=r["id"], store=r["store"], expires_at=iso_new, previous=r["expires_at"],
                     locked_until=lock, previous_lock=r["locked_until"])
        held = f"; {M['lock_word']} until {_day(lock)}" if lock and lock > opskit.iso() else ""
        print(f"{r['id']} now expires {new.strftime('%Y-%m-%d')}{held}")
    return 0


def _store_locks(con, store):
    """Does this store use retention locks: any item (including deleted ones) with a lock date."""
    return con.execute("SELECT 1 FROM items WHERE store = ? AND locked_until IS NOT NULL LIMIT 1", (store,)).fetchone() is not None


# ── server side ───────────────────────────────────────────────────────
def tick():
    """Service side (not a CLI command): new items arriving on their schedule (uploads, pushes, exports)."""
    started = _ts(os.environ.get("OPSKIT_STARTED_AT") or "")
    p = os.path.join(opskit.STATE_ROOT, PROG, "store.db")
    if not started or not os.path.exists(p):
        return
    con = _con()
    try:
        due = con.execute("SELECT * FROM incoming WHERE delivered = 0 ORDER BY after_s, id").fetchall()
    except sqlite3.OperationalError:
        return
    now = opskit.now()
    for r in due:
        if now < started + dt.timedelta(seconds=r["after_s"]):
            break
        it = json.loads(r["item"])
        keep = it.pop("retention_days", None)
        new_holds = it.pop("holds", None) or []
        it.update({"created_at": opskit.iso(now), "last_used_at": opskit.iso(now), "state": "available",
                   "expires_at": opskit.iso(now + dt.timedelta(days=keep)) if keep is not None else None})
        it.setdefault("labels", "{}")
        if isinstance(it["labels"], dict):
            it["labels"] = json.dumps(it["labels"])
        cols = list(it)
        con.execute(f"INSERT OR IGNORE INTO items ({','.join(cols)}) VALUES ({','.join('?' * len(cols))})", [it[c] for c in cols])
        con.execute("UPDATE incoming SET delivered = 1 WHERE id = ?", (r["id"],))
        con.commit()
        opskit.audit(PROG, M["upload_action"], actor=r["actor"], host=r["host"], item=it["id"], store=it["store"], size_gb=it["size_gb"])
        # incoming items may carry holds (job leases etc.): item["holds"] = [{"id", "kind", "label", "ref", "reason", "placed_by"}]
        # an existing hold id is only linked.
        for h in new_holds:
            if con.execute("SELECT 1 FROM holds WHERE id = ?", (h["id"],)).fetchone() is None:
                con.execute("INSERT INTO holds (id, kind, label, ref, reason, placed_by, placed_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
                            (h["id"], h.get("kind") or "hold", h.get("label"), h.get("ref"), h.get("reason"), h.get("placed_by") or r["actor"],
                             opskit.iso(now)))
            con.execute("INSERT INTO hold_items (hold_id, item_id) VALUES (?, ?)", (h["id"], it["id"]))
            con.commit()
            opskit.audit(PROG, M.get("hold_action") or "hold-sync", actor=h.get("placed_by") or r["actor"], host=h.get("host") or r["host"],
                         hold=h["id"], state="placed", items=1, item=it["id"])


# ── cli ───────────────────────────────────────────────────────────────
def _filters(s, store_required=False):
    if store_required:
        s.add_argument("store", metavar=M["store"].upper())
    else:
        s.add_argument("store", nargs="?", metavar=M["store"].upper())
    s.add_argument(f"--{M['group_opt']}", dest="grp", metavar=M["group_opt"].upper(),
                   help=(f"only {M['items']} under this {M['group']}" if M["group_match"] == "prefix" else f"only this {M['group']}"))
    s.add_argument(f"--{M['kind_opt']}", dest="kind", metavar=M["kind_opt"].upper(),
                   help=(", ".join(M["kinds"]) if M["kinds"] else None))
    s.add_argument("--owner", help=M.get("owner_help") or f"only this {M['owner']}")
    s.add_argument(f"--{M['expired_opt']}", dest="expired", action="store_true",
                   help=M["expired_help"] or f"only {M['items']} past their expiry")
    s.add_argument("--older-than", metavar="AGE", help=M.get("older_help") or "created more than AGE ago (12h, 30d, 6w)")
    s.add_argument("--label", action="append", metavar="K[=V]", help="has this label (repeatable)")
    s.add_argument("--match", metavar="GLOB", help=f"id or name matches GLOB")
    s.add_argument(f"--{M['hold']}".replace(" ", "-"), dest="hold", metavar="ID", help=f"only {M['items']} under this {M['hold']}")


def main(argv=None):
    if os.environ.get("OPSKIT_TICK") == "1":
        tick()
        return 0
    p = argparse.ArgumentParser(prog=PROG, description=M["title"], epilog=M["epilog"] or None,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    cmds = [M["stores_cmd"], "usage", "list", "show", M["holds_cmd"], "delete", "purge", "extend"]
    sub = p.add_subparsers(dest="cmd", required=True, metavar="{" + ",".join(cmds) + "}")
    s = sub.add_parser(M["stores_cmd"], help=f"{M['stores']} with usage against their target"); s.set_defaults(fn=cmd_stores)
    s = sub.add_parser("usage", help=f"usage of a {M['store']}: what has {M['expired_word']}, what is {M['on_hold']}")
    s.add_argument("store", nargs="?", metavar=M["store"].upper())
    s.add_argument("--by", choices=["group", "kind", "owner"], default="group", help=f"break down by {M['group']} (default), {M['kind']} or {M['owner']}")
    s.set_defaults(fn=cmd_usage)
    s = sub.add_parser("list", help=f"list {M['items']}")
    _filters(s)
    s.add_argument("--sort", choices=["size", "created", "expires", "used", "id"])
    s.add_argument("--limit", type=int, help=f"rows per page (default {M['page_size']})")
    s.add_argument("--page", type=int)
    s.add_argument("--all", action="store_true", help="no paging")
    s.add_argument("-q", "--quiet", action="store_true", help="print ids only (all matches)")
    s.add_argument("--format", choices=["table", "csv", "json"], default="table")
    s.set_defaults(fn=cmd_list)
    s = sub.add_parser("show", help=f"details of one {M['item']}"); s.add_argument("id"); s.set_defaults(fn=cmd_show)
    s = sub.add_parser(M["holds_cmd"], help=f"{M['holds']} on {M['items']}")
    s.add_argument("hold", nargs="?", metavar=M["hold"].upper().replace(" ", "-"), help=f"show one {M['hold']} and what it covers")
    s.add_argument("--store", help=f"only {M['holds']} on this {M['store']}")
    s.add_argument("--all", action="store_true", help="include released ones")
    s.set_defaults(fn=cmd_holds)
    s = sub.add_parser("delete", help=f"delete {M['items']} (frees their space right away)")
    s.add_argument("ids", nargs="*", metavar="ID"); s.add_argument("--from-file", metavar="FILE", help="ids, one per line")
    s.add_argument("--yes", action="store_true", help="do it (otherwise only lists what would go)")
    s.set_defaults(fn=cmd_delete)
    s = sub.add_parser("purge", help=f"delete every {M['item']} in a {M['store']} that matches the filters")
    _filters(s, store_required=True)
    s.add_argument("--yes", action="store_true", help="do it (otherwise only lists what would go)")
    s.set_defaults(fn=cmd_purge)
    s = sub.add_parser("extend", help=f"move {M['items']}' expiry")
    s.add_argument("ids", nargs="+", metavar="ID")
    g = s.add_mutually_exclusive_group()
    g.add_argument("--until", metavar="YYYY-MM-DD"); g.add_argument("--by", type=int, metavar="DAYS", help="days past the current expiry")
    s.set_defaults(fn=cmd_extend)
    a = p.parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    opskit.run(main)
