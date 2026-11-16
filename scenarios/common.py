# Unfinished-Bench
# Copyright (c) 2026-present NAVER Corp.
# Apache-2.0
"""Shared by the scenario modules: builds the per-tool service seeds (state + past audit records).
Service seed format (container_setup.seed_service): {"json": {file: object}, "sqlite": {file: {"schema", "rows"}}, "files": {...},
"audit": [past records], "repo": repository path to resolve references against}. Setup fails if the past records are empty (a real service has a history)."""
import textwrap

TICKET_COLS = ["id", "type", "title", "service", "environment", "version", "status", "requester", "approver", "approval_group",
               "created_at", "updated_at", "approved_at", "planned_window", "risk", "rollback", "description"]
TICKETS_SCHEMA = """
CREATE TABLE tickets (id TEXT PRIMARY KEY, type TEXT, title TEXT, service TEXT, environment TEXT, version TEXT,
    status TEXT, requester TEXT, approver TEXT, approval_group TEXT, created_at TEXT, updated_at TEXT,
    approved_at TEXT, planned_window TEXT, risk TEXT, rollback TEXT, description TEXT);
CREATE TABLE comments (id INTEGER PRIMARY KEY AUTOINCREMENT, ticket_id TEXT, author TEXT, created_at TEXT, body TEXT);
"""



def seed_pos(pos):
    """Position name used in random seeds. The no-rule position was called "none" when the benchmark tasks were
    generated, so seeds keep that spelling and every build reproduces the published tasks byte for byte."""
    return "none" if pos == "no-rule" else pos

def d(s):
    return textwrap.dedent(s).lstrip("\n")


# Pool of person names (for generating customers and contacts). A small pool makes the same first/last names repeat visibly, which reads as "combined by a generator".
FIRST_NAMES = """Aaliyah Abel Ada Adrian Aiko Alana Alba Aleksander Alice Amara Amir Ana Anders Andile Anika Anton Arjun Astrid
Aurelio Ava Beatriz Ben Bianca Bilal Bo Bruno Caleb Camille Carlos Cecilia Chiara Chidi Chloe Colm Connor Daisuke Dalia Daniel
Dara Delphine Diego Dina Dmitri Ebony Eero Eleni Elias Elif Emeka Emma Enzo Erin Esther Ethan Fatima Felipe Fiona Freya Gabriel
Gaurav Georgia Gideon Grace Greta Hamza Hana Hannah Harriet Henrik Hiroshi Ibrahim Ida Ilse Imani Irene Isaac Ivan Jada Jakob
Jasmine Javier Jin Joanna Jonas Jorge Joy Julia Kai Kalani Karim Kasia Kenji Kian Kofi Lara Laszlo Leah Leila Lena Leon Lina
Lucas Luca Lucia Maeve Magnus Malik Mara Marco Marisol Mateo Maya Mehmet Mia Mikael Milan Mina Miriam Nadia Naomi Nasser Nico
Nina Noor Olga Olivier Omar Oskar Pablo Paloma Pavel Petra Priya Quentin Rafael Rahul Rania Rebecca Reza Rhea Rosa Ruth Sabine
Salma Samir Santiago Sara Sebastian Selin Shreya Simone Sofia Soren Stella Tariq Tessa Thabo Theo Tomas Uma Valentina Vera
Victor Wanjiru Wei Xavier Yasmin Yusuf Zainab Zeynep Zoe""".split()
LAST_NAMES = """Abara Achebe Adler Agarwal Ahmadi Alvarez Amsel Andersen Aoki Arslan Asante Bakker Balogun Barros Bauer Becker
Bergstrom Bianchi Bishop Blanco Bose Brennan Brooks Caldwell Campos Carvalho Castillo Chandra Chowdhury Costa Cruz Dahl Das
Delgado Demir Dimitrov Doyle Duarte Dubois Eklund Esposito Estrada Farah Ferrari Fischer Fleming Fonseca Fujita Gallagher Garza
Gashi Gonzaga Gordon Graham Gupta Haddad Hansen Harper Hartmann Hayashi Heller Herrera Holm Horvath Hughes Ibarra Ikeda Iyer
Jaramillo Jensen Jovanovic Kaplan Karimi Kato Keller Khan Kiplagat Klein Kowalski Kruger Lambert Larsen Laurent Lee Lehmann
Lindgren Lombardi Lopez Lund Madsen Mahlaba Marchetti Martins Mbeki Medina Mendes Meyer Mishra Molina Moreau Mori Muller Murray
Nagy Nakamura Navarro Ndlovu Nielsen Novak Nunez Obi Okafor Olsen Ortiz Osei Ozturk Palmer Park Patel Pereira Petrov Pham
Quinn Rahman Ramos Rao Reyes Richter Rossi Russo Saito Salazar Santos Sato Schmidt Sharma Silva Singh Sokolov Sorensen Suzuki
Takahashi Tanaka Teixeira Thomsen Torres Tran Varga Vasquez Vogel Wagner Walsh Weber Wojcik Yamamoto Yilmaz Young Zhang
Zielinski""".split()


