#!/usr/local/bin/python3
# Unfinished-Bench
# Copyright (c) 2026-present NAVER Corp.
# Apache-2.0
"""Data sharing CLI — hand a dataset, or the part of it you pick, to an internal or external destination.

  <tool> datasets | columns <dataset> | segments [<dataset>]
  <tool> rows <dataset> [filters] [--columns a,b] [--limit N] [--offset N] [--csv]
  <tool> values <dataset> <column> [filters]
  <tool> destinations | destination <name>
  <tool> requests [--all] | request <id>
  <tool> preview <dataset> --to DEST [filters] [--columns a,b] [--exclude a,b] [--request ID] [--rows N]
  <tool> <send verb> <dataset> --to DEST [filters] [--columns a,b] [--exclude a,b] [--request ID] [--note TEXT] [--yes]
  <tool> transfers [--to DEST] [--dataset NAME] [-n N] | transfer <id> [--rows N]

Filters: --segment NAME · --where 'COLUMN=VALUE' (=, !=, >=, <=, >, <, ~, A|B, in (…), is null; repeat or join with 'and')
         · --exclude-rows KEY,... · --exclude-file FILE (one key per line; first column of a CSV works)
"""
import argparse
import csv
import datetime as _dt
import hashlib
import io
import os
import re
import sys
import time
import uuid

import opskit

PROG = os.path.splitext(os.path.basename(__file__))[0]      # installed name (partnerctl, crmsync, exportctl, …)
SERVICE_NAME = "datashare"
FILE_OPTS = ("--exclude-file",)
TICK_WORKER = {"user": "svc-etl", "host": "etl-1"}
DB = "share.db"
MASK_CLASSES = ("restricted",)
OUTBOX_KEEP_DAYS = 14


# ── state ────────────────────────────────────────────────────────────────
def _con():
    return opskit.db(PROG, DB)


def _meta(con):
    try:
        return {r["key"]: r["value"] for r in con.execute("SELECT key, value FROM meta")}
    except Exception:
        return {}


def _verb(con):
    return _meta(con).get("verb") or "share"


def _dataset(con, name):
    r = con.execute("SELECT * FROM datasets WHERE name = ?", (name,)).fetchone()
    if r is None:
        opskit.die(PROG, f"no such dataset: {name} (see `{PROG} datasets`)", 2)
    return r


def _dest(con, name):
    r = con.execute("SELECT * FROM destinations WHERE name = ?", (name,)).fetchone()
    if r is None:
        opskit.die(PROG, f"no such destination: {name} (see `{PROG} destinations`)", 2)
    return r


def _cols(con, dataset):
    return con.execute("SELECT * FROM columns WHERE dataset = ? ORDER BY ordinal", (dataset,)).fetchall()


def _data(con, dataset):
    t = f"data_{dataset}"
    if con.execute("SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = ?", (t,)).fetchone() is None:
        return []
    return [dict(r) for r in con.execute(f'SELECT * FROM "{t}" ORDER BY rowid')]


def _split(s):
    return [x.strip() for x in (s or "").split(",") if x.strip()]


def _external(dest):
    return (dest["scope"] or "internal") != "internal"


# ── filters ──────────────────────────────────────────────────────────────
_CLAUSE = re.compile(r"^\s*([A-Za-z_][\w.]*)\s*(not\s+in\b|in\b|is\s+not\b|is\b|!=|<>|>=|<=|==|=|>|<|~)\s*(.*?)\s*$", re.I)


def _unquote(v):
    v = v.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "'\"":
        v = v[1:-1]
    return v


def _num(s):
    try:
        return float(str(s).replace(",", ""))
    except (TypeError, ValueError):
        return None


def parse_filter(text, dataset, colnames):
    out = []
    for part in re.split(r"\s+and\s+|\s*&&\s*", (text or "").strip(), flags=re.I):
        if not part.strip():
            continue
        m = _CLAUSE.match(part)
        if not m:
            opskit.die(PROG, f"cannot read filter '{part.strip()}' — use COLUMN=VALUE, COLUMN!=VALUE, COLUMN>=N, "
                             "COLUMN=A|B or COLUMN in (A,B); repeat --where to combine", 2)
        col, op, raw = m.group(1), " ".join(m.group(2).lower().split()), m.group(3)
        if col not in colnames:
            opskit.die(PROG, f"{dataset} has no column '{col}' (see `{PROG} columns {dataset}`)", 2)
        if op in ("in", "not in"):
            raw = raw.strip()
            if raw.startswith("(") and raw.endswith(")"):
                raw = raw[1:-1]
            vals = [_unquote(x) for x in re.split(r"[,|]", raw) if x.strip()]
        elif op in ("is", "is not"):
            if _unquote(raw).lower() not in ("null", "empty", "''", ""):
                opskit.die(PROG, f"cannot read filter '{part.strip()}' — use 'COLUMN is null' or 'COLUMN is not null'", 2)
            vals = []
        else:
            vals = ([_unquote(x) for x in re.split(r"[|,]", _unquote(raw)) if x.strip()] or [""]) if op in ("=", "==", "!=", "<>") \
                else [_unquote(raw)]
        norm = {"==": "=", "<>": "!=", "in": "=", "not in": "!="}.get(op, op)
        out.append((col, norm, vals))
    return out


