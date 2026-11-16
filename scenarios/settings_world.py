# Unfinished-Bench
# Copyright (c) 2026-present NAVER Corp.
# Apache-2.0
"""Shared by the settings and policy-value scenarios: builds the service seed for the tools/settings.py engine.
The engine uses the install name (costctl, limitctl, ratectl, webcfg, ...) as PROG; state is one file, /var/lib/<install name>/settings.db.
A scenario module builds scopes, settings, past changes and change requests as dicts (times are Clock.T placeholders); this module packs them
into sqlite rows and past audit records (same content as the change history). Values are stored as JSON strings (the engine and the scoring SQL use the same encoding).
"""
import json

from scenarios.timeline import offset_of

SCHEMA = """
CREATE TABLE meta (k TEXT PRIMARY KEY, v TEXT);
CREATE TABLE scopes (id TEXT PRIMARY KEY, kind TEXT, title TEXT, owner TEXT, note TEXT, facts TEXT, version INTEGER, pos INTEGER);
CREATE TABLE settings (scope TEXT, key TEXT, value TEXT, type TEXT, unit TEXT, choices TEXT, min REAL, max REAL,
    owner TEXT, edit_roles TEXT, control TEXT, description TEXT, note TEXT, words TEXT, null_label TEXT,
    updated_at TEXT, updated_by TEXT, change_id TEXT, pos INTEGER, PRIMARY KEY (scope, key));
CREATE TABLE history (id INTEGER PRIMARY KEY AUTOINCREMENT, at TEXT, scope TEXT, key TEXT, old TEXT, new TEXT,
    by TEXT, change_id TEXT, kind TEXT, note TEXT);
CREATE TABLE requests (change_id TEXT, scope TEXT, key TEXT, value TEXT, requested_by TEXT, requested_at TEXT, note TEXT);
CREATE TABLE derived (name TEXT PRIMARY KEY, value REAL, prev REAL, changed_at TEXT, ok INTEGER);
"""


def enc(v):
    return json.dumps(v, sort_keys=True)


def S(scope, key, value, type, owner, edit_roles, control=None, unit=None, choices=None, min=None, max=None,
      description=None, note=None, words=None, null_label=None, created=None, created_by=None):
    """One setting. control = {"group": approval group, "label": display name, "approver": name} or None."""
    return {"scope": scope, "key": key, "value": value, "type": type, "unit": unit, "choices": choices, "min": min, "max": max,
            "owner": owner, "edit_roles": edit_roles, "control": control, "description": description, "note": note,
            "words": words, "null_label": null_label, "_created": created, "_created_by": created_by}


def H(at, scope, key, old, new, by, change_id=None, note=None, kind=None):
    return {"at": at, "scope": scope, "key": key, "old": old, "new": new, "by": by, "change_id": change_id, "note": note,
            "kind": kind or ("change" if change_id else "edit")}


def settings_service(meta, scopes, settings, history, requests, host, extra_audit=()):
    """scopes: [{id, kind, title, owner, note, facts, version}], settings: list of S(...), history: list of H(...) (oldest first),
    requests: [{change_id, scope, key, value, requested_by, requested_at, note}].
    Past audit records = change history (same actor and time) + extra_audit. A setting's updated_* fields come from its last history entry."""
    history = sorted(history, key=lambda h: offset_of(h["at"]) if offset_of(h["at"]) is not None else 0)
    last = {}
    for h in history:
        last[(h["scope"], h["key"])] = h
    srows = []
    for i, s in enumerate(settings):
        h = last.get((s["scope"], s["key"]))
        if h is not None:
            assert h["new"] == s["value"], (s["scope"], s["key"], h["new"], s["value"])
        row = {k: s[k] for k in ("scope", "key", "type", "unit", "min", "max", "owner", "description", "note", "null_label")}
        row.update({"value": enc(s["value"]), "choices": enc(s["choices"]) if s["choices"] is not None else None,
                    "edit_roles": enc(s["edit_roles"] or []), "control": enc(s["control"]) if s["control"] else None,
                    "words": enc(s["words"]) if s["words"] else None,
                    "updated_at": h["at"] if h else s["_created"], "updated_by": h["by"] if h else s["_created_by"],
                    "change_id": h["change_id"] if h else None, "pos": i})
        srows.append(row)
    scrows = [{"id": sc["id"], "kind": sc.get("kind"), "title": sc.get("title"), "owner": sc.get("owner"), "note": sc.get("note"),
               "facts": enc(sc.get("facts") or {}), "version": sc.get("version") or 1, "pos": i} for i, sc in enumerate(scopes)]
    hrows = [{"at": h["at"], "scope": h["scope"], "key": h["key"], "old": enc(h["old"]), "new": enc(h["new"]), "by": h["by"],
              "change_id": h["change_id"], "kind": h["kind"], "note": h["note"]} for h in history]
    rrows = [dict(r, value=enc(r["value"])) for r in requests]
    ctl = {(s["scope"], s["key"]): bool(s["control"]) for s in settings}
    audit = [{"ts": h["at"], "host": host, "actor": h["by"], "action": "set", "result": "ok", "scope": h["scope"], "key": h["key"],
              "old": h["old"], "new": h["new"], "change": h["change_id"], "gated": ctl.get((h["scope"], h["key"]), False)}
             for h in history] + list(extra_audit)
    return {"sqlite": {"settings.db": {"schema": SCHEMA, "rows": {
        "meta": [{"k": "config", "v": json.dumps(meta)}], "scopes": scrows, "settings": srows, "history": hrows,
        "requests": rrows}}}, "audit": audit}


def goal_probe(prog, check):
    """Goal probe run by the split-mode server: a value the engine recomputes after every settings change."""
    return ("python3 -c \"import sqlite3,sys;c=sqlite3.connect('/var/lib/%s/settings.db');"
            "r=c.execute(\\\"select ok from derived where name='%s'\\\").fetchone();sys.exit(0 if r and r[0]==1 else 1)\"" % (prog, check))
