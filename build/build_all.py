# Unfinished-Bench
# Copyright (c) 2026-present NAVER Corp.
# Apache-2.0
"""Build the full task set: 97 scenarios x (doc,user variants 1-10 + no-rule variants 1-2) = 2,134 task folders (~4 GB).
Usage: python3 build/build_all.py --out tasks/main [--only c1-refund,c7-release]
Scenario list = companies/assignment.json; each id maps to a module in scenarios/ via its CATEGORY."""
import argparse, glob, importlib, json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, REPO)
import build_tasks
sys.path.insert(0, os.path.join(REPO, "fill"))
from fill import used_slots
_left = {s for d in ("companies", "scenarios", "tools") for s in used_slots(os.path.join(REPO, d))}
if _left:
    sys.exit(f"{len(_left)} name slots are not filled. Fill them first and build from the filled copy "
             "(README, 'Setup'): python3 fill/llm_fill.py --out values.json; python3 fill/fill.py --values values.json --out <dir>")
ap = argparse.ArgumentParser(); ap.add_argument("--out", required=True); ap.add_argument("--only", default="")
a = ap.parse_args()
mods = {}
for f in sorted(glob.glob(os.path.join(REPO, "scenarios", "c*.py"))):
    w = os.path.basename(f)[:-3]
    try:
        m = importlib.import_module("scenarios." + w)
        cat, slug = getattr(m, "CATEGORY", None) or build_tasks.CATEGORY.get(w, (None, None))
        if cat: mods[f"{cat}-{slug}"] = w
    except Exception as e:
        print(f"skip {w}: {e}", file=sys.stderr)
A = json.load(open(os.path.join(REPO, "companies", "assignment.json")))["companies"]
slugs = [s for co in A.values() for s in co]
only = {x for x in a.only.split(",") if x}
todo = [(s, mods[s]) for s in slugs if s in mods and (not only or s in only)]
missing = [s for s in slugs if s not in mods]
print(f"{len(todo)} scenarios to build; not in scenarios/: {missing}")
for slug, w in todo:
    for pos, nv in (("doc,user", "10"), ("no-rule", "2")):
        subprocess.check_call([sys.executable, os.path.join(HERE, "build_tasks.py"), "--world", w, "--out", a.out,
                               "--split", "--positions", pos, "--variants", nv])