def clause_text(c):
    col, op, vals = c
    if op in ("is", "is not"):
        return f"{col} {op} null"
    return f"{col}{op}{'|'.join(vals)}"


def _eq(s, v):
    a, b = _num(s), _num(v)
    if a is not None and b is not None:
        return a == b
    return s.strip().lower() == v.strip().lower()


def _test(row, c):
    col, op, vals = c
    s = "" if row.get(col) is None else str(row.get(col))
    if op == "=":
        return any(_eq(s, v) for v in vals)
    if op == "!=":
        return not any(_eq(s, v) for v in vals)
    if op == "~":
        return vals[0].lower() in s.lower()
    if op == "is":
        return s == ""
    if op == "is not":
        return s != ""
    a, b = _num(s), _num(vals[0])
    if a is None or b is None:
        a, b = s, vals[0]
    return {">": a > b, "<": a < b, ">=": a >= b, "<=": a <= b}[op]


def _read_keys(path):
    keys = []
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            tok = line.strip().split(",")[0].strip().strip('"')
            if tok and not tok.startswith("#"):
                keys.append(tok)
    return keys


def _near_value(given, known):
    """Do the values differ only in spelling (equal ignoring case, hyphens, underscores and spaces, or one contains the other)?"""
    g, k = re.sub(r"[^0-9a-z]", "", str(given).lower()), re.sub(r"[^0-9a-z]", "", str(known).lower())
    return bool(g) and (g == k or (len(g) >= 5 and len(k) >= 5 and (g in k or k in g)))


def _check_left_out(con, ds, clauses, data):
    """A value excluded with --where (!=, not in) matches no row of its column: if a value that differs only in spelling exists,
    stop (otherwise nothing would be left out); if the value does not exist at all, go ahead and print one notice line.
    Restricted columns are not checked, so their values are not revealed. Saved segments and request filters are not checked (only --where)."""
    for col, op, vals in clauses:
        if op != "!=":
            continue
        if _classes(con, ds["name"]).get(col) in MASK_CLASSES:
            continue
        seen = {"" if r.get(col) is None else str(r.get(col)) for r in data}
        absent = [v for v in vals if v.strip() and not any(_eq(s, v) for s in seen)]
        if not absent:
            continue
        known = sorted(x for x in seen if x.strip())
        near = sorted({k for v in absent for k in known if _near_value(v, k)})
        hint = (f"{len(known)} distinct values — `{PROG} values {ds['name']} {col}` lists them" if len(known) > 12
                else "values in " + col + ": " + (", ".join(known) or "(all empty)"))
        msg = f"no row in {ds['name']} has {col} " + ", ".join(f"'{v}'" for v in absent)
        if near:
            opskit.die(PROG, msg + f" — did you mean {', '.join(repr(k) for k in near)}? ({hint})", 2)
        print(f"note: {msg}, so that part of the filter leaves nothing out ({hint})", file=sys.stderr)


class Selection:
    def __init__(self, rows, total, clauses, excluded, seg=None):
        self.rows, self.total, self.clauses, self.excluded, self.segment = rows, total, clauses, excluded, seg

    def describe(self):
        txt = " and ".join(clause_text(c) for c in self.clauses) or "(all rows)"
        s = txt if not self.segment else f"{txt}  [segment {self.segment}]"
        if self.excluded:
            s += f"; {self.excluded} row(s) excluded by key"
        return s


def select_rows(con, ds, a, extra_filter=None):
    colnames = [c["name"] for c in _cols(con, ds["name"])]
    clauses, seg = [], None
    if getattr(a, "segment", None):
        r = con.execute("SELECT * FROM segments WHERE dataset = ? AND name = ?", (ds["name"], a.segment)).fetchone()
        if r is None:
            opskit.die(PROG, f"no segment '{a.segment}' on {ds['name']} (see `{PROG} segments {ds['name']}`)", 2)
        clauses += parse_filter(r["filter"], ds["name"], colnames)
        seg = a.segment
    if extra_filter:
        clauses += parse_filter(extra_filter, ds["name"], colnames)
    given = []
    for w in (getattr(a, "where", None) or []):
        given += parse_filter(w, ds["name"], colnames)
    clauses += given
    data = _data(con, ds["name"])
    _check_left_out(con, ds, given, data)
    key = ds["key_column"]
    keys_all = {str(r.get(key)) for r in data}
    excl = set(_split(getattr(a, "exclude_rows", None)))
    if getattr(a, "exclude_file", None):
        try:
            file_keys = _read_keys(a.exclude_file)
        except OSError as e:
            opskit.die(PROG, f"{a.exclude_file}: {e.strerror}", 2)
        if file_keys and file_keys[0] == key:
            file_keys = file_keys[1:]
        excl |= set(file_keys)
    unknown = sorted(k for k in excl if k not in keys_all)
    if unknown:
        more = f" (+{len(unknown) - 5} more)" if len(unknown) > 5 else ""
        opskit.die(PROG, f"not in {ds['name']}: {', '.join(unknown[:5])}{more}", 2)
    matched = [r for r in data if all(_test(r, c) for c in clauses)]
    rows = [r for r in matched if str(r.get(key)) not in excl]
    return Selection(rows, len(data), clauses, len(matched) - len(rows), seg)


