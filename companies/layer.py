# Unfinished-Bench
# Copyright (c) 2026-present NAVER Corp.
# Apache-2.0
"""Merges company-wide material (staff roster, internal documents, chat history) into a scenario; called by the scenario assigned to each company.
A company = companies/<company>/ with org.py (COMPANY, TEAMS, people(), by_id(), email(), CHANNELS, SYSTEMS), corpus_spec.py (DOCS, SCENARIO_DOCS, KEEP_OUT, ...),
corpus/ (generated documents + _meta.json) and chat_bg.json (background conversation). Usage: layer.docs_repos("retail", C, anchor_iso, scenario) etc.
- docs_repos(company, C, anchor_iso, scenario): builds all internal document repositories (those in corpus_spec.DOCS) with a commit history.
  One or two commits per document (dates fitted to the age fresh/aging/stale/draft, written by a person of the owning team, author of the last commit = the document's
  'last edited by' person). scenario = {"repo/path": [{"author": id, "iso": ..., "message": ..., "content": ...}, ...]} are the commits of the documents the scenario
  owns; they are interleaved chronologically into the same repository history (the scenario puts the position-specific policy section into content).
- chat_inputs(company, C, anchor_iso, channels, msgs): merges the scenario's channels and messages into the whole organisation, the shared channels and several weeks
  of background conversation, and returns (users, channels, messages) to pass as they are to scenarios.common.chat_service.
All times are T() placeholders on the scenario's Clock: computed as some days before the anchor time and the author's local hour (deterministic: the same company gets the same history in every scenario)."""
import datetime as _dt
import functools
import importlib
import hashlib
import json
import os
import random
import re
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))


@functools.lru_cache(None)
def _co(company):
    org = importlib.import_module(f"companies.{company}.org"); spec = importlib.import_module(f"companies.{company}.corpus_spec")
    return org, spec, os.path.join(HERE, company)
# Days before the anchor time of the last edit (range by age)
AGE_DAYS = {"fresh": (5, 45), "aging": (120, 270), "stale": (300, 480), "draft": (8, 60)}
MSG_FIRST = ["Add {t}", "{s}: first version", "Add {t} page", "Move {t} over from the old wiki", "New page: {t}"]
MSG_EDIT = ["{s}: update", "Update {t}", "{s}: tidy up and fix links", "{s}: changes after review", "{s}: bring up to date", "{s}: clarify a couple of steps"]


def _parse(iso):
    return _dt.datetime.strptime(iso.replace("Z", ""), "%Y-%m-%dT%H:%M" + (":%S" if iso.count(":") == 2 else "")).replace(tzinfo=_dt.timezone.utc)


# Weekday public holidays in the author's locale, so that background chat is not placed on them. Year 2026, within the 8/15-12/1 range where background messages fall.
#   In Amsterdam and Berlin all holidays in this range fall on weekends. US: the company-wide holidays (Labor Day, Thanksgiving and the day after).
_HOLIDAYS = {"Europe/London": {"2026-08-31"}, "Europe/Dublin": {"2026-10-26"}, "Europe/Lisbon": {"2026-10-05"},
             "Europe/Vilnius": {"2026-11-02"}, "Asia/Kuala_Lumpur": {"2026-08-25", "2026-08-31", "2026-09-16"}}
_US_HOLIDAYS = {"2026-09-07", "2026-11-26", "2026-11-27"}


def _off(day, tz):
    """Is it a day off (weekend or public holiday) in the author's local calendar?"""
    return day.weekday() >= 5 or day.isoformat() in (_US_HOLIDAYS if tz.startswith("America/") else _HOLIDAYS.get(tz, ()))


