#!/usr/bin/env python3
# Unfinished-Bench
# Copyright (c) 2026-present NAVER Corp.
# Apache-2.0
"""Run one cell: one task × one condition × one model.

Starts the task's server container (tool backends and service state) and the agent container (an employee
workstation), prepares both, runs the agent driver inside the agent container, then grades the final state
on the server side and copies all records into <RUNS_ROOT>/<task>__<condition>__<tag>/.

Usage:
  python3 harness/run_cell.py --task c1-refund-doc-v01 --condition persistence --agent-model openai/gpt-oss-20b --tag gptoss20b_r1
Environment:
  LLM_API_BASE, LLM_API_KEY   OpenAI-compatible endpoint and key for the agent model (set per cell by run_batch.py)
  TASKS_ROOT                  built task folders (default: tasks/main)
  RUNS_ROOT                   output root (default: runs)
  AGENT_IMAGE                 agent image with the virtual clock (default: unfinished-bench/agent:vclock)
  DRIVER_TIMEOUT              wall-clock seconds for the agent episode (default 14400)
  CONTAINER_TTL               wall-clock seconds after which both containers are stopped (default 16200)
  NET_INTERNAL                1 (default): no internet in the cell except the model endpoint (see harness/server_split.py)
Time limits nest: container lifetime 16200 > cell process (run_batch.py) 15700 > driver 14400 + grading and copying.
"""
import argparse, datetime, json, os, shutil, subprocess, sys, threading, time, uuid

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import virtual_clock                      # noqa: E402
from server_split import SplitEnv         # noqa: E402
from source_notice import copy_without_notice  # noqa: E402

TASKS = os.environ.get("TASKS_ROOT") or os.path.join(REPO, "tasks", "main")
IMAGE = os.environ.get("AGENT_IMAGE", "unfinished-bench/agent:vclock")
DRIVER = os.path.join(HERE, "agent_driver.py")
PATCHES = os.environ.get("HERMES_PATCH_DIR") or os.path.join(HERE, "hermes_patches")
SCORER = os.path.join(REPO, "scoring", "run_eval.py")
CONDITIONS = ("no_persistence", "persistence")

# Paths inside the agent container. The driver gets an ordinary-looking name and deletes itself after start.
DRIVER_IN = "/opt/hermes/runtime/session.py"
SITE = "/opt/hermes-venv/lib/python3.12/site-packages"
# The driver and PID 1 run with a minimal environment so nothing harness-related shows in /proc/<pid>/environ.
CLEAN_PATH = "/usr/local/bin:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin"
CLEAN_ENV_PREFIX = ["env", "-i", f"PATH={CLEAN_PATH}", "LANG=C.UTF-8"]
TRACE_FILES = ("hermes_summary.json", "hermes_dialogue.jsonl", "full_transcript.json", "_api_kwargs.jsonl",
               "_system_prompt.txt", "_system_prompt_turns.jsonl", "transcript_live.jsonl")
RESULT_FILES = {"hermes_summary.json", "eval_result.json", "full_transcript.json", "transcript_live.jsonl",
                "hermes_dialogue.jsonl", "DRIVER_TIMEOUT"}


def _mask(cmd):
    return [(a.split("=", 1)[0] + "=***" if ("TOKEN=" in a or "KEY=" in a) else a) for a in cmd]


def run(cmd, timeout=300, check=True):
    print("+ " + " ".join(_mask(cmd[:6])) + (" ..." if len(cmd) > 6 else ""), flush=True)
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired as e:
        raise subprocess.TimeoutExpired(_mask(list(cmd)), e.timeout) from None   # never leak a key into a traceback
    except Exception:
        raise RuntimeError("subprocess error: " + " ".join(_mask(list(cmd)[:6])) + " ...") from None
    if check and r.returncode != 0:
        print(f"  ! exit {r.returncode}\n  stdout: {(r.stdout or '')[-800:]}\n  stderr: {(r.stderr or '')[-800:]}", flush=True)
        raise SystemExit(f"command failed: {cmd[:4]}")
    return r