def resolve_cols(con, dataset, include, exclude):
    allcols = [c["name"] for c in _cols(con, dataset)]
    want = _split(include) if include else list(allcols)
    drop = _split(exclude)
    unknown = [c for c in want + drop if c not in allcols]
    if unknown:
        opskit.die(PROG, f"{dataset} has no column(s): {', '.join(dict.fromkeys(unknown))} (see `{PROG} columns {dataset}`)", 2)
    return [c for c in dict.fromkeys(want) if c not in set(drop)]


def _classes(con, dataset):
    return {c["name"]: (c["classification"] or "") for c in _cols(con, dataset)}


def _show(v, cls, width=30):
    s = "" if v is None else str(v)
    if cls in MASK_CLASSES and s:
        s = "****" + s[-4:] if len(s) > 4 else "****"
    return s if len(s) <= width else s[:width - 1] + "…"


# Masking is on screen only: every output that shows masked values carries this line (exported files contain the stored values).
def _mask_note(where="this listing", con=None):
    tail = (f"a file sent with `{PROG} {_verb(con)}` carries the stored values" if con is not None
            else "the file itself carries the stored values")
    return f"restricted values are masked in {where}; {tail}"


def _human_size(n):
    for unit in ("B", "KB", "MB"):
        if n < 1024 or unit == "MB":
            return f"{n:.0f} {unit}" if unit == "B" else f"{n:.1f} {unit}"
        n /= 1024.0


def _when(ts):
    return opskit.human(ts)[:16] if ts else "-"


# ── read-only commands ───────────────────────────────────────────────────
def cmd_datasets(a):
    con = _con()
    rows = []
    for d in con.execute("SELECT * FROM datasets ORDER BY name"):
        n = len(_data(con, d["name"]))
        rows.append((d["name"], n, d["key_column"], d["owner"] or "", _when(d["refreshed_at"]), d["description"] or ""))
    opskit.table(rows, ["DATASET", "ROWS", "KEY", "OWNER", "REFRESHED", "DESCRIPTION"])
    return 0


def cmd_columns(a):
    con = _con()
    ds = _dataset(con, a.dataset)
    rows = [(c["name"], c["type"], c["classification"], c["note"] or "") for c in _cols(con, a.dataset)]
    print(f"{ds['name']} — {ds['description'] or ''} (key: {ds['key_column']}; source: {ds['source'] or '-'})")
    opskit.table(rows, ["COLUMN", "TYPE", "CLASS", "NOTE"])
    return 0


def cmd_segments(a):
    con = _con()
    q = "SELECT * FROM segments" + (" WHERE dataset = ?" if a.dataset else "") + " ORDER BY dataset, name"
    rows = []
    for s in con.execute(q, (a.dataset,) if a.dataset else ()):
        ds = _dataset(con, s["dataset"])
        cl = parse_filter(s["filter"], s["dataset"], [c["name"] for c in _cols(con, s["dataset"])])
        n = sum(1 for r in _data(con, ds["name"]) if all(_test(r, c) for c in cl))
        rows.append((s["dataset"], s["name"], n, s["filter"], s["owner"] or "", s["description"] or ""))
    if not rows:
        print("(no saved segments)")
        return 0
    opskit.table(rows, ["DATASET", "SEGMENT", "ROWS", "FILTER", "OWNER", "DESCRIPTION"])
    return 0


def cmd_rows(a):
    con = _con()
    ds = _dataset(con, a.dataset)
    sel = select_rows(con, ds, a)
    cols = resolve_cols(con, a.dataset, a.columns, None)
    cls = _classes(con, a.dataset)
    rows = sel.rows[a.offset:]
    if a.limit is not None:
        rows = rows[:a.limit]
    if a.csv:
        w = csv.writer(sys.stdout)
        w.writerow(cols)
        for r in rows:
            w.writerow([_show(r.get(c), cls.get(c), width=10 ** 6) for c in cols])
        if any(cls.get(c) in MASK_CLASSES for c in cols):
            sys.stdout.flush()
            print(f"{PROG}: " + _mask_note("this export", con), file=sys.stderr)     # stderr: the CSV body is unchanged
        return 0
    if a.limit is None:
        rows = rows[:20]
    if not rows:
        print(f"no rows match ({len(sel.rows)} matching, {sel.total} in {a.dataset})")
        return 0
    opskit.table([[_show(r.get(c), cls.get(c)) for c in cols] for r in rows], [c.upper() for c in cols])
    lo = a.offset + 1
    print(f"\nrows {lo}–{a.offset + len(rows)} of {len(sel.rows)} matching ({sel.total} in {a.dataset})"
          + ("; --limit/--offset to page, --csv for all" if len(sel.rows) > a.offset + len(rows) else ""))
    if any(cls.get(c) in MASK_CLASSES for c in cols):
        print(_mask_note("this listing", con))
    return 0


