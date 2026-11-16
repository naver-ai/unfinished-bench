# Unfinished-Bench
# Copyright (c) 2026-present NAVER Corp.
# Apache-2.0
"""Ask a language model to fill every slot in fill/slots.json and write a values file for fill/fill.py.

Slots that share a role (the shops in one list, the bank codes, the airlines, ...) are asked together and
must get different names. For each slot the model sees its role, the sentences it appears in (slots already filled are
shown with their values, the others by role) and the setting: the company the text belongs to and, for scenario code,
the scenario's own description. No value is used for two slots. Requests use temperature 0 and a fixed order.

Usage: python3 fill/llm_fill.py --out my_values.json [--model deepseek-ai/DeepSeek-V4-Flash-0731] [--only SLOT,SLOT]
Endpoint: LLM_API_BASE / LLM_API_KEY (OpenAI-compatible). Rerunning with the same --out fills only what is missing."""
import argparse
import importlib
import json
import os
import random
import re
import sys
import time
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, REPO)
sys.path.insert(0, HERE)
from fill import TOKEN, UNSAFE, text_files, TEXT_EXT  # noqa: E402

BASE = (os.environ.get("LLM_API_BASE") or "").rstrip("/")
SYSTEM = ("You help write realistic workplace documents. Some names in the text are blank, marked <<B1>>, <<B2>>, ... "
          "For each blank you get the kind of thing it stands for, the setting (company, country, situation) and the "
          "sentences it appears in. Give each blank the name that fits the setting best, the way a person working there "
          "would write it. Rules: "
          "(1) The value is a thing of the stated kind, even if another word would also read well in the sentence. "
          "(2) It is a proper name (a brand, product, organisation, place or code as people really write it), never the "
          "plain word for the kind of thing (not 'wiki', 'container' or 'VM'). Prefer well-known real names; when the "
          "obvious ones are taken, choose a less common real one rather than making one up. "
          "(3) Fit the country, city and size of business in the setting: a small local business gets a name a local owner "
          "would give it (in the local language where people there would use it), not a well-known chain. "
          "(4) Numbers and codes look like real ones in that country (real numbering ranges), never a counting run "
          "such as 12345 or 7000, 7001, 7002. "
          "(5) Do not build names from the company's own name or the names of its own sites (campuses, offices, schools); "
          "these are outside organisations, products and businesses. "
          "(6) Blanks of the same kind are different things and need different names; a full name and its abbreviation "
          "count as the same thing. A list of names should look like a real mixed list: no alphabetical runs, no repeated "
          "first word. "
          "(7) The value reads correctly with the words just before and after the blank: if the sentence already has "
          "'the' before a blank, the name does not start with 'The'; if the next word is 'Business', the name does not "
          "end with 'Business'. "
          "(8) A value is the name of the thing itself as it would be written in a sentence, even when the blank sits "
          "inside a host name, file name, label or list: not the host, file or label. Write the 'name' form with its usual "
          "capitals; lower-case forms are made from it automatically. "
          "Answer with one JSON object only.")


def norm(v):
    return re.sub(r"[^a-z0-9]+", "", v.lower())


def company_lines():
    out = {}
    assign = json.load(open(os.path.join(REPO, "companies", "assignment.json")))["companies"]
    for co in assign:
        c = importlib.import_module(f"companies.{co}.org").COMPANY
        offices = "; ".join(v[0] for v in c["offices"].values())
        out[co] = f"{c['legal_name']} — {c['what']} Offices: {offices}."
    return out, assign


_SCEN = {}


def scenario_info(rel, assign):
    """(company key, short description of the scenario) for a file"""
    if rel.startswith("companies/"):
        return rel.split("/")[1], ""
    if not rel.startswith("scenarios/c"):
        return None, ""
    if rel in _SCEN:
        return _SCEN[rel]
    sys.path.insert(0, os.path.join(REPO, "build"))
    import build_tasks
    mod = os.path.basename(rel)[:-3]
    co, desc = None, ""
    try:
        m = importlib.import_module("scenarios." + mod)
        cat, slug = getattr(m, "CATEGORY", None) or build_tasks.CATEGORY.get(mod, (None, None))
        co = next((c for c, ids in assign.items() if f"{cat}-{slug}" in ids), None)
        doc = m.__doc__ or ""
        i = doc.find("Situation:")
        desc = re.sub(r"\s+", " ", doc[i + 10:i + 710] if i >= 0 else doc[:500]).strip()
        desc = TOKEN.sub(lambda t: "[name]", desc)
    except Exception:
        pass
    _SCEN[rel] = (co, desc)
    return co, desc