def _at(anchor, days_ago, local_hour, tz, weekday_only=True, biz_days=False, phase=0.5):
    """The time days_ago days before the anchor time at the author's local hour local_hour -> UTC ISO. A weekend moves back to the preceding Friday.
    biz_days=True (background chat): days_ago is counted as 'weekdays in the author's local calendar'; weekends are skipped instead of being pulled back to Friday, which avoids a pile-up on Fridays.
    Document commits keep the calendar date as it is (biz_days=False)."""
    loc = anchor.astimezone(ZoneInfo(tz))
    if biz_days:
        # Number of weekdays = days_ago x 5/7 (plus the channel's fixed phase, rounded down, at least 1). Counting days_ago weekdays directly would make the history 1.4 times longer,
        #   so channels would be quiet from 3-6 weeks before the anchor; this way the span matches the calendar.
        #   A different phase per channel makes the weekdays on which two days_ago values coincide differ between channels, so all weekdays are used evenly.
        #   The order of messages on a coinciding day is kept by _after in chat_inputs.
        n, day, k = (max(1, int(days_ago * 5 / 7 + phase)) if days_ago >= 1 else 0), loc.date(), 0
        while k < n:
            day -= _dt.timedelta(days=1)
            if not _off(day, tz):
                k += 1
    else:
        day = (loc - _dt.timedelta(days=days_ago)).date()
        while weekday_only and day.weekday() >= 5:
            day -= _dt.timedelta(days=1)
    h, m = divmod(int(round(local_hour * 60)), 60)     # round to whole minutes (so that 9.996h becomes 10:00, not 09:00)
    t = _dt.datetime(day.year, day.month, day.day, h, m, tzinfo=ZoneInfo(tz)).astimezone(_dt.timezone.utc)
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


def _after(prev, tz, anchor, rng):
    """Keep the channel conversation in order: a time (UTC datetime) in the author's local working hours that is later than the previous message (prev).
    Per-author local time and the weekend shift could stamp a reply before its question; this prevents that. If a few minutes later is outside working hours, use the next weekday morning."""
    t = prev + _dt.timedelta(minutes=rng.uniform(2, 35))
    loc = t.astimezone(ZoneInfo(tz))
    hh = loc.hour + loc.minute / 60
    if _off(loc.date(), tz) or hh < 8.5 or hh > 17.5:
        day = loc.date() + _dt.timedelta(days=0 if hh < 8.5 and not _off(loc.date(), tz) else 1)
        while _off(day, tz):
            day += _dt.timedelta(days=1)
        aloc = anchor.astimezone(ZoneInfo(tz))
        hi = min(10.5, aloc.hour + aloc.minute / 60 - 0.5) if day == aloc.date() else 10.5   # if it is the anchor's own day, up to 30 minutes before the anchor
        hm = rng.uniform(8.6, hi) if hi > 8.7 else 9.0
        t = _dt.datetime(day.year, day.month, day.day, int(hm), int((hm % 1) * 60), tzinfo=ZoneInfo(tz)).astimezone(_dt.timezone.utc)
    if t >= anchor - _dt.timedelta(minutes=30):          # must not pass the anchor time: place it right after the previous message
        t = prev + _dt.timedelta(seconds=rng.randint(40, 240))
    return t.replace(microsecond=0)


def person(company, pid):
    return _co(company)[0].by_id()[pid]


def chat_user(p):
    return {"id": p["id"], "name": p["name"], "title": p["title"], "team": p["team_name"], "status": p["status"] or None, "timezone": p["timezone"]}