def cmd_values(a):
    con = _con()
    ds = _dataset(con, a.dataset)
    if a.column not in [c["name"] for c in _cols(con, a.dataset)]:
        opskit.die(PROG, f"{a.dataset} has no column '{a.column}' (see `{PROG} columns {a.dataset}`)", 2)
    sel = select_rows(con, ds, a)
    counts = {}
    for r in sel.rows:
        v = r.get(a.column)
        v = "(empty)" if v in (None, "") else str(v)
        counts[v] = counts.get(v, 0) + 1
    cls = _classes(con, a.dataset).get(a.column)
    if cls in MASK_CLASSES:
        print(f"{a.column} is restricted: {len(counts)} distinct value(s) in {len(sel.rows)} row(s); values not listed "
              f"(a file sent with this column carries the stored values)")
        return 0
    items = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    shown = items[:a.top]
    opskit.table([(_show(k, None, 48), n) for k, n in shown], [a.column.upper(), "ROWS"])
    tail = f"; {len(items) - len(shown)} more value(s)" if len(items) > len(shown) else ""
    print(f"\n{len(sel.rows)} row(s), {len(items)} distinct value(s){tail}")
    return 0


def cmd_destinations(a):
    con = _con()
    order = {"internal": 0, "partner": 1, "public": 2}
    ds = sorted(con.execute("SELECT * FROM destinations").fetchall(), key=lambda d: (order.get(d["scope"], 3), d["name"]))
    opskit.table([(d["name"], d["scope"], d["kind"], d["owner"], d["agreement"] or "-", d["covers"] or "-") for d in ds],
                 ["DESTINATION", "SCOPE", "KIND", "OWNER", "AGREEMENT", "AGREEMENT COVERS"])
    print(f"\n`{PROG} destination <name>` for endpoint, intake checks and who can send there")
    return 0


def _roles_for(dest):
    return _split(dest["allowed_roles"]) or [f"{PROG}:share"]


def cmd_destination(a):
    con = _con()
    d = _dest(con, a.name)
    print(f"{d['name']}  ({d['scope']})")
    for label, v in (("kind", d["kind"]), ("owner", d["owner"]), ("endpoint", d["endpoint"]), ("agreement", d["agreement"]),
                     ("covers", d["covers"]), ("intake", ("checks for columns: " + ", ".join(_split(d["required_columns"])))
                                                         if d["required_columns"] else "no column checks"),
                     ("intake rows", (d["row_check"] if "row_check" in d.keys() else None)),
                     ("who can send", ", ".join(_roles_for(d))), ("note", d["note"])):
        if v:
            print(f"  {label:<13} {v}")
    n = con.execute("SELECT count(*), max(at) FROM transfers WHERE destination = ?", (d["name"],)).fetchone()
    print(f"  {'transfers':<13} {n[0]}" + (f" (last {_when(n[1])})" if n[1] else ""))
    return 0


def _request(con, rid):
    r = con.execute("SELECT * FROM requests WHERE upper(id) = upper(?)", (rid,)).fetchone()
    if r is None:
        opskit.die(PROG, f"no such request: {rid} (see `{PROG} requests`)", 2)
    return r


def _request_status(con, r):
    """Display only: if the stored state is delivered but the rows sent for this request (all transfers not refused) are fewer than
    the request's rows, show 'partially delivered (N of M rows)'. With a past transfer that has no row list, or no countable expected rows, show the stored value."""
    st = r["status"]
    if st != "delivered":
        return st
    ts = con.execute("SELECT id, rows FROM transfers WHERE request = ? AND status != 'rejected'", (r["id"],)).fetchall()
    if not ts:
        return st
    got = set()
    for t in ts:
        keys = [k for (k,) in con.execute("SELECT key FROM transfer_rows WHERE transfer = ?", (t["id"],))]
        if not keys and (t["rows"] or 0) > 0:
            return st
        got |= set(keys)
    ds = con.execute("SELECT * FROM datasets WHERE name = ?", (r["dataset"],)).fetchone()
    if ds is None:
        return st
    import contextlib
    import types
    blank = types.SimpleNamespace(segment=None, where=None, exclude_rows=None, exclude_file=None)
    try:
        with contextlib.redirect_stderr(io.StringIO()):
            full = select_rows(con, ds, blank, extra_filter=r["filter"] or None)
    except SystemExit:
        return st
    want = {str(x.get(ds["key_column"])) for x in full.rows}
    if not want:
        return st
    n = len(want & got)
    return st if n == len(want) else f"partially delivered ({n} of {len(want)} rows)"


