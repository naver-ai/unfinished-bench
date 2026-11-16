#!/usr/bin/env python3
# Unfinished-Bench
# Copyright (c) 2026-present NAVER Corp.
# Apache-2.0
"""Run tasks x conditions x models x repetitions, one harness/run_cell.py process per cell.

  python3 harness/run_batch.py --tasks-file tasklists/round_01.txt \
      --conditions no_persistence,persistence --models gpt-oss-20b,glm-5.3 --reps 1 --jobs 16

Models come from models.json (key -> model id and provider). Each cell is written to
<RUNS_ROOT>/<task>__<condition>__<model key>_r<rep>/.

Resuming: a cell is skipped when it has both hermes_summary.json and eval_result.json, unless it ended for an
infrastructure reason (api_error, exception, agent_abort), in which case it is run again. A cell that hit the
driver time limit is kept as an observation (not re-run) when it has an evaluation and a transcript, so long
episodes are not replaced by shorter re-runs.

Environment:
  RUNS_ROOT       output root (default: runs)
  MODEL_JOBS      per-model concurrency caps, e.g. "glm-5.3=8,deepseek-v4.1-flash=4"
  BATCH_RUN_TIMEOUT  wall-clock limit of one cell process in seconds (default 15700)
To stop a batch, create <RUNS_ROOT>/_STOP_NEW: no new cells are started and running cells finish.
Do not kill the batch process; running cells would lose their results.
"""
import argparse, collections, json, os, random, signal, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
CONDITIONS = ("no_persistence", "persistence")
REDO_END_REASONS = {"api_error", "exception", "agent_abort"}


def pid_alive(pid):
    try:
        os.kill(pid, 0)
        return True
    except Exception:
        return False


def acquire_lock(root):
    """One batch per output folder. A second batch waits until the first one exits."""
    os.makedirs(root, exist_ok=True)
    lock = os.path.join(root, "_batch.lock")
    if os.path.isfile(lock):
        try:
            old = json.load(open(lock))
        except Exception:
            old = {}
        pid = old.get("pid")
        if pid and pid_alive(pid):
            print(f"[wait] another batch is running in this folder (PID {pid}); waiting for it to exit", flush=True)
            while pid_alive(pid):
                time.sleep(30)
    with open(lock, "w") as f:
        json.dump({"pid": os.getpid(), "started": time.strftime("%Y-%m-%d %H:%M:%S"), "argv": sys.argv[1:]}, f)

    import atexit

    def release():
        try:
            if json.load(open(lock)).get("pid") == os.getpid():
                os.remove(lock)
        except Exception:
            pass
    atexit.register(release)