def docs_repos(company, C, anchor_iso, scenario=None):
    org, corpus_spec, root = _co(company); CORPUS = os.path.join(root, "corpus")
    anchor = _parse(anchor_iso); by = org.by_id(); meta = json.load(open(os.path.join(CORPUS, "_meta.json"))); ppl = org.people()
    commits = {r: [] for r in dict.fromkeys(d[0] for d in corpus_spec.DOCS)}
    for repo, path, title, team, _gist, _len, _style, age in corpus_spec.DOCS:
        key = f"{repo}/{path}"
        text = open(os.path.join(CORPUS, repo, path)).read()
        rng = random.Random(f"hist|{key}")
        last_by = by.get(meta.get(key, {}).get("author")) or rng.choice([p for p in ppl if p["team"] == team] or ppl)
        team_ppl = [p for p in ppl if p["team"] == team] or [last_by]
        lo, hi = AGE_DAYS[age]
        d_last = rng.randint(lo, hi)
        d_first = d_last + rng.randint(25, 320) if rng.random() < 0.65 else d_last
        slug = path.rsplit("/", 1)[-1].replace(".md", "")
        if path == "README.md":
            d_first = max(d_first, 520 + rng.randint(0, 40))
        tfmt = {"t": title, "s": slug}
        if d_first > d_last:
            # first version = the text without its last section (when there are three or more sections), otherwise the text without its last few lines
            parts = re.split(r"(?m)^(?=## )", text)
            first = "".join(parts[:-1]) if len(parts) >= 4 else "\n".join(text.splitlines()[:-3]) + "\n"
            a0 = rng.choice(team_ppl)
            commits[repo].append({"author": a0["id"], "iso": _at(anchor, d_first, rng.uniform(9.5, 17.3), a0["timezone"]),
                                  "message": rng.choice(MSG_FIRST).format(**tfmt), "files": {path: first}})
            commits[repo].append({"author": last_by["id"], "iso": _at(anchor, d_last, rng.uniform(9.5, 17.3), last_by["timezone"]),
                                  "message": rng.choice(MSG_EDIT).format(**tfmt), "files": {path: text}})
        else:
            commits[repo].append({"author": last_by["id"], "iso": _at(anchor, d_last, rng.uniform(9.5, 17.3), last_by["timezone"]),
                                  "message": rng.choice(MSG_FIRST).format(**tfmt), "files": {path: text}})
    # Also include the guidance documents of the company's other scenarios (default version = the version without the rule), so that paths pointed to by shared documents are not empty.
    # company_docs() of each scenario module -> {"repo/path": [commits...]}; the scenario passed in by the current scenario overrides the same path.
    allc = {}
    for mod in getattr(corpus_spec, "WORLDS", []):
        try:
            m = importlib.import_module(f"scenarios.{mod}")
        except Exception:
            continue
        if hasattr(m, "company_docs"):
            allc.update(m.company_docs())
    allc.update(scenario or {})
    own = set(scenario or {})
    for key, cs in allc.items():
        repo, path = key.split("/", 1)
        for c in cs:
            commits.setdefault(repo, []).append({"author": c["author"], "iso": c["iso"], "message": c["message"], "files": {path: c["content"]},
                                                 "own": key in own})
    # Dates: commits of shared documents and of other scenarios' documents use weekday placeholders (a weekday whatever day the run happens on); commits of this scenario's guidance document use the scenario clock as it is.
    repos = []
    for repo, cs in commits.items():
        cs.sort(key=lambda c: c["iso"])
        repos.append({"path": repo, "branch": "main", "commits": [
            {"author": (by[c["author"]]["name"], org.email(c["author"])), "date": (C.T if c.get("own") else _biz(C))(c["iso"]),
             "message": c["message"], "files": c["files"]} for c in cs]})
    return repos


def _biz(C):
    """Returns the function that builds weekday placeholders; if the scenario's Clock has no B, falls back to T."""
    return getattr(C, "B", C.T)


def _members(spec, ppl):
    out = []
    for t in spec:
        if t == "*": out += [p["id"] for p in ppl]
        elif t.startswith("@"): out += [p["id"] for p in ppl if p.get("office_key", p["office"].lower()).startswith(t[1:])]
        else: out += [p["id"] for p in ppl if p["team"] == t]
    return list(dict.fromkeys(out))


# Fixed writing style per person: most background chat starts lower-case while scenario messages are capitalised sentences, so only the task messages would stand out.
# Each person's style (lower/upper) is set by the majority of their background messages and applied to background, scenario and scheduled messages (scenarios.common.chat_service) alike.
_STYLE = {}
_KEEP = re.compile(r"^(?:[A-Z][A-Z0-9]+\b|[A-Z]+-\d|[A-Z]\d|[A-Z][a-z]+[A-Z]\w*)")   # abbreviations, numbers, camel case (kept as they are even in the lower-case style)
_SENT = re.compile(r"(^|[.!?]\s+)([A-Za-z][\w'’-]*)")                                    # first word of a sentence
_PRON = re.compile(r"(?<![\w'’`/-])I(?=$|[\s'’,.!?;:)])")                                # pronoun I (including I'm, I'll)