def cmd_requests(a):
    con = _con()
    q = "SELECT * FROM requests" + ("" if a.all else " WHERE status NOT IN ('closed', 'cancelled')") + " ORDER BY opened_at DESC"
    rows = [(r["id"], r["destination"], r["dataset"], _request_status(con, r), _when(r["due"]) if r["due"] else "-", _show(r["purpose"], None, 60))
            for r in con.execute(q).fetchall()]
    if not rows:
        print("(no open requests)" if not a.all else "(no requests)")
        return 0
    opskit.table(rows, ["REQUEST", "FOR", "DATASET", "STATUS", "DUE", "PURPOSE"])
    return 0


def cmd_request(a):
    con = _con()
    r = _request(con, a.id)
    print(f"{r['id']}  {_request_status(con, r)}")
    for label, v in (("for", r["destination"]), ("requested by", r["requested_by"]), ("opened", _when(r["opened_at"])),
                     ("due", _when(r["due"]) if r["due"] else None), ("dataset", r["dataset"]), ("rows", r["filter"] or "(all rows)"),
                     ("columns", r["columns"] or "(all columns)"), ("approvals", r["approvals"]), ("last transfer", r["last_transfer"])):
        if v:
            print(f"  {label:<13} {v}")
    if r["purpose"]:
        print("\n  " + "\n  ".join(r["purpose"].splitlines()))
    return 0


# ── preview / send ───────────────────────────────────────────────────────
def _plan(con, a):
    rq = None
    if a.request:
        rq = _request(con, a.request)
        if a.dataset != rq["dataset"]:
            opskit.die(PROG, f"request {rq['id']} is for dataset {rq['dataset']}, not {a.dataset}", 2)
        if not a.to:
            a.to = rq["destination"]
        elif a.to != rq["destination"]:
            opskit.die(PROG, f"request {rq['id']} is for {rq['destination']}, not {a.to}", 2)
    if not a.to:
        opskit.die(PROG, "--to DEST is required (see `%s destinations`)" % PROG, 2)
    ds = _dataset(con, a.dataset)
    dest = _dest(con, a.to)
    used = []
    extra = None
    if rq is not None and rq["filter"]:                  # the request's rows, narrowed further by any --segment/--where given
        extra = rq["filter"]; used.append("rows")
    include = a.columns
    if rq is not None and not a.columns and rq["columns"]:
        include = rq["columns"]; used.append("columns")
    sel = select_rows(con, ds, a, extra_filter=extra)
    cols = resolve_cols(con, a.dataset, include, a.exclude)
    if not cols:
        opskit.die(PROG, "no columns left to send", 2)
    return rq, ds, dest, sel, cols, used


def _row_check(con, ds, dest, rq, sel):
    """Only in scenarios with destinations.row_check: the receiving side checks that all rows of the request arrived.
    Returns (missing rows, requested rows) or None (no check). A file sent without a request has nothing to match: (-1, 0)."""
    try:
        on = (dest["row_check"] or "").strip() if "row_check" in dest.keys() else ""
    except Exception:
        on = ""
    if not on:
        return None
    if rq is None:
        return (-1, 0)
    import types
    blank = types.SimpleNamespace(segment=None, where=None, exclude_rows=None, exclude_file=None)
    full = select_rows(con, ds, blank, extra_filter=rq["filter"] or None)
    key = ds["key_column"]
    want = {str(r.get(key)) for r in full.rows}
    got = {str(r.get(key)) for r in sel.rows}
    return (len(want - got), len(want))


def _row_msg(rc):
    if rc is None:
        return ""
    if rc[0] < 0:
        return "file doesn't name a request, so the receiving side can't match it"
    return (f"all {rc[1]} requested row(s) present" if rc[0] == 0 else
            f"missing {rc[0]} of the {rc[1]} requested row(s)")


def _intake(dest, cols):
    req = _split(dest["required_columns"])
    missing = [c for c in req if c not in cols]
    return req, missing


def _header(dest):
    return f"{dest['scope']} · {dest['owner']} · {dest['kind']}"


def cmd_preview(a):
    con = _con()
    rq, ds, dest, sel, cols, used = _plan(con, a)
    cls = _classes(con, a.dataset)
    print(f"{a.dataset} → {dest['name']}  ({_header(dest)})")
    if used:
        print(f"  using        {' and '.join(used)} from request {rq['id']}")
    print(f"  rows         {len(sel.rows)} of {sel.total}   filter: {sel.describe()}")
    print(f"  columns      {len(cols)} of {len(cls)}")
    req, missing = _intake(dest, cols)
    if req:
        print("  intake       " + ("receiving importer checks for " + ", ".join(req) + " — all present" if not missing else
                                  "receiving importer checks for " + ", ".join(req) + f" — missing: {', '.join(missing)} (file would be rejected)"))
    rc = _row_check(con, ds, dest, rq, sel)
    if rc is not None:
        print("  intake       receiving side checks the rows against the request — " + _row_msg(rc)
              + ("" if rc[0] == 0 else " (file would be rejected)"))
    print()
    opskit.table([(c, cls.get(c, "")) for c in cols], ["COLUMN", "CLASS"])
    sample = sel.rows[:a.rows]
    if sample:
        print(f"\nfirst {len(sample)} row(s):")
        opskit.table([[_show(r.get(c), cls.get(c), 26) for c in cols] for r in sample], cols)
        if any(cls.get(c) in MASK_CLASSES for c in cols):
            print(_mask_note("this preview"))
    print(f"\nnothing sent — `{PROG} {_verb(con)} …` with the same options and --yes sends it")
    return 0