def needs_run(out):
    sp, ep = os.path.join(out, "hermes_summary.json"), os.path.join(out, "eval_result.json")
    has_transcript = any(os.path.isfile(os.path.join(out, f)) and os.path.getsize(os.path.join(out, f)) > 2
                         for f in ("transcript_live.jsonl", "full_transcript.json"))
    if os.path.isfile(os.path.join(out, "DRIVER_TIMEOUT")) and os.path.isfile(ep) and has_transcript:
        return False
    if not (os.path.isfile(sp) and os.path.isfile(ep)):
        return True
    try:
        if json.load(open(sp)).get("end_reason") in REDO_END_REASONS:
            return True
        for lg in ("driver_log.txt", "eval_log.txt"):
            p = os.path.join(out, lg)
            if os.path.isfile(p):
                t = open(p, errors="ignore").read()
                if "API call failed" in t or "Connection error" in t or "EVAL_TIMEOUT" in t:
                    return True
        return False
    except Exception:
        return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tasks", default="", help="comma-separated task ids")
    ap.add_argument("--tasks-file", default="", help="one task id per line (# comments allowed)")
    ap.add_argument("--conditions", default="no_persistence,persistence")
    ap.add_argument("--models", required=True, help="comma-separated keys from models.json")
    ap.add_argument("--reps", default="1")
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--iter-cap", default=None)
    ap.add_argument("--models-file", default=os.path.join(REPO, "models.json"))
    args = ap.parse_args()

    cfg = json.load(open(args.models_file))
    tasks = [t.strip() for t in args.tasks.split(",") if t.strip()]
    if args.tasks_file:
        for ln in open(args.tasks_file):
            ln = ln.split("#", 1)[0].strip()
            if ln:
                tasks.append(ln)
    if not tasks:
        raise SystemExit("give --tasks or --tasks-file")
    conds = [c.strip() for c in args.conditions.split(",") if c.strip()]
    for c in conds:
        if c not in CONDITIONS:
            raise SystemExit(f"unknown condition {c!r}; choose from {CONDITIONS}")
    models = [m.strip() for m in args.models.split(",") if m.strip()]
    for m in models:
        spec = cfg["models"].get(m)
        if spec is None:
            raise SystemExit(f"model {m!r} is not in {args.models_file}")
        prov = cfg["providers"][spec["provider"]]
        for var in (prov["api_base_env"], prov["api_key_env"]):
            if not os.environ.get(var):
                raise SystemExit(f"{var} is not set (provider {spec['provider']!r} of model {m!r})")

    root = os.environ.get("RUNS_ROOT") or os.path.join(REPO, "runs")
    root = os.path.abspath(root)
    acquire_lock(root)
    stop_file = os.path.join(root, "_STOP_NEW")

    jobs = [(t, c, m, r.strip()) for t in tasks for c in conds for m in models for r in args.reps.split(",")]
    # Fixed-seed shuffle: an outage hits a time window, so running conditions and models interleaved keeps
    # failures from lining up with one condition.
    random.Random(20260711).shuffle(jobs)

    def one(job):
        t, c, m, r = job
        tag = f"{m}_r{r}"
        out = os.path.join(root, f"{t}__{c}__{tag}")
        if not needs_run(out):
            print(f"[skip] {t}/{c}/{tag}", flush=True)
            return 0
        spec = cfg["models"][m]
        prov = cfg["providers"][spec["provider"]]
        env = dict(os.environ)
        env["RUNS_ROOT"] = root
        env["LLM_API_BASE"] = os.environ[prov["api_base_env"]]
        env["LLM_API_KEY"] = os.environ[prov["api_key_env"]]
        env.update({k: str(v) for k, v in (spec.get("env") or {}).items()})
        if os.path.isdir(out):
            mark = os.path.join(out, "_running.pid")
            if os.path.isfile(mark):
                try:
                    owner = int(open(mark).read().split()[0])
                except Exception:
                    owner = None
                if owner and pid_alive(owner):
                    print(f"[protect] cell is running in PID {owner}: {t}/{c}/{tag}", flush=True)
                    return 0
            env["ARCHIVE_PREV_RUN"] = "1"           # the runner moves earlier files to <cell>/_prev_runs/<time>/
        os.makedirs(out, exist_ok=True)
        with open(os.path.join(out, "_running.pid"), "w") as f:
            f.write(f"{os.getpid()} {time.strftime('%H:%M:%S')}")
        cmd = [sys.executable, os.path.join(HERE, "run_cell.py"), "--task", t, "--condition", c,
               "--agent-model", spec["id"], "--tag", tag]
        if args.iter_cap:
            cmd += ["--iter-cap", str(args.iter_cap)]
        # The cell writes its log to a file and runs in its own session, so it finishes and copies its
        # results even if this process dies.
        log = os.path.join(root, f"_launch_{t}_{c}_{tag}.log")
        t0 = time.time()
        with open(log, "a") as lf:
            lf.write(f"\n===== run {time.strftime('%Y-%m-%d %H:%M:%S')} batch PID {os.getpid()} =====\n")
            lf.flush()
            proc = subprocess.Popen(cmd, stdout=lf, stderr=subprocess.STDOUT, text=True,
                                    start_new_session=True, env=env)
            try:
                # Outer limit > driver limit (14400 s) + grading + setup and copying; the container lifetime (16200 s) is above it.
                rc = proc.wait(timeout=int(os.environ.get("BATCH_RUN_TIMEOUT", "15700")))
            except subprocess.TimeoutExpired:
                try:
                    os.killpg(proc.pid, signal.SIGKILL)
                except Exception:
                    pass
                proc.wait()
                rc = -9
        print(f"[done] {t}/{c}/{tag} rc={rc} {time.time() - t0:.0f}s", flush=True)
        return 0 if rc == 0 else 1

    caps = {}
    for part in (os.environ.get("MODEL_JOBS") or "").split(","):
        if "=" in part:
            k, v = part.split("=", 1)
            caps[k.strip()] = max(1, int(v))
    print(f"batch: {len(jobs)} cells, jobs={args.jobs}, model caps={caps or '-'}, runs={root}", flush=True)
    fails, pending, running, per, stopped = 0, list(jobs), {}, collections.Counter(), False
    with ThreadPoolExecutor(max_workers=args.jobs) as ex:
        while pending or running:
            if not stopped and os.path.exists(stop_file):
                stopped = True
                print(f"[stop] {stop_file} found: no new cells; waiting for {len(running)} running "
                      f"({len(pending)} not started)", flush=True)
            if not stopped:
                i = 0
                while len(running) < args.jobs and i < len(pending):
                    m = pending[i][2]
                    if per[m] < caps.get(m, args.jobs):       # a capped model's job waits; the next job goes first
                        job = pending.pop(i)
                        running[ex.submit(one, job)] = m
                        per[m] += 1
                    else:
                        i += 1
            if not running:
                break
            done, _ = wait(list(running), timeout=30, return_when=FIRST_COMPLETED)
            for f in done:
                per[running.pop(f)] -= 1
                try:
                    fails += f.result()
                except Exception as e:
                    print(f"[error] {e}", flush=True)
                    fails += 1
    if stopped:
        print(f"BATCH-STOPPED fails={fails} not_started={len(pending)}", flush=True)
    print(f"BATCH-DONE fails={fails}", flush=True)


if __name__ == "__main__":
    main()