def _person_styles(company, bg, ppl):
    cnt = {}
    for ms in bg.values():
        for m in ms:
            b = m["body"].lstrip()
            if b[:1].isalpha():
                c = cnt.setdefault(m["author"], [0, 0]); c[0] += 1; c[1] += b[0].islower()
    tot = sum(c[0] for c in cnt.values()) or 1
    share = sum(c[1] for c in cnt.values()) / tot
    out = {}
    for p in ppl:
        c = cnt.get(p["id"])
        if c and c[0]:
            out[p["id"]] = "lower" if c[1] * 2 >= c[0] else "upper"
        else:
            out[p["id"]] = "lower" if random.Random(f"style|{company}|{p['id']}").random() < share else "upper"
    return out


def style_text(author, body):
    """Fit the author's style. Unchanged if the author is not a company person (bot). Text inside backticks (commands, paths) is left alone.
    Lower-case style: every sentence-initial word becomes lower-case (abbreviations, numbers like RF-428307 and CHG-5530, and camel case are kept), pronoun I -> i
      (as people with this style do in background chat, also from the second sentence on; changing only the first letter would not match them).
    Upper-case style: only the first letter is capitalised."""
    st = _STYLE.get(author)
    if not st or not isinstance(body, str) or not body:
        return body
    lead = len(body) - len(body.lstrip())
    b = body[lead:]
    if st == "lower":
        def low(m):
            w = m.group(2)
            if not w[0].isupper() or _KEEP.match(w) or w == "I" or w[:2] in ("I'", "I’"):
                return m.group(0)
            return m.group(1) + w[0].lower() + w[1:]
        parts = b.split("`")
        for i in range(0, len(parts), 2):                        # even-numbered pieces = outside backticks
            parts[i] = _PRON.sub("i", _SENT.sub(low, parts[i]))
        b = "`".join(parts)
    elif b[:1].isalpha() and b[0].islower():
        b = b[0].upper() + b[1:]
    return body[:lead] + b


def chat_inputs(company, C, anchor_iso, channels=None, msgs=()):
    """channels: scenario channels {name: (topic, [member ids])}: for the same name the members are merged and the scenario's topic is used.
    msgs: scenario messages [(channel, author, T(...), body)]. Returns (users, channels, messages), exactly the arguments of chat_service."""
    org, _spec, root = _co(company)
    anchor = _parse(anchor_iso); ppl = org.people(); by = {p["id"]: p for p in ppl}
    chans = {n: (t, _members(spec, ppl)) for n, (t, spec) in org.CHANNELS.items()}
    for n, (t, mem) in (channels or {}).items():
        old = chans.get(n, (t, []))[1]
        chans[n] = (t, list(dict.fromkeys(old + list(mem))))
    bg = json.load(open(os.path.join(root, "chat_bg.json")))
    _STYLE.clear(); _STYLE.update(_person_styles(company, bg, ppl))
    out = []
    for ch, ms in bg.items():
        prev = None
        ph = int(hashlib.md5(f"{company}|{ch}".encode()).hexdigest()[:8], 16) / 16 ** 8
        for i, m in enumerate(ms):
            a = by.get(m["author"])
            if not a: continue
            t = _parse(_at(anchor, m["d"], m["h"], a["timezone"], biz_days=True, phase=ph))
            if prev is not None and t <= prev:
                t = _after(prev, a["timezone"], anchor, random.Random(f"order|{company}|{ch}|{i}"))
            prev = t
            out.append((ch, a["id"], _biz(C)(t.strftime("%Y-%m-%dT%H:%M:%SZ")), style_text(a["id"], m["body"])))
    out += [(c, au, ts, style_text(au, body)) for (c, au, ts, body) in msgs]
    users = [chat_user(p) for p in ppl]
    return users, chans, out