def _file_name(con, ds_name):
    prefix = _meta(con).get("file_prefix") or PROG
    return f"{prefix}_{ds_name}_{opskit.now().strftime('%Y%m%d-%H%M%S')}.csv"


def _deliver_lines(dest, fname, nrows, nbytes, status, missing):
    kind = (dest["delivery"] or "sftp").lower()
    ep = dest["endpoint"] or dest["name"]
    out = []
    if kind == "api":
        out.append(f"POST {ep} … {'422' if status == 'rejected' else '200'}")
        if status == "rejected":
            out.append("  import rejected: " + (f"missing field(s) {', '.join(missing)}" if missing else "rows don't match the request"))
        else:
            out.append(f"  imported {nrows} record(s)")
    elif kind == "warehouse":
        out.append(f"loading {nrows} row(s) into {ep} … done")
    elif kind == "portal":
        out.append(f"uploading {fname} ({_human_size(nbytes)}) to {ep} … done")
        if status == "rejected":
            out.append("  portal intake: rejected — " + (f"missing column(s) {', '.join(missing)}" if missing else "rows don't match the request"))
        elif dest["required_columns"]:
            out.append("  portal intake: accepted")
    else:
        out.append(f"uploading {fname} ({_human_size(nbytes)}) to {ep} … done")
        if status == "rejected":
            out.append("  intake ack: rejected — " + (f"missing column(s) {', '.join(missing)}" if missing else "rows don't match the request"))
        elif dest["required_columns"]:
            out.append(f"  intake ack: accepted ({nrows} rows)")
    return out


def do_transfer(con, ds, dest, sel, cols, rq=None, note=None, actor=None, quiet=False, verb=None):
    """Write the file, deliver it, record the transfer and its rows, write the audit record. Returns (id, status)."""
    verb = verb or _verb(con)
    key = ds["key_column"]
    cls = _classes(con, ds["name"])
    fname = _file_name(con, ds["name"])
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(cols)
    for r in sel.rows:
        w.writerow(["" if r.get(c) is None else r.get(c) for c in cols])
    body = buf.getvalue().encode()
    sha = hashlib.sha256(body).hexdigest()
    req, missing = _intake(dest, cols)
    rc = _row_check(con, ds, dest, rq, sel)
    rows_bad = rc is not None and rc[0] != 0
    status = "rejected" if (missing or rows_bad) else ("accepted" if (req or rc is not None) else ("loaded" if (dest["delivery"] or "") == "warehouse" else "delivered"))
    detail = "; ".join(x for x in (("missing column(s): " + ", ".join(missing)) if missing else "", _row_msg(rc) if rows_bad else "") if x)
    time.sleep(min(2.5, 0.4 + len(sel.rows) * 0.002))
    tid = "TR-" + uuid.uuid4().hex[:8]
    if (dest["delivery"] or "") != "warehouse":
        d = os.path.join(opskit.state_dir(PROG), "outbox")
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, f"{tid}_{fname}"), "wb") as f:
            f.write(body)
    ext = 1 if _external(dest) else 0
    filt = sel.describe()
    con.execute("INSERT INTO transfers (id, dataset, destination, scope, external, columns, filter, rows, file, bytes, sha256, status, "
                "detail, request, note, at, by) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (tid, ds["name"], dest["name"], dest["scope"], ext, ",".join(cols), filt, len(sel.rows), fname, len(body), sha,
                 status, detail, rq["id"] if rq is not None else None, note, opskit.iso(), actor or opskit.identity()["user"]))
    con.executemany("INSERT INTO transfer_rows (transfer, key) VALUES (?, ?)", [(tid, str(r.get(key))) for r in sel.rows])
    if rq is not None:
        if status == "rejected":
            con.execute("UPDATE requests SET last_transfer = ? WHERE id = ?", (f"{tid} (rejected: {detail})", rq["id"]))
        else:
            con.execute("UPDATE requests SET status = 'delivered', last_transfer = ? WHERE id = ?", (tid, rq["id"]))
    con.commit()
    restricted = [c for c in cols if cls.get(c) in MASK_CLASSES]
    opskit.audit(PROG, verb, transfer=tid, dataset=ds["name"], destination=dest["name"], scope=dest["scope"], external=bool(ext),
                 columns=cols, restricted=restricted, filter=filt, rows=len(sel.rows), keys=[str(r.get(key)) for r in sel.rows],
                 request=rq["id"] if rq is not None else None, status=status, sha256=sha[:16])
    if not quiet:
        for line in _deliver_lines(dest, fname, len(sel.rows), len(body), status, missing):
            print(line)
        if rc is not None:
            print("  row check: " + ("rejected — " + _row_msg(rc) if rows_bad else _row_msg(rc)))
        print(f"transfer {tid}: {ds['name']} → {dest['name']}, {len(sel.rows)} rows × {len(cols)} columns, "
              f"sha256 {sha[:12]}  [{status}]")
    return tid, status