def dexec(cid, sh, timeout=300, check=True, env=None):
    pre = sum((["-e", f"{k}={v}"] for k, v in (env or {}).items()), [])
    return run(["docker", "exec", *pre, cid, "bash", "-lc", sh], timeout=timeout, check=check)


def dexec_stream(cid, sh, timeout, env, outdir):
    """Run the driver. Its configuration goes in on stdin as JSON (not -e, which would show in /proc/<pid>/environ).
    The driver writes its records to a framed stdout stream (`\\x1eTRACE <A|W> <name> <len>`) instead of the container
    filesystem; they are written to outdir as they arrive, so a timeout keeps everything received so far.
    Returns (exit code or None on timeout, other stdout, stderr)."""
    p = subprocess.Popen(["docker", "exec", "-i", cid, *CLEAN_ENV_PREFIX, f"HOME={env.get('HOME', '/root')}", "bash", "-lc", sh],
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.stdin.write(json.dumps(env).encode())
    p.stdin.close()
    other, err = [], []

    def _out():
        f = p.stdout
        while True:
            line = f.readline()
            if not line:
                return
            if not line.startswith(b"\x1eTRACE "):
                other.append(line)
                continue
            try:
                _, mode, name, n = line.rstrip(b"\n").split(b" ")
                name, n = name.decode(), int(n)
            except ValueError:
                other.append(line)
                continue
            data = f.read(n)
            if name in TRACE_FILES:
                dst = os.path.join(outdir, name)
                if mode == b"A":
                    with open(dst, "ab") as w:
                        w.write(data)
                else:
                    with open(dst + ".part", "wb") as w:
                        w.write(data)
                    os.replace(dst + ".part", dst)
            if len(data) < n:
                return

    ts = [threading.Thread(target=_out, daemon=True), threading.Thread(target=lambda: err.append(p.stderr.read()), daemon=True)]
    for t in ts:
        t.start()
    try:
        rc = p.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        p.kill(); p.wait(); rc = None
    for t in ts:
        t.join(30)
    return rc, b"".join(other).decode("utf-8", "replace"), b"".join(err).decode("utf-8", "replace")


def prepare_outdir(outdir):
    """Cells are written once. Re-running a cell that already has results requires ARCHIVE_PREV_RUN=1 (set by
    run_batch.py for redo passes); earlier files are then moved to <cell>/_prev_runs/<time>/, never deleted."""
    if os.path.isdir(outdir):
        prev = [f for f in os.listdir(outdir) if f not in ("_prev_runs", "_running.pid")]
        if prev:
            if (set(prev) & RESULT_FILES) and os.environ.get("ARCHIVE_PREV_RUN") != "1":
                print(f"[write-once] results already present, not overwriting: {outdir}", flush=True)
                sys.exit(3)
            dst = os.path.join(outdir, "_prev_runs", time.strftime("%Y%m%d_%H%M%S"))
            os.makedirs(dst)
            for f in prev:
                shutil.move(os.path.join(outdir, f), os.path.join(dst, f))
    os.makedirs(outdir, exist_ok=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", required=True)
    ap.add_argument("--condition", required=True, choices=CONDITIONS)
    ap.add_argument("--agent-model", required=True)
    ap.add_argument("--tag", required=True, help="<model key>_r<rep>")
    ap.add_argument("--iter-cap", default="120", help="tool-call budget of the episode")
    ap.add_argument("--keep", action="store_true", help="keep containers for inspection")
    args = ap.parse_args()
    base, key = os.environ.get("LLM_API_BASE"), os.environ.get("LLM_API_KEY")
    if not (base and key):
        raise SystemExit("LLM_API_BASE and LLM_API_KEY must be set")
    tdir = os.path.join(TASKS, args.task)
    man = json.load(open(os.path.join(tdir, "_private", "manifest.json")))
    runid = f"{args.task}__{args.condition}__{args.tag}"
    outdir = os.path.join(os.environ.get("RUNS_ROOT") or os.path.join(REPO, "runs"), runid)
    prepare_outdir(outdir)
    cname = f"ubench-{uuid.uuid4().hex[:8]}"

    # Virtual clock: both containers see the weekday and local time the scenario was written for
    # (the same weekday nearest to today). Without it, timestamps in documents and chat would not line up.
    vca = virtual_clock.virtual_anchor(man.get("clock_gate"))
    if vca is None:
        raise SystemExit("manifest has no clock_gate")
    real = datetime.datetime.now(datetime.timezone.utc)
    vc_env = virtual_clock.container_env(vca, IMAGE, real)
    json.dump({"real_start": real.strftime("%Y-%m-%dT%H:%M:%SZ"), "virtual_anchor": vc_env["OPSKIT_ANCHOR"],
               "faketime": vc_env["FAKETIME"], "clock_gate": man.get("clock_gate"), "image": IMAGE},
              open(os.path.join(outdir, "vclock.json"), "w"))

    senv = SplitEnv(tdir, man, cname, IMAGE, label="unfinished-bench=1", extra_env=vc_env)
    try:
        with open(os.path.join(outdir, "server_init_log.txt"), "w") as sl:
            senv.create(log=sl)
    except Exception as e:
        open(os.path.join(outdir, "INIT_FAILED"), "w").write(f"server: {e}\n")
        senv.destroy()
        raise SystemExit(f"server init failed: {e}")
    goal_probe = senv.goal_probe()
    host = ["--hostname", man["hostname"]] if man.get("hostname") else []
    run(["docker", "run", "-d", "--name", cname, "--label", "unfinished-bench=1", *host, *senv.agent_run_args(),
         "--pids-limit", "512", "--memory", "3g", IMAGE, *CLEAN_ENV_PREFIX, "sleep", "infinity"])
    # Container lifetime cap, enforced from the host so no timer is visible inside the container.
    reaper = subprocess.Popen(["sh", "-c", f"sleep {int(os.environ.get('CONTAINER_TTL', '16200'))}; "
                               f"docker stop -t 5 {cname} {senv.srv} >/dev/null 2>&1"],
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
    hermes_dir = "/root/.hermes"
    env = {}
    try:
        # Virtual clock through /etc/ld.so.preload and the offset file, so nothing shows in the agent's environment.
        conf = virtual_clock.CONF
        dexec(cname, f"t=$(stat -c %Y /etc); printf '%s\\n' '{vc_env['FAKETIME']}' > {conf} && "
                     f"printf '%s\\n' '{vc_env['LD_PRELOAD']}' > /etc/ld.so.preload && "
                     f"touch -r /etc/debian_version /etc/ld.so.preload {conf} && touch -d @$t /etc")
        chk = (dexec(cname, "date -u +%s; env | grep -c -i -E 'faketime|ld_preload' || true", check=False).stdout or "").split()
        want = int(time.time()) + int(vc_env["FAKETIME"])
        if len(chk) < 2 or not chk[0].isdigit() or abs(int(chk[0]) - want) > 300 or chk[1] != "0":
            open(os.path.join(outdir, "INIT_FAILED"), "w").write(f"virtual clock check failed: {chk} want~{want}\n")
            raise SystemExit("virtual clock check failed")

        # Workstation setup: files go to /outputs; the setup script installs the thin tool clients, replays the
        # document repositories, writes the employee home, then removes /utils. No grader is in the container yet.
        dexec(cname, "mkdir -p /outputs /utils /instruction && rm -rf /outputs/* || true")
        run(["docker", "cp", f"{tdir}/utils/.", f"{cname}:/utils/"])
        if os.path.isdir(f"{tdir}/workspace"):
            run(["docker", "cp", f"{tdir}/workspace/.", f"{cname}:/outputs/"])
        run(["docker", "cp", f"{tdir}/task.md", f"{cname}:/instruction/task.md"])
        ienv = dict(senv.agent_env())
        ienv.setdefault("OPSKIT_ANCHOR", vc_env["OPSKIT_ANCHOR"])
        ir = dexec(cname, "bash /utils/init.sh", timeout=300, check=False, env=ienv)
        open(os.path.join(outdir, "init_log.txt"), "w").write(f"rc={ir.returncode}\n{ir.stdout or ''}\n===STDERR===\n{ir.stderr or ''}")
        if ir.returncode != 0:
            open(os.path.join(outdir, "INIT_FAILED"), "w").write(f"rc={ir.returncode}\n{(ir.stderr or '')[-2000:]}\n")
            raise SystemExit(f"workstation setup failed rc={ir.returncode}")

        dexec(cname, f"mkdir -p {os.path.dirname(DRIVER_IN)}")
        drv = copy_without_notice(DRIVER, os.path.join(outdir, ".driver_copy.py"))     # the measured bytes, no notice
        run(["docker", "cp", drv, f"{cname}:{DRIVER_IN}"])
        os.remove(drv)
        for root, _, files in os.walk(PATCHES):           # hermes-agent files we patch (see harness/hermes_patches)
            for fn in files:
                if fn.endswith(".py"):
                    src = os.path.join(root, fn)
                    tmp = copy_without_notice(src, os.path.join(outdir, ".patch_copy.py"))   # notice removed: the measured bytes
                    run(["docker", "cp", tmp, f"{cname}:{SITE}/{os.path.relpath(src, PATCHES)}"])
                    os.remove(tmp)

        user = json.load(open(os.path.join(tdir, "utils", "seed.json")))["identity"]["user"]
        hermes_dir = f"/home/{user}/.hermes"               # Hermes lives in the employee's home like any user install
        dexec(cname, f"if [ -d /root/.hermes ] && [ ! -e {hermes_dir} ]; then mkdir -p /home/{user} && mv /root/.hermes {hermes_dir}; fi",
              check=False)
        env = {
            "LLM_API_BASE": base, "LLM_API_KEY": key, "AGENT_MODEL": args.agent_model,
            "CONDITION": args.condition, "ITER_CAP": args.iter_cap,
            "AGENT_USER": user, "HOME": f"/home/{user}",
            "HERMES_API_CALL_STALE_TIMEOUT": os.environ.get("HERMES_API_CALL_STALE_TIMEOUT", "900"),
            "HERMES_DISABLE_FILE_STATE_GUARD": "1",       # its "modified by sibling subagent" warning reads as a harness artifact
            "HERMES_NO_CAP_WRAPUP": "1", "HERMES_SILENT_USER": "1",   # no framework-generated user turns (see hermes_patches)
            "HERMES_ECHO_REASONING_MODELS": os.environ.get("HERMES_ECHO_REASONING_MODELS",
                                                           "gpt-oss,qwen,gemma,glm,deepseek,kimi,llama,exaone,muse"),
            "HERMES_EMPTY_RETRIES": os.environ.get("HERMES_EMPTY_RETRIES", "8"),
            "GOAL_PROBE": json.dumps(goal_probe, separators=(",", ":")),
        }
        for k in ("REASONING_MODE", "REASONING_EFFORT", "RATELIMIT_RETRIES", "AGENT_MAX_TOKENS"):
            if os.environ.get(k):
                env[k] = os.environ[k]

        timeout = int(os.environ.get("DRIVER_TIMEOUT", "14400"))
        t0, dlog = time.time(), ""
        try:
            rc, so, se = dexec_stream(cname, f"cd /outputs && /opt/hermes-venv/bin/python {DRIVER_IN} -", timeout, env, outdir)
            dlog = (so or "") + "\n===STDERR===\n" + (se or "")
            if rc is None:
                raise subprocess.TimeoutExpired("driver", timeout)
            open(os.path.join(outdir, "driver_log.txt"), "w").write(dlog)
        except subprocess.TimeoutExpired:
            open(os.path.join(outdir, "driver_log.txt"), "w").write(f"DRIVER_TIMEOUT: {timeout}s\n" + dlog)
            open(os.path.join(outdir, "DRIVER_TIMEOUT"), "w").write(f"{timeout}\n")
            # Stop the in-container driver before grading so the graded state is the state at the time limit.
            pat = "[" + DRIVER_IN[0] + "]" + DRIVER_IN[1:]
            k = dexec(cname, f"pkill -TERM -f '{pat}'; sleep 3; pkill -KILL -f '{pat}'; true", timeout=60, check=False)
            open(os.path.join(outdir, "DRIVER_TIMEOUT"), "a").write(f"in-container driver stopped before grading (rc={k.returncode})\n")
        print(f"[driver ran in {time.time() - t0:.0f}s]", flush=True)

        # Grading on the server side: audit logs and service state, plus evidence copied from the agent container.
        ev = None
        try:
            ev, missing = senv.collect_evidence(cname)
            rc2, out, err, res = senv.grade(ev, os.path.join(tdir, "_private", "evaluator.py"), SCORER)
            open(os.path.join(outdir, "eval_log.txt"), "w").write(
                (out or "") + "\n===STDERR===\n" + (err or "") + (f"\nmissing agent evidence: {missing}\n" if missing else ""))
            if res:
                open(os.path.join(outdir, "eval_result.json"), "w").write(res)
        except subprocess.TimeoutExpired:
            open(os.path.join(outdir, "eval_log.txt"), "w").write("EVAL_TIMEOUT\n")
        except Exception as e:
            open(os.path.join(outdir, "eval_log.txt"), "w").write(f"EVAL_ERROR: {e}\n")
        try:
            senv.state_tar(os.path.join(outdir, "service_state.tgz"), ev)
        except Exception as e:
            print(f"  ! service state copy failed: {e}", flush=True)
        if ev:
            shutil.rmtree(ev, ignore_errors=True)

        for marker, cond, text in (("MISSING_SUMMARY", "hermes_summary.json", "driver summary missing — container likely died early\n"),
                                   ("MISSING_EVAL", "eval_result.json", "no grading result — eval failed or timed out\n")):
            if not os.path.isfile(os.path.join(outdir, cond)):
                open(os.path.join(outdir, marker), "w").write(text)
        r = dexec(cname, "cd /outputs && ls -la", check=False)
        open(os.path.join(outdir, "outputs_listing.txt"), "w").write(r.stdout or "")
        r = dexec(cname, "cd /outputs && find . -type f -printf '%10s  %TY-%Tm-%Td %TH:%TM  %p\\n' 2>/dev/null | sort -k4", check=False)
        open(os.path.join(outdir, "outputs_tree.txt"), "w").write(r.stdout or "")
        dexec(cname, "cd /outputs && tar czf /tmp/ws_text.tgz --exclude='*.dat' --exclude='*.db' --exclude='*.sqlite*' "
                     "--exclude='__pycache__' . 2>/dev/null || true", check=False)
        run(["docker", "cp", f"{cname}:/tmp/ws_text.tgz", os.path.join(outdir, "workspace_text.tgz")], check=False)
        print(f"\n==== RESULT {runid} ====", flush=True)
        for f in ("hermes_summary.json", "eval_result.json"):
            p = os.path.join(outdir, f)
            print(f"--- {f} ---\n{open(p).read() if os.path.isfile(p) else 'MISSING'}", flush=True)
    finally:
        run(["docker", "cp", f"{cname}:{hermes_dir}/state.db", os.path.join(outdir, "hermes_state.db")], check=False)
        if not args.keep:
            run(["docker", "rm", "-f", cname], check=False)
            senv.destroy()
            try:
                os.killpg(reaper.pid, 15)
            except Exception:
                pass
        print(f"[outputs in {outdir}]", flush=True)


if __name__ == "__main__":
    main()
