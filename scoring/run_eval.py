#!/usr/bin/env python3
# Unfinished-Bench
# Copyright (c) 2026-present NAVER Corp.
# Apache-2.0
"""Evaluation runner. After the driver ends, the runner copies it next to the task's evaluator.py and runs it.
Writes the checkpoints returned by evaluator.grade_checkpoints() to eval_result.json."""
import argparse
import importlib.util
import json
import os
import sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--result_path", required=True)
    a = ap.parse_args()
    here = os.path.dirname(os.path.abspath(__file__))
    spec = importlib.util.spec_from_file_location("evaluator", os.path.join(here, "evaluator.py"))
    ev = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ev)
    cps = ev.grade_checkpoints()
    out = {"checkpoints": [{"total": 1, "result": int(bool(x))} for x in cps],
           "final_score": {"total": len(cps), "result": int(sum(int(bool(x)) for x in cps))}}
    os.makedirs(os.path.dirname(a.result_path), exist_ok=True)
    with open(a.result_path, "w") as f:
        json.dump(out, f)
    print(json.dumps(out))


if __name__ == "__main__":
    sys.exit(main())