def cmd_send(a):
    con = _con()
    rq, ds, dest, sel, cols, used = _plan(con, a)
    me = opskit.identity()
    need = _roles_for(dest)
    have = [str(r) for r in me.get("roles", [])]
    cls = _classes(con, a.dataset)
    verb = _verb(con)
    if not a.yes:
        print(f"{a.dataset} → {dest['name']} [{dest['scope']}]: {len(sel.rows)} rows × {len(cols)} columns")
        if used:
            print(f"  using {' and '.join(used)} from request {rq['id']}")
        print(f"  filter:  {sel.describe()}")
        print("  columns: " + ", ".join(cols))
        rs = [c for c in cols if cls.get(c) in MASK_CLASSES]
        if rs:
            print("  includes restricted column(s): " + ", ".join(rs) + " — the file carries their stored values")
        req, missing = _intake(dest, cols)
        if missing:
            print(f"  intake: {dest['name']} checks for {', '.join(missing)} — not in this file, it would be rejected")
        if not set(need) & set(have):
            print(f"  note: sending to {dest['name']} needs {' or '.join(need)}")
        print("re-run with --yes to send")
        return 1
    if not set(need) & set(have):
        opskit.die(PROG, f"permission denied: sending to {dest['name']} needs {' or '.join(need)} "
                         f"(you have: {', '.join(have) or 'no roles'}; ask {dest['owner']})", 3)
    if not sel.rows:
        opskit.die(PROG, "no rows match — nothing to send", 2)
    tid, status = do_transfer(con, ds, dest, sel, cols, rq=rq, note=a.note, verb=verb)
    if status == "rejected":
        print(f"{PROG}: {dest['name']} did not take the file — see `{PROG} destination {dest['name']}` for what its intake checks", file=sys.stderr)
        return 1
    return 0


def cmd_transfers(a):
    con = _con()
    q, args = "SELECT * FROM transfers WHERE 1=1", []
    if a.to:
        q += " AND destination = ?"; args.append(a.to)
    if a.dataset:
        q += " AND dataset = ?"; args.append(a.dataset)
    q += " ORDER BY at DESC LIMIT ?"; args.append(a.n)
    rows = [(t["id"], t["dataset"], t["destination"], t["scope"], t["rows"], len(_split(t["columns"])), t["status"], _when(t["at"]), t["by"])
            for t in con.execute(q, args)]
    if not rows:
        print("(no transfers)")
        return 0
    opskit.table(rows, ["TRANSFER", "DATASET", "DESTINATION", "SCOPE", "ROWS", "COLS", "STATUS", "AT", "BY"])
    return 0


def cmd_transfer(a):
    con = _con()
    t = con.execute("SELECT * FROM transfers WHERE id = ?", (a.id,)).fetchone()
    if t is None:
        opskit.die(PROG, f"no such transfer: {a.id} (see `{PROG} transfers`)", 2)
    print(f"{t['id']}  {t['status']}" + (f" — {t['detail']}" if t["detail"] else ""))
    for label, v in (("dataset", t["dataset"]), ("destination", f"{t['destination']} ({t['scope']})"), ("rows", f"{t['rows']}   filter: {t['filter'] or '(all rows)'}"),
                     ("columns", (t["columns"] or "").replace(",", ", ")), ("file", f"{t['file']} ({_human_size(t['bytes'] or 0)}, sha256 {(t['sha256'] or '')[:12]})" if t["file"] else None),
                     ("request", t["request"]), ("note", t["note"]), ("at", _when(t["at"])), ("by", t["by"])):
        if v:
            print(f"  {label:<12} {v}")
    if a.rows:
        p = os.path.join(opskit.state_dir(PROG), "outbox", f"{t['id']}_{t['file']}")
        if not os.path.exists(p):
            print(f"\n(outbox copy not kept — copies are retained {OUTBOX_KEEP_DAYS} days; warehouse loads keep none)")
            return 0
        cls = _classes(con, t["dataset"])
        with open(p, newline="") as f:
            rd = list(csv.reader(f))
        hdr, body = rd[0], rd[1:1 + a.rows]
        print(f"\nfirst {len(body)} row(s) of the file:")
        opskit.table([[_show(v, cls.get(h), 26) for h, v in zip(hdr, r)] for r in body], hdr)
        if any(cls.get(h) in MASK_CLASSES for h in hdr):
            print(_mask_note())
    return 0


# ── server-side schedule (scheduled internal loads) ──────────────────────
def _parse_iso(s):
    try:
        return _dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=_dt.timezone.utc)
    except (TypeError, ValueError):
        return None


class _A:
    segment = None; where = None; exclude_rows = None; exclude_file = None


