# Unfinished-Bench
# Copyright (c) 2026-present NAVER Corp.
# Apache-2.0
"""Fill the name slots, writing a filled copy of the repository.

Apart from the fictional organizations in the scenarios, the released data refers to outside organizations, products
and shops through slots such as {{SQL_DB_1}} or {{SQL_DB_1|short}}. fill/slots.json describes each slot by its role only. A values file
(made by fill/llm_fill.py, or written by hand) gives each slot its value; this script copies the repository to --out
and replaces every slot. Build and run from the filled copy.

Usage: python3 fill/fill.py --values my_values.json --out ../unfinished-bench-filled
       python3 fill/fill.py --check            # list the slots used in the repository and check them against slots.json

Values file: {"SLOT": {"name": "...", "short": "...", "code": "..."}, "LIST_SLOT": {"list": [...]}}
Forms: name (default) or any other form a slot defines in slots.json (short, code, key, domain, ...); lower (name in
lower case); key falls back to a slug of name; csv (a list slot joined with commas, used as "...".split(",")).
In Python files a value that contains the enclosing string's quote character is escaped."""
import argparse
import json
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
TOKEN = re.compile(r"\{\{([A-Z][A-Z0-9_]*)(?:\|([a-z]+))?\}\}")
TEXT_EXT = (".py", ".md", ".json", ".jsonl", ".txt", ".sh", ".yml", ".yaml", ".toml", ".cfg", ".example")
SKIP_DIRS = {".git", "__pycache__", "tasks", "runs"}
UNSAFE = re.compile(r'["\\{}%\n\r\t]')        # values land inside quoted strings and format strings


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def resolve(slot, form, values):
    v = values.get(slot)
    if v is None:
        raise KeyError(f"no value for {slot}")
    if "list" in v:
        if form != "csv":
            raise KeyError(f"{slot} is a list slot; use {{{{{slot}|csv}}}}")
        for s in v["list"]:
            if not isinstance(s, str) or UNSAFE.search(s) or "," in s or not s:
                raise ValueError(f"bad list item in {slot}: {s!r}")
        return ",".join(v["list"])
    form = form or "name"
    if form == "lower":
        out = v["name"].lower()
    elif form == "key":
        out = v.get("key") or slug(v["name"])
    else:
        if form not in v:
            raise KeyError(f"no '{form}' form for {slot}")
        out = v[form]
    if not isinstance(out, str) or not out or UNSAFE.search(out):
        raise ValueError(f"unsafe or empty value for {slot}|{form}: {out!r}")
    return out


def py_string_spans(src):
    """(start, end, quote) for every string literal in Python source, so a filled value can be escaped for the string
    it lands in. A small scanner (not tokenize) so that it behaves the same on every Python version."""
    spans, i, n = [], 0, len(src)
    while i < n:
        c = src[i]
        if c == "#":
            j = src.find("\n", i)
            i = n if j < 0 else j
            continue
        if c in "'\"":
            k = i
            while k > 0 and src[k - 1].isalpha() and src[k - 1].lower() in "rbuf":
                k -= 1
            raw = "r" in src[k:i].lower()
            q = src[i:i + 3] if src[i:i + 3] in ('"""', "'''") else c
            j = i + len(q)
            while j < n:
                if src[j] == "\\" and not raw:
                    j += 2
                    continue
                if src.startswith(q, j):
                    break
                if len(q) == 1 and src[j] == "\n":
                    break
                j += 1
            spans.append((i, j + len(q), q[0], raw))
            i = j + len(q)
            continue
        i += 1
    return spans


def fill_text(t, values, is_py):
    if not is_py:
        return TOKEN.sub(lambda m: resolve(m.group(1), m.group(2), values), t)
    spans = py_string_spans(t)
    out, last, si = [], 0, 0
    for m in TOKEN.finditer(t):
        val = resolve(m.group(1), m.group(2), values)
        while si < len(spans) and spans[si][1] <= m.start():
            si += 1
        if si < len(spans) and spans[si][0] <= m.start() < spans[si][1]:
            _s, _e, q, raw = spans[si]
            if q in val:
                if raw:
                    raise ValueError(f"{m.group(0)} sits in a raw string; its value cannot contain {q}")
                val = val.replace(q, "\\" + q)
        out.append(t[last:m.start()]); out.append(val); last = m.end()
    out.append(t[last:])
    return "".join(out)


def text_files(root):
    for d, dirs, files in os.walk(root):
        dirs[:] = [x for x in dirs if x not in SKIP_DIRS and not x.startswith("runs_")]
        for f in files:
            yield os.path.join(d, f)


def used_slots(root):
    used = {}
    for p in text_files(root):
        if not p.endswith(TEXT_EXT) or p.startswith(os.path.join(root, "fill") + os.sep):
            continue
        t = open(p, encoding="utf-8").read()
        for m in TOKEN.finditer(t):
            used.setdefault(m.group(1), set()).add(m.group(2) or "name")
    return used


def check():
    slots = json.load(open(os.path.join(HERE, "slots.json")))["slots"]
    used = used_slots(REPO)
    undefined = sorted(set(used) - set(slots))
    unused = sorted(set(slots) - set(used))
    for s in sorted(used):
        print(f"{s:32s} {','.join(sorted(used[s]))}")
    print(f"{len(used)} slots used; undefined: {undefined or 'none'}; defined but unused: {unused or 'none'}")
    return 1 if undefined else 0


def fill(values_path, out):
    values = json.load(open(values_path))
    if os.path.exists(out):
        sys.exit(f"{out} exists; choose a new folder")
    n = 0
    for p in text_files(REPO):
        rel = os.path.relpath(p, REPO)
        dst = os.path.join(out, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if p.endswith(TEXT_EXT) and not p.startswith(HERE):
            t = open(p, encoding="utf-8").read()
            new = fill_text(t, values, p.endswith(".py"))
            n += len(TOKEN.findall(t))
            with open(dst, "w", encoding="utf-8") as f:
                f.write(new)
            shutil.copymode(p, dst)
        else:
            shutil.copy2(p, dst)
    left = used_slots(out)
    if left:
        sys.exit(f"slots left unfilled: {sorted(left)}")
    print(f"filled {n} slots -> {out}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--values")
    ap.add_argument("--out")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    if a.check:
        sys.exit(check())
    if not (a.values and a.out):
        ap.error("--values and --out are required (or --check)")
    fill(a.values, a.out)