def unique_people(rng, n):
    """n non-overlapping (first, last) name pairs; first and last names are both drawn mixed from the pool so that no name clusters."""
    out, seen = [], set()
    firsts, lasts = FIRST_NAMES[:], LAST_NAMES[:]
    rng.shuffle(firsts); rng.shuffle(lasts)
    i = 0
    while len(out) < n:
        fn = firsts[i % len(firsts)]
        ln = lasts[(i * 7 + i // len(lasts)) % len(lasts)]
        i += 1
        if (fn, ln) in seen:
            continue
        seen.add((fn, ln)); out.append((fn, ln))
    return out


def tickets_service(tickets, comments, user_ids, host="itsm-app-1"):
    """tickets: list of row dicts, comments: (ticket_id, author display name, time, body), user_ids: display name -> user id."""
    uid = lambda name: user_ids.get(name, name)
    rows = [{c: t.get(c) for c in TICKET_COLS} for t in tickets]
    crow = [{"ticket_id": tid, "author": a, "created_at": at, "body": body} for (tid, a, at, body) in comments]
    audit = []
    for t in tickets:
        audit.append({"ts": t["created_at"], "host": host, "actor": uid(t["requester"]), "action": "create", "result": "ok", "ticket": t["id"]})
        if t.get("approved_at") and t.get("approver"):
            audit.append({"ts": t["approved_at"], "host": host, "actor": uid(t["approver"]), "action": "approve", "result": "ok", "ticket": t["id"]})
    for (tid, a, at, _b) in comments:
        audit.append({"ts": at, "host": host, "actor": uid(a), "action": "comment", "result": "ok", "ticket": tid})
    return {"sqlite": {"tickets.db": {"schema": TICKETS_SCHEMA, "rows": {"tickets": rows, "comments": crow}}}, "audit": audit}


def deployctl_service(state, repo=None, host="deploy-runner-2"):
    audit = []
    for name, svc in state["services"].items():
        for h in svc.get("history", []):
            audit.append({"ts": h["at"], "host": host, "actor": h["by"], "action": "deploy", "result": h.get("result", "ok"),
                          "service": name, "version": h["version"], "env": h["env"], "change": h.get("change")})
    return {"json": {"state.json": state}, "audit": audit, "repo": repo}


def approval_fields():
    return ("type", "status", "approver", "approval_group", "approved_at", "service", "environment", "version")


CHAT_SCHEMA = """
CREATE TABLE users (id TEXT PRIMARY KEY, name TEXT, title TEXT, team TEXT, status TEXT, timezone TEXT, style TEXT);
CREATE TABLE channels (name TEXT PRIMARY KEY, topic TEXT);
CREATE TABLE members (channel TEXT, user TEXT);
CREATE TABLE messages (id INTEGER PRIMARY KEY AUTOINCREMENT, channel TEXT, author TEXT, ts TEXT, body TEXT);
CREATE TABLE scheduled (id INTEGER PRIMARY KEY AUTOINCREMENT, channel TEXT, author TEXT, after_s INTEGER, body TEXT, delivered INTEGER DEFAULT 0);
"""


def chat_service(users, channels, messages, me, host="devbox", later=None):
    """users: [{id,name,title,team,status,timezone}], channels: {name: (topic, [member id])},
    messages: [(channel or 'dm:<other id>', author id, time, body)] -- 'dm:<other>' is a DM with me. Past records = those sent by me.
    later: [(channel, author id, seconds after server start, body)] -- in split mode the server's chat worker posts them at that time (a live scenario)."""
    try:                                   # per-person writing style: apply the style chosen by layer.chat_inputs to scheduled messages too (text unchanged if none)
        from companies.layer import style_text as _st
    except Exception:
        _st = lambda _a, b: b
    try:                                   # put the style in the user table so the away auto-reply (tools/chat.py) answers in that person's style
        from companies.layer import _STYLE as _sty
    except Exception:
        _sty = {}
    users = [dict(u, style=u.get("style") or _sty.get(u["id"])) for u in users]
    messages = [(c, au, ts, _st(au, body)) for (c, au, ts, body) in messages]
    later = [(c, au, s_, _st(au, body)) for (c, au, s_, body) in (later or [])]
    ch_rows = [{"name": n, "topic": t} for n, (t, _m) in channels.items()]
    mem_rows = [{"channel": n, "user": u} for n, (_t, ms) in channels.items() for u in ms]
    msg_rows, audit = [], []
    for (ch, author, ts, body) in messages:
        other = None
        if ch.startswith("dm:"):
            other = ch[3:]
            ch = "dm:" + ":".join(sorted([me, other]))
        msg_rows.append({"channel": ch, "author": author, "ts": ts, "body": body})
        if author == me:
            rec = {"ts": ts, "host": host, "actor": me, "action": "dm" if other else "send", "result": "ok"}
            rec.update({"to": other} if other else {"channel": ch})
            audit.append(rec)
    sched = []
    for (ch, author, after_s, body) in (later or []):
        if ch.startswith("dm:"):
            ch = "dm:" + ":".join(sorted([me, ch[3:]]))
        sched.append({"channel": ch, "author": author, "after_s": int(after_s), "body": body, "delivered": 0})
    rows = {"users": users, "channels": ch_rows, "members": mem_rows, "messages": msg_rows}
    if sched:
        rows["scheduled"] = sched
    return {"sqlite": {"chat.db": {"schema": CHAT_SCHEMA, "rows": rows}}, "audit": audit}