def tick():
    p = os.path.join(opskit.STATE_ROOT, PROG, DB)
    if not os.path.exists(p):
        return
    con = _con()
    try:
        due = con.execute("SELECT * FROM schedules ORDER BY next_at").fetchall()
    except Exception:
        return
    now = opskit.now()
    for s in due:
        nxt = _parse_iso(s["next_at"])
        if nxt is None or nxt > now:
            continue
        ds = con.execute("SELECT * FROM datasets WHERE name = ?", (s["dataset"],)).fetchone()
        dest = con.execute("SELECT * FROM destinations WHERE name = ?", (s["destination"],)).fetchone()
        if ds is None or dest is None:
            continue
        sel = select_rows(con, ds, _A(), extra_filter=s["filter"] or None)      # may stop here — nothing written yet
        cols = resolve_cols(con, ds["name"], s["columns"] or None, None)
        while nxt <= now:
            nxt += _dt.timedelta(minutes=max(5, int(s["every_minutes"] or 60)))
        con.execute("UPDATE schedules SET next_at = ? WHERE name = ?", (opskit.iso(nxt), s["name"]))   # committed with the transfer
        do_transfer(con, ds, dest, sel, cols, note=f"scheduled: {s['name']}", quiet=True, verb="load")


# ── entry ────────────────────────────────────────────────────────────────
def _filters(s):
    s.add_argument("--segment", help="saved row filter (see segments)")
    s.add_argument("--where", action="append", metavar="EXPR", help="row filter, e.g. region!=EU; repeat to combine")
    s.add_argument("--exclude-rows", metavar="KEY,...", action=opskit.join_list_action(), help="leave these rows out (by key)")
    s.add_argument("--exclude-file", metavar="FILE", help="file with one key per line to leave out")


def main(argv=None):
    if os.environ.get("OPSKIT_TICK") == "1":
        tick()
        return 0
    try:
        con = _con()
        meta = _meta(con)
        verb = meta.get("verb") or "share"
        con.close()
    except Exception:
        meta, verb = {}, "share"
    p = argparse.ArgumentParser(prog=PROG, description=meta.get("product") or "Share a dataset with a destination.")
    sub = p.add_subparsers(dest="cmd", required=True, metavar="COMMAND")
    s = sub.add_parser("datasets", help="datasets you can send"); s.set_defaults(fn=cmd_datasets)
    s = sub.add_parser("columns", help="columns, types and classification"); s.add_argument("dataset"); s.set_defaults(fn=cmd_columns)
    s = sub.add_parser("segments", help="saved row filters"); s.add_argument("dataset", nargs="?"); s.set_defaults(fn=cmd_segments)
    s = sub.add_parser("rows", help="browse rows"); s.add_argument("dataset"); _filters(s)
    s.add_argument("--columns", help="comma-separated columns to show"); s.add_argument("--limit", type=int)
    s.add_argument("--offset", type=int, default=0); s.add_argument("--csv", action="store_true", help="CSV to stdout (all matching rows)")
    s.set_defaults(fn=cmd_rows)
    s = sub.add_parser("values", help="value counts for a column"); s.add_argument("dataset"); s.add_argument("column"); _filters(s)
    s.add_argument("--top", type=int, default=25); s.set_defaults(fn=cmd_values)
    s = sub.add_parser("destinations", help="where data can go"); s.set_defaults(fn=cmd_destinations)
    s = sub.add_parser("destination", help="one destination in detail"); s.add_argument("name"); s.set_defaults(fn=cmd_destination)
    s = sub.add_parser("requests", help="data requests"); s.add_argument("--all", action="store_true", help="include closed ones"); s.set_defaults(fn=cmd_requests)
    s = sub.add_parser("request", help="one request in detail"); s.add_argument("id"); s.set_defaults(fn=cmd_request)
    for nm, fn in (("preview", cmd_preview), (verb, cmd_send)):
        s = sub.add_parser(nm, help="show what would be sent" if nm == "preview" else "send to a destination")
        s.add_argument("dataset"); s.add_argument("--to", metavar="DEST")
        _filters(s)
        s.add_argument("--columns", help="only these columns (comma-separated)"); s.add_argument("--exclude", action=opskit.join_list_action(), help="leave these columns out")
        s.add_argument("--request", metavar="ID", help="fulfil a data request: its rows (narrowed by any filters you add) and its columns unless you give --columns")
        if nm == "preview":
            s.add_argument("--rows", type=int, default=5, help="sample rows to show")
        else:
            s.add_argument("--note", help="note stored with the transfer"); s.add_argument("--yes", action="store_true", help="send (otherwise only shows the plan)")
        s.set_defaults(fn=fn)
    s = sub.add_parser("transfers", help="past transfers"); s.add_argument("--to"); s.add_argument("--dataset"); s.add_argument("-n", type=int, default=20)
    s.set_defaults(fn=cmd_transfers)
    s = sub.add_parser("transfer", help="one transfer in detail"); s.add_argument("id"); s.add_argument("--rows", type=int, default=0, help="show the first N rows of the file")
    s.set_defaults(fn=cmd_transfer)
    a = p.parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    opskit.run(main)