CONST = re.compile(r'^([A-Z][A-Z0-9_]*) = "([^"{}\\]*)"\s*$', re.M)
FILLER = {"and", "of", "the", "for", "&", "de", "la"}


def contexts():
    """slot -> [(file, snippet, written after 'the', form, next word)], documents and chat before code"""
    found = {}
    for p in text_files(REPO):
        if not p.endswith(TEXT_EXT) or p.startswith(HERE):
            continue
        rel = os.path.relpath(p, REPO)
        t = open(p, encoding="utf-8").read()
        consts = dict(CONST.findall(t)) if rel.endswith(".py") else {}
        for m in TOKEN.finditer(t):
            a, b = max(0, m.start() - 200), min(len(t), m.end() + 200)
            while a > 0 and t[a - 1] not in " \n":
                a -= 1
            while b < len(t) and t[b] not in " \n":
                b += 1
            snip = re.sub(r"\s+", " ", t[a:b]).strip()
            named = [f'{k} = "{consts[k]}"' for k in dict.fromkeys(re.findall(r"\b[A-Z][A-Z0-9_]*\b", snip)) if k in consts and len(consts[k]) <= 40]
            if named:          # constants the code refers to, e.g. WEB = "example.com"
                snip += " [where " + "; ".join(named) + "]"
            the = t[max(0, m.start() - 4):m.start()].lower() == "the "
            nxt = re.match(r" ([A-Za-z]+)", t[m.end():m.end() + 30])
            found.setdefault(m.group(1), []).append((rel, snip, the, m.group(2) or "name", nxt.group(1).lower() if nxt else ""))
    for s in found:      # sentences in documents and chat first, code after
        found[s].sort(key=lambda x: (x[0].endswith(".py"), x[0]))
    return found


def forms_of(v):
    return [x for x in v.values() if isinstance(x, str)]


def acronym(name):
    w = [x for x in re.findall(r"[A-Za-z][A-Za-z']*", name) if x.lower() not in FILLER]
    a = "".join(x if x.isupper() and len(x) > 1 else x[0].upper() for x in w) if len(w) > 1 else ""
    return a if len(a) >= 3 else ""          # two letters ('HM') match too many unrelated names


def plain_word(value, role, form):
    """the value is only the word for the kind of thing: role 'wiki' -> 'wiki', 'virtual machine service' -> 'VM'.
    A capitalised product name that is also an ordinary word ('Word', 'Teams') is fine."""
    w = re.findall(r"[a-z]+", role.lower())
    if form == "name" and value == value.lower() and norm(value) in w:
        return True
    return form in ("name", "code", "key") and norm(value) in {w[i][0] + w[i + 1][0] for i in range(len(w) - 1)}


def counting_run(items):
    """'12345', '8901', or numbers in regular steps such as 7000, 7001, 7002 or 7712, 7723, 7734"""
    if len(items) == 1 and items[0].isdigit() and len(items[0]) >= 3:
        d = [int(c) for c in items[0]]
        return all((d[i + 1] - d[i]) % 10 == 1 for i in range(len(d) - 1))
    nums = sorted(int(x) for x in items if x.isdigit())
    steps = [b - a for a, b in zip(nums, nums[1:])]
    return len(nums) >= 4 and max(steps.count(x) for x in set(steps)) >= len(nums) / 3


def render(snippet, labels, slots, values):
    def rep(m):
        s, f = m.group(1), m.group(2) or "name"
        if s in labels:
            return f"<<{labels[s]}{'' if f == 'name' else ':' + f}>>"
        v = values.get(s)
        if v and "list" not in v:
            first = v.get("name") or next(iter(v.values()))
            return first.lower() if f == "lower" else (v.get(f) or first)
        return "[" + slots[s]["role"] + "]"
    return TOKEN.sub(rep, snippet)


