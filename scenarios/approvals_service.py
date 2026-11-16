# Unfinished-Bench
# Copyright (c) 2026-present NAVER Corp.
# Apache-2.0
"""Shared by the approvals tool (tools/approvals.py): builds the service seed (state.json plus past audit records)
from each item's history. Audit action names match those the engine uses: create, check, request_signoff, sign,
note, <action>, pause. Every timestamp (ts) in the past records must be a timeline placeholder (the grader
sorts them by offset)."""


def approvals_service(state, host_of=None, default_host="approvals-app-1"):
    """state: engine state (dict). host_of: user id -> name of that person's workstation (audit record host)."""
    host_of = host_of or {}
    h = lambda uid: host_of.get(uid, default_host)
    act = state["vocab"]["action"]
    audit = []

    def rec(ts, actor, action, **f):
        r = {"ts": ts, "host": h(actor), "actor": actor, "action": action, "result": "ok"}
        r.update({k: v for k, v in f.items() if v is not None})
        audit.append(r)

    for it in state["items"]:
        extra = {"account": it["account"], "amount": it.get("amount")} if it.get("account") else {}
        rec(it["created_at"], it["prepared_by"], "create", item=it["id"], **extra)
        if it.get("checked_at"):
            rec(it["checked_at"], it.get("checked_by", it["prepared_by"]), "check", item=it["id"], result_summary="pass")
        for r in it.get("requests", []):
            rec(r["at"], r["by"], "request_signoff", item=it["id"], step=r["step"], to=r.get("to"))
        for s in it.get("signoffs", []):
            rec(s["at"], s["by"], "sign", item=it["id"], step=s["step"])
        for n in it.get("notes", []):
            if n.get("at") != it["created_at"]:
                rec(n["at"], n["by"], "note", item=it["id"])
        if it["status"] == "done":
            f = {"item": it["id"], "signoffs": len(it.get("signoffs", []))}
            if it.get("account"):
                f.update(account=it["account"], amount=it.get("amount"))
            if it.get("override"):
                f.update(override=True, reason=it["override"].get("reason"), missing=it["override"].get("missing"))
            rec(it["done_at"], it["done_by"], act, **f)
        if it["status"] == "cancelled" and it.get("cancelled_at"):
            rec(it["cancelled_at"], it.get("cancelled_by", it["prepared_by"]), "cancel", item=it["id"])
    for name, acc in (state.get("accounts") or {}).items():
        for l in acc.get("lines", []):
            if l.get("paused_at") and l.get("paused_by"):
                rec(l["paused_at"], l["paused_by"], "pause", account=name, line=l["id"])
    return {"json": {"state.json": state}, "audit": audit}
