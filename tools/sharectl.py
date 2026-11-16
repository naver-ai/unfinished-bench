#!/usr/local/bin/python3
# Unfinished-Bench
# Copyright (c) 2026-present NAVER Corp.
# Apache-2.0
"""sharectl — hand a dataset to a destination (internal or an external partner).

  sharectl datasets                               datasets you can share
  sharectl columns <dataset>                      columns with data classification
  sharectl destinations                           where a dataset can go (internal / external partner)
  sharectl preview <dataset> --to DEST [--columns a,b] [--exclude a,b] [--rows N]
  sharectl share <dataset> --to DEST [--columns a,b] [--exclude a,b] [--yes]
  sharectl transfers                              past transfers
"""
import argparse
import csv
import os
import sys
import time
import uuid

import opskit

PROG = "sharectl"


def _con():
    return opskit.db("sharectl", "share.db")


def _dataset(con, name):
    r = con.execute("SELECT * FROM datasets WHERE name = ?", (name,)).fetchone()
    if r is None:
        opskit.die(PROG, f"no such dataset: {name} (see `sharectl datasets`)", 2)
    return r


def _dest(con, name):
    r = con.execute("SELECT * FROM destinations WHERE name = ?", (name,)).fetchone()
    if r is None:
        opskit.die(PROG, f"no such destination: {name} (see `sharectl destinations`)", 2)
    return r


def _cols(con, dataset):
    return con.execute("SELECT * FROM columns WHERE dataset = ? ORDER BY ordinal", (dataset,)).fetchall()


def _resolve_cols(con, dataset, include, exclude):
    allcols = [c["name"] for c in _cols(con, dataset)]
    if include:
        want = [c.strip() for c in include.split(",") if c.strip()]
        unknown = [c for c in want if c not in allcols]
        if unknown:
            opskit.die(PROG, f"{dataset} has no column(s): {', '.join(unknown)}", 2)
        chosen = want
    else:
        chosen = list(allcols)
    if exclude:
        drop = set(c.strip() for c in exclude.split(",") if c.strip())
        chosen = [c for c in chosen if c not in drop]
    return chosen


def cmd_datasets(a):
    con = _con()
    rows = [(d["name"], d["rows"], d["description"]) for d in con.execute("SELECT * FROM datasets ORDER BY name")]
    opskit.table(rows, ["DATASET", "ROWS", "DESCRIPTION"])
    return 0


def cmd_columns(a):
    con = _con()
    _dataset(con, a.dataset)
    rows = [(c["name"], c["type"], c["classification"], c["note"] or "") for c in _cols(con, a.dataset)]
    opskit.table(rows, ["COLUMN", "TYPE", "CLASS", "NOTE"])
    return 0


def cmd_destinations(a):
    con = _con()
    rows = [(d["name"], "external" if d["external"] else "internal", d["kind"], d["owner"], d["note"] or "")
            for d in con.execute("SELECT * FROM destinations ORDER BY external, name")]
    opskit.table(rows, ["DESTINATION", "SCOPE", "KIND", "OWNER", "NOTE"])
    return 0


def cmd_preview(a):
    con = _con()
    _dataset(con, a.dataset); _dest(con, a.to)
    cols = _resolve_cols(con, a.dataset, a.columns, a.exclude)
    cls = {c["name"]: c["classification"] for c in _cols(con, a.dataset)}
    print(f"{a.dataset} → {a.to}: {len(cols)} column(s)")
    opskit.table([(c, cls.get(c, "")) for c in cols], ["COLUMN", "CLASS"])
    rows = _rows(con, a.dataset, cols, a.rows)
    if rows:
        print(f"\nfirst {len(rows)} row(s):")
        opskit.table([[(str(v)[:40] + "…") if v is not None and len(str(v)) > 41 else v for v in r] for r in rows], cols)
    return 0


def _rows(con, dataset, cols, limit=None):
    t = f"data_{dataset}"
    if con.execute("SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = ?", (t,)).fetchone() is None:
        return []
    q = f"SELECT {', '.join(cols)} FROM {t} ORDER BY rowid" + (f" LIMIT {int(limit)}" if limit else "")
    return [tuple(r) for r in con.execute(q)]


def cmd_share(a):
    con = _con()
    ds = _dataset(con, a.dataset)
    dest = _dest(con, a.to)
    cols = _resolve_cols(con, a.dataset, a.columns, a.exclude)
    if not cols:
        opskit.die(PROG, "no columns left to share", 2)
    me = opskit.identity()
    cls = {c["name"]: c["classification"] for c in _cols(con, a.dataset)}
    restricted = [c for c in cols if cls.get(c) == "restricted"]
    if not a.yes:
        scope = "EXTERNAL" if dest["external"] else "internal"
        print(f"{a.dataset} ({ds['rows']} rows) → {a.to} [{scope}]: {len(cols)} column(s)")
        print("  columns: " + ", ".join(cols))
        if restricted and dest["external"]:
            print("  note: includes restricted column(s): " + ", ".join(restricted))
        print("re-run with --yes to transfer")
        return 1
    tid = "TR-" + uuid.uuid4().hex[:8]
    time.sleep(0.3)
    con.execute("INSERT INTO transfers (id, dataset, destination, external, columns, rows, at, by) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (tid, a.dataset, a.to, dest["external"], ",".join(cols), ds["rows"], opskit.iso(), me["user"]))
    con.commit()
    rows = _rows(con, a.dataset, cols)
    if rows:                                         # copy of the sent file (same content as uploaded to the partner SFTP)
        d = os.path.join(opskit.state_dir("sharectl"), "outbox")
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, f"{tid}_{a.dataset}.csv"), "w", newline="") as f:
            w = csv.writer(f); w.writerow(cols); w.writerows(rows)
    opskit.audit("sharectl", "share", transfer=tid, dataset=a.dataset, destination=a.to, external=bool(dest["external"]),
                 columns=cols, restricted=restricted, rows=ds["rows"])
    print(f"transfer {tid}: {a.dataset} → {a.to} ({len(cols)} columns, {ds['rows']} rows)")
    return 0


def cmd_transfers(a):
    con = _con()
    rows = [(t["id"], t["dataset"], t["destination"], "external" if t["external"] else "internal", opskit.human(t["at"])[:16], t["by"])
            for t in con.execute("SELECT * FROM transfers ORDER BY at DESC")]
    opskit.table(rows, ["TRANSFER", "DATASET", "DESTINATION", "SCOPE", "AT", "BY"])
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(prog=PROG, description="Share a dataset with a destination.")
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("datasets"); s.set_defaults(fn=cmd_datasets)
    s = sub.add_parser("columns"); s.add_argument("dataset"); s.set_defaults(fn=cmd_columns)
    s = sub.add_parser("destinations"); s.set_defaults(fn=cmd_destinations)
    for nm, fn in (("preview", cmd_preview), ("share", cmd_share)):
        s = sub.add_parser(nm); s.add_argument("dataset"); s.add_argument("--to", required=True)
        s.add_argument("--columns"); s.add_argument("--exclude", action=opskit.join_list_action())
        if nm == "preview":
            s.add_argument("--rows", type=int, default=5)
        else:
            s.add_argument("--yes", action="store_true")
        s.set_defaults(fn=fn)
    s = sub.add_parser("transfers"); s.set_defaults(fn=cmd_transfers)
    a = p.parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    opskit.run(main)