def call(model, messages, tok, max_tokens):
    body = {"model": model, "messages": messages, "temperature": 0, "max_tokens": max_tokens,
            "response_format": {"type": "json_object"}}
    last = None
    for att in range(6):
        try:
            r = urllib.request.Request(BASE + "/chat/completions", data=json.dumps(body).encode(),
                                       headers={"Authorization": "Bearer " + tok, "Content-Type": "application/json"})
            j = json.load(urllib.request.urlopen(r, timeout=300))
            return j["choices"][0]["message"].get("content") or ""
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as e:
            last = e
            time.sleep(5 * (att + 1))
    raise SystemExit(f"API error: {last}")


def primary(v):
    return v.get("name") or next((x for x in v.values() if isinstance(x, str)), "")


def check_one(spec, ans):
    pat = spec.get("pattern")
    if spec.get("list"):
        items = ans.get("list") if isinstance(ans, dict) else None
        if isinstance(items, list) and pat:      # a leading 0 the pattern does not want (e.g. phone prefixes) is dropped
            ans["list"] = items = [x[1:] if isinstance(x, str) and x.startswith("0") and not re.fullmatch(pat, x)
                                   and re.fullmatch(pat, x[1:]) else x for x in items]
        if not isinstance(items, list) or len(items) != spec["items"]:
            return f"give exactly {spec['items']} items in 'list'"
        if len(set(items)) != len(items):
            return "list items must all be different"
        for x in items:
            if not isinstance(x, str) or UNSAFE.search(x) or "," in x or (pat and not re.fullmatch(pat, x)):
                return f"bad item {x!r}"
        return None
    if not isinstance(ans, dict):
        return "each blank needs an object with its forms"
    for f in spec["forms"]:
        v = ans.get(f)
        if not isinstance(v, str) or not v.strip() or UNSAFE.search(v):
            return f"form '{f}' missing or has quotes, braces, backslashes or % signs"
        if pat and f == next(iter(spec["forms"])) and not re.fullmatch(pat, v.strip()):
            return f"form '{f}' must match {pat}"
    return None


def taken(values, exclude):
    """normalised forms and acronyms of the values already given -> slot"""
    names, acrs = {}, {}
    for s, v in values.items():
        if "list" in v or s in exclude:
            continue
        for f in forms_of(v):
            names.setdefault(norm(f), s)
            if acronym(f):
                acrs.setdefault(norm(acronym(f)), s)
    return names, acrs

def problems(todo, picked, labels, env):
    """what is wrong with the picked values; env holds values, slots, ctx, slot_cos, own, existing, order"""
    values, slots, ctx, slot_cos, own, existing, order = (env[k] for k in ("values", "slots", "ctx", "slot_cos", "own", "existing", "order"))
    out = []
    names, acrs = taken(values, set(todo))
    by = {}
    for s in todo:
        v, lab, spec = picked[s], labels[s], slots[s]
        if spec.get("list"):
            if counting_run(v["list"]):
                out.append(f"{lab}: the items are a counting run; use numbers really in use there, spread out")
            continue
        for f, x in v.items():
            by.setdefault(norm(x), set()).add(s)
            if plain_word(x, spec["role"], f):
                out.append(f"{lab}: '{x}' is only the word for the kind of thing; give the name of a specific product or organisation")
            if x.isdigit() and counting_run([x]):
                out.append(f"{lab}: '{x}' is a counting run; use digits really in use there")
            other = names.get(norm(x))
            if other and (not slot_cos.get(other) or not slot_cos.get(s) or slot_cos[other] & slot_cos[s]):
                out.append(f"{lab}: '{x}' is already used for another blank")
            for k in (norm(acronym(x)), norm(x)):      # 'Medical Research Council' and 'MRC' are the same thing
                o = (names if k != norm(x) else acrs).get(k) if k else None
                if o and slot_cos.get(o, set()) & slot_cos.get(s, set()):
                    out.append(f"{lab}: '{x}' is the same organisation as {primary(values[o])}, already used for another blank")
        pv = primary(v)
        if " " in pv and re.search(r"(?<![A-Za-z0-9])" + re.escape(pv) + r"(?![A-Za-z0-9])", existing):
            out.append(f"{lab}: '{pv}' is already the name of something else in the data")
        for rel, _sn, _the, form, nxt in ctx.get(s, []):
            x = v.get(form) or v.get("name") or pv
            if nxt and x.split()[-1].lower() == nxt:
                out.append(f"{lab}: '{x}' repeats the next word in the sentence ('{nxt}'); give the name without it")
                break
        for co in slot_cos.get(s, ()):
            if re.search(r"(?<![A-Za-z])" + re.escape(own[co]) + r"(?![A-Za-z])", " ".join(v.values()), re.I):
                out.append(f"{lab}: '{pv}' is built from the company's own name ({own[co]}); give an outside one")
                break
    out += [f"{' and '.join(labels[x] for x in sorted(v))} got the same name" for v in by.values() if len(v) > 1]
    plain = [s for s in todo if not slots[s].get("list")]
    fam = [primary(values[x]) for x in order if family(x) == family(todo[0]) and x in values and x not in todo and "list" not in values[x]]
    allnames = fam + [primary(picked[s]) for s in plain]
    if len(allnames) >= 6:
        lim = max(4, len(allnames) // 8)
        first = {}
        for n in allnames:
            if " " in n:
                first[n.split()[0].lower()] = first.get(n.split()[0].lower(), 0) + 1
        over = [w for w, c in first.items() if c > lim]
        if over:
            out.append(f"too many names in this list start with {', '.join(repr(w) for w in over)} (at most {lim} each); change some of yours")
    def words(n):
        return re.findall(r"[a-z0-9]+", n.lower())

    def too_close(x, y):           # 'Kasut & Beg Ria' / 'Kasut & Beg Ria Baru'
        a, b = sorted((words(x), words(y)), key=len)
        return len(a) >= 2 and b[:len(a)] == a

    for s in plain:
        close = [n for n in allnames if n != primary(picked[s]) and too_close(n, primary(picked[s]))]
        if close:
            out.append(f"{labels[s]}: '{primary(picked[s])}' is too close to '{close[0]}' in the same list")
    lets = [primary(picked[s])[:1].upper() for s in plain]
    run = 1
    for i in range(1, len(lets) + 1):
        if i < len(lets) and ord(lets[i]) - ord(lets[i - 1]) == 1:
            run += 1
            continue
        if run >= 4:
            seq = plain[i - run:i]
            out.append(f"{', '.join(labels[x] for x in seq)} ({', '.join(primary(picked[x]) for x in seq)}) run through the "
                       "alphabet; change some of them so the list is mixed")
        run = 1
    return list(dict.fromkeys(out))



JUDGE = ("You check names filled into realistic workplace documents. For each blank you get the kind of thing it must be "
         "and the value chosen; the setting and sentences are given for reference. A value fails only if (a) it is not a "
         "thing of that kind at all (a tax number is not a tax authority, an app store is not a phone, a research council "
         "is not a government ministry, a hospital is not a shop), or (b) it is named after the company itself or its own "
         "sites. Do not judge which particular organisation or product would be the best choice, or whether it matches the "
         "country: any real thing of that kind passes. Reject only what you are sure is wrong: a real name you do not "
         "recognise, or the new name of a renamed company or product, passes. Answer with one JSON object only.")


def judge(model, tok, todo, picked, labels, slots, setting_txt, lines):
    """a second look by the model: is each value a thing of its kind that fits the setting? -> list of problems"""
    plain = [s for s in todo if not slots[s].get("list")]
    if not plain:
        return []
    items = "\n".join(f"- {labels[s]}: kind = {slots[s]['role']}; value = {primary(picked[s])}" for s in plain)
    ask = (f"Setting:\n{setting_txt or '- not stated'}\nSentences (blanks marked <<B1>>, ...):\n" + "\n".join(lines[:40])
           + f"\nValues:\n{items}\n"
           'Answer as JSON: {"B1": {"ok": true or false, "why": "<if not ok: what is wrong, in a few words>"}, ...}')
    raw = call(model, [{"role": "system", "content": JUDGE}, {"role": "user", "content": ask}], tok, 300 + 60 * len(plain))
    try:
        ans = json.loads(raw[raw.find("{"): raw.rfind("}") + 1])
    except ValueError:
        return []
    out = []
    for s in plain:
        r = ans.get(labels[s])
        if isinstance(r, dict) and r.get("ok") is False:
            out.append(f"{labels[s]}: '{primary(picked[s])}' does not fit ({str(r.get('why') or 'wrong kind or setting')[:160]})")
    return out


def unrun(todo, picked, slots, seed):
    """blanks of one kind are interchangeable: if the model listed the names in alphabetical order, shuffle which blank
    gets which name (fixed seed) instead of asking again"""
    plain = [s for s in todo if not slots[s].get("list")]

    def longest(vals):
        run = best = 1
        for x, y in zip(vals, vals[1:]):
            run = run + 1 if ord(y[:1].upper() or " ") - ord(x[:1].upper() or " ") == 1 else 1
            best = max(best, run)
        return best

    vals = [picked[s] for s in plain]
    if len(vals) < 4 or longest([primary(v) for v in vals]) < 4:
        return picked
    rng = random.Random(seed)
    for _ in range(50):
        rng.shuffle(vals)
        if longest([primary(v) for v in vals]) < 4:
            break
    return {**picked, **dict(zip(plain, vals))}


def family(s):
    return re.sub(r"_\d+$", "", s)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--model", default="deepseek-ai/DeepSeek-V4-Flash-0731")
    ap.add_argument("--only", default="")
    a = ap.parse_args()
    tok = os.environ.get("LLM_API_KEY")
    if not (tok and BASE):
        raise SystemExit("set LLM_API_BASE and LLM_API_KEY")
    slots = json.load(open(os.path.join(HERE, "slots.json")))["slots"]
    cos, assign = company_lines()
    own = {co: line.split()[0] for co, line in cos.items()}          # the company's own name, e.g. its first word
    ctx = contexts()
    slot_cos, slot_files = {}, {}
    for s, occ in ctx.items():
        for rel, *_ in occ:
            slot_files.setdefault(s, set()).add(rel)
            co = scenario_info(rel, assign)[0]
            if co:
                slot_cos.setdefault(s, set()).add(co)
    existing = "\n".join(TOKEN.sub(" ", open(p, encoding="utf-8").read()) for p in text_files(REPO)
                          if p.endswith(TEXT_EXT) and os.path.relpath(p, REPO).startswith(("companies", "scenarios", "tools")))
    values = json.load(open(a.out)) if os.path.exists(a.out) else {}
    only = {x for x in a.only.split(",") if x}
    order = sorted(slots, key=lambda k: [int(x) if x.isdigit() else x for x in re.split(r"(\d+)", k)])
    groups = {}
    for s in order:
        key = ("list", s) if slots[s].get("list") else ("role", slots[s]["role"])
        groups.setdefault(key, []).append(s)

    env = dict(values=values, slots=slots, ctx=ctx, slot_cos=slot_cos, own=own, existing=existing, order=order)
    failed = []
    for key, members in groups.items():
        todo = [s for s in members if s not in values and (not only or s in only)]
        if not todo:
            continue
        spec = slots[todo[0]]
        labels = {s: f"B{i}" for i, s in enumerate(todo, 1)}
        per = 6 if len(todo) <= 3 else (3 if len(todo) <= 10 else 1)
        settings, lines = {}, []
        for s in todo:
            seen = set()
            for rel, snip, *_ in ctx.get(s, []):
                co, desc = scenario_info(rel, assign)
                if co:
                    settings.setdefault(cos[co], set())
                    if desc:
                        settings[cos[co]].add(desc)
                text = render(snip, labels, slots, values)
                if text in seen:
                    continue
                seen.add(text)
                lines.append(f"- {labels[s]} ({slots[s]['role']}): {text}")
                if len(seen) >= per:
                    break
        setting_txt = "\n".join("".join(f"- Situation the sentences come from: {d}\n" for d in sorted(ds)[:2]) + f"- Company background: {c}"
                                for c, ds in settings.items())
        fam_used = [primary(values[x]) for x in order if family(x) == family(todo[0]) and x in values and "list" not in values[x]]
        files = set().union(*(slot_files.get(s, set()) for s in todo))
        cos_here = set().union(*(slot_cos.get(s, set()) for s in todo))
        filled = [x for x in order if x in values and "list" not in values[x] and family(x) != family(todo[0])]
        near = ([primary(values[x]) for x in filled if slot_files.get(x, set()) & files]          # same documents first,
                + [primary(values[x]) for x in filled if not slot_files.get(x, set()) & files and slot_cos.get(x, set()) & cos_here])[:60]
        if spec.get("list"):
            want = '{"B1": {"list": [ ... exactly %d different items ... ]}}' % spec["items"]
        else:
            fs = {s: ", ".join(f'"{f}": "<{d}>"' for f, d in slots[s]["forms"].items()) for s in todo}
            if len(set(fs.values())) == 1:
                want = "{" + ", ".join(f'"{labels[s]}": {{{fs[s]}}}' for s in todo[:2]) + (", ..." if len(todo) > 2 else "") + "}"
            else:
                want = "{" + ", ".join(f'"{labels[s]}": {{{fs[s]}}}' for s in todo) + "}"
        prompt = (f"Kind of thing: {spec['role']} ({len(todo)} blank{'s' if len(todo) > 1 else ''}: {', '.join(labels.values())}"
                  + (", all different" if len(todo) > 1 else "") + ").\n"
                  + (f"Pattern for each value: {spec['pattern']}\n" if spec.get("pattern") else "")
                  + f"Setting:\n{setting_txt or '- not stated'}\nSentences:\n" + "\n".join(lines)
                  + (f"\nNames already given to other blanks in this list (do not reuse them): {', '.join(fam_used)}." if fam_used else "")
                  + (f"\nOther names already in these documents (each is a different thing): {', '.join(near)}." if near else "")
                  + f"\nAnswer as JSON: {want}")
        msgs = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": prompt}]
        err, picked = None, {}
        for att in range(6):
            raw = call(a.model, msgs, tok, 600 + 120 * len(todo))
            try:
                ans = json.loads(raw[raw.find("{"): raw.rfind("}") + 1])
            except ValueError:
                ans, err = {}, "the answer was not JSON"
            else:
                err, picked = None, {}
                for s in todo:
                    e = check_one(slots[s], ans.get(labels[s]))
                    if e:
                        err = f"{labels[s]}: {e}"
                        break
                    picked[s] = ans[labels[s]]
                if not err:
                    for s in todo:            # always written "the <slot>": drop a leading "The" before checking
                        if "list" not in picked[s] and ctx.get(s) and all(x[2] for x in ctx[s]):
                            picked[s] = {f: (x.strip()[4:] if x.strip().startswith("The ") else x.strip()) for f, x in picked[s].items()
                                         if f in slots[s]["forms"]}
                    picked = unrun(todo, picked, slots, todo[0])
                    found = problems(todo, picked, labels, env)
                    if not found and att < 5:          # the last attempt is not judged, so a strict judge cannot block a group
                        found = judge(a.model, tok, todo, picked, labels, slots, setting_txt, lines)
                    if found:
                        err = "; ".join(found) + ". Keep the other answers and change only these"
            if not err:
                break
            print(f"  retry {', '.join(todo[:3])}{' ...' if len(todo) > 3 else ''}: {err[:400]}", file=sys.stderr)
            msgs += [{"role": "assistant", "content": raw}, {"role": "user", "content": f"Problem: {err}. Answer again as JSON: {want}"}]
        if err:
            print(f"SKIPPED {', '.join(todo)}: {err}")
            failed += todo
            continue
        for s in todo:
            v = picked[s]
            values[s] = {"list": v["list"]} if slots[s].get("list") else {f: v[f].strip() for f in slots[s]["forms"]}
            print(s, json.dumps(values[s], ensure_ascii=False))
        json.dump(values, open(a.out, "w"), indent=1, ensure_ascii=False, sort_keys=True)
    print(f"{len(values)} of {len(slots)} slots filled -> {a.out}")
    if failed:
        print("not filled (run again to retry):", ", ".join(failed))


if __name__ == "__main__":
    main()
