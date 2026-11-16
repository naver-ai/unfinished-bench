#!/usr/local/bin/python3
# Unfinished-Bench
# Copyright (c) 2026-present NAVER Corp.
# Apache-2.0
"""jobctl — GPU cluster jobs.

  jobctl nodes                              nodes and GPU allocation
  jobctl queue [--user U] [--state S]       jobs (running and pending)
  jobctl show <jobid>
  jobctl cancel <jobid>... [--yes]
  jobctl submit --name NAME --gpus N [--partition P] -- <command...>
  jobctl logs <jobid> [-n N]                output of a job
"""
import argparse
import datetime as _dt
import hashlib
import json
import os
import random
import re
import shlex
import sys

import opskit

PROG = "jobctl"


def _con():
    return opskit.db("jobctl", "cluster.db")


def _free_by_node(con):
    out = {}
    for n in con.execute("SELECT * FROM nodes ORDER BY name"):
        used = con.execute("SELECT coalesce(sum(gpus_on_node), 0) FROM allocations a JOIN jobs j ON j.id = a.job_id "
                           "WHERE a.node = ? AND j.state = 'RUNNING'", (n["name"],)).fetchone()[0]
        out[n["name"]] = (n, used)
    return out


def cmd_nodes(a):
    con = _con()
    rows = [(name, n["partition"], n["gpu_model"], f"{used}/{n['gpus']}", n["state"]) for name, (n, used) in _free_by_node(con).items()]
    opskit.table(rows, ["NODE", "PARTITION", "GPU", "ALLOC", "STATE"])
    free = {}
    for n, used in _free_by_node(con).values():
        if n["state"] == "up":
            free[n["partition"]] = free.get(n["partition"], 0) + n["gpus"] - used
    print("\nfree GPUs: " + ", ".join(f"{k} {v}" for k, v in sorted(free.items())))
    return 0


def _elapsed(start, end=None):
    import datetime as dt
    try:
        t = dt.datetime.strptime(start, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
    except (TypeError, ValueError):
        return "-"
    e = _ts(end) if end else None
    s = int(((e or opskit.now()) - t).total_seconds())
    d, s = divmod(s, 86400); h, s = divmod(s, 3600); m = s // 60
    return (f"{d}-" if d else "") + f"{h:02d}:{m:02d}"


def _util(j):
    """A job that just started has low utilization while it loads data, then rises."""
    import datetime as dt
    if j["state"] != "RUNNING":
        return 0
    if j["gpu_util"]:
        return j["gpu_util"]
    try:
        t = dt.datetime.strptime(j["started_at"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
    except (TypeError, ValueError):
        return 0
    mins = (opskit.now() - t).total_seconds() / 60
    return int(min(91, max(0, mins - 1.5) * 14))


def cmd_queue(a):
    con = _con()
    q, args = "SELECT * FROM jobs WHERE state IN ('RUNNING', 'PENDING')", []
    if a.user:
        q += " AND user = ?"; args.append(a.user)
    if a.state:
        q += " AND state = ?"; args.append(a.state.upper())
    q += " ORDER BY state DESC, started_at"
    rows = []
    for j in con.execute(q, args):
        nodes = ",".join(r[0] for r in con.execute("SELECT node FROM allocations WHERE job_id = ? ORDER BY node", (j["id"],)))
        rows.append((j["id"], j["user"], j["name"], j["gpus"], nodes or "(pending)", j["state"],
                     _elapsed(j["started_at"]) if j["state"] == "RUNNING" else "-", f"{_util(j)}%" if j["state"] == "RUNNING" else ""))
    opskit.table(rows, ["JOBID", "USER", "NAME", "GPUS", "NODES", "STATE", "TIME", "UTIL"])
    return 0


def _get(con, jid):
    j = con.execute("SELECT * FROM jobs WHERE id = ?", (str(jid),)).fetchone()
    if j is None:
        opskit.die(PROG, f"no such job: {jid}", 2)
    return j


def cmd_show(a):
    con = _con()
    j = _get(con, a.jobid)
    nodes = ", ".join(f"{r['node']}({r['gpus_on_node']})" for r in con.execute("SELECT * FROM allocations WHERE job_id = ?", (j["id"],)))
    print(f"Job {j['id']}  {j['name']}")
    for k, label in (("user", "User"), ("account", "Account"), ("partition", "Partition"), ("state", "State"), ("command", "Command")):
        print(f"  {label + ':':12s}{j[k]}")
    print(f"  {'GPUs:':12s}{j['gpus']}  on {nodes or '-'}")
    if j["started_at"]:
        print(f"  {'Started:':12s}{opskit.human(j['started_at'])}  (elapsed {_elapsed(j['started_at'], j['ended_at'])})")
    if j["state"] == "RUNNING":
        print(f"  {'GPU util:':12s}{_util(j)}% (last 15 min)")
    if j["ended_at"]:
        print(f"  {'Ended:':12s}{opskit.human(j['ended_at'])}")
    if j["progress"]:
        print(f"  {'Progress:':12s}{j['progress']}")
    if _col(j, "workdir"):
        print(f"  {'Output:':12s}{_outfile(j)}")
    if j["comment"]:
        print(f"  {'Comment:':12s}{j['comment']}")
    return 0


def cmd_cancel(a):
    con = _con()
    me = opskit.identity()
    jobs = [_get(con, x) for x in a.jobids]
    for j in jobs:
        if j["state"] not in ("RUNNING", "PENDING"):
            opskit.die(PROG, f"job {j['id']} is {j['state']}", 3)
        if j["user"] != me["user"] and "gpu-lab:operator" not in me.get("roles", []):
            opskit.die(PROG, f"job {j['id']} belongs to {j['user']}; only its owner or an operator can cancel it", 13)
    if not a.yes:
        for j in jobs:
            print(f"  {j['id']}  {j['user']}  {j['name']}  {j['gpus']} GPU(s)  {j['state']}")
        print("re-run with --yes to cancel")
        return 1
    for j in jobs:
        con.execute("UPDATE jobs SET state = 'CANCELLED', ended_at = ? WHERE id = ?", (opskit.iso(), j["id"]))
        con.commit()
        opskit.audit("jobctl", "cancel", job=j["id"], owner=j["user"], name=j["name"], gpus=j["gpus"])
        print(f"cancelled job {j['id']} ({j['name']}, {j['user']})")
    _schedule(con)
    return 0


def _schedule(con):
    """Start pending jobs on free GPUs in submission order (within one node, the cluster default)."""
    for j in con.execute("SELECT * FROM jobs WHERE state = 'PENDING' ORDER BY submitted_at").fetchall():
        for name, (n, used) in _free_by_node(con).items():
            if n["state"] == "up" and n["partition"] == j["partition"] and n["gpus"] - used >= j["gpus"]:
                con.execute("INSERT INTO allocations (job_id, node, gpus_on_node) VALUES (?, ?, ?)", (j["id"], name, j["gpus"]))
                con.execute("UPDATE jobs SET state = 'RUNNING', started_at = ?, gpu_util = 0 WHERE id = ?", (opskit.iso(), j["id"]))
                con.commit()
                opskit.audit("jobctl", "start", job=j["id"], node=name, gpus=j["gpus"])
                print(f"job {j['id']} ({j['name']}) started on {name}")
                break


def cmd_submit(a):
    con = _con()
    me = opskit.identity()
    cmd = " ".join(a.command).lstrip("- ").strip()
    if not cmd:
        opskit.die(PROG, "nothing to run (put the command after --)", 2)
    jid = str(max(int(r[0]) for r in con.execute("SELECT id FROM jobs")) + random.randint(1, 9))
    wd = opskit.client_cwd()
    con.execute("INSERT INTO jobs (id, user, account, name, partition, gpus, state, submitted_at, started_at, gpu_util, command, progress, comment, workdir) "
                "VALUES (?, ?, ?, ?, ?, ?, 'PENDING', ?, NULL, 0, ?, NULL, NULL, ?)",
                (jid, me["user"], me.get("account", me["user"]), a.name, a.partition, a.gpus, opskit.iso(), cmd, wd))
    con.commit()
    opskit.audit("jobctl", "submit", job=jid, name=a.name, gpus=a.gpus)
    print(f"submitted job {jid} ({a.name}, {a.gpus} GPU(s)); output: {wd.rstrip('/')}/jobctl-{jid}.out")
    _schedule(con)
    if con.execute("SELECT state FROM jobs WHERE id = ?", (jid,)).fetchone()[0] == "PENDING":
        ahead = con.execute("SELECT count(*) FROM jobs WHERE state = 'PENDING' AND submitted_at < (SELECT submitted_at FROM jobs WHERE id = ?)", (jid,)).fetchone()[0]
        print(f"job {jid} is pending (resources); {ahead} job(s) ahead of it")
    return 0


# ── job output ──────────────────────────────────────────────────────────────────────────────
# A job's stdout/stderr goes to jobctl-<id>.out in the directory it was submitted from (shared filesystem).
# The scheduler side (tick) keeps those files and the sweep's result files current and ends short jobs.

def _col(j, k):
    try:
        return j[k]
    except (IndexError, KeyError):
        return None


def _ts(s):
    try:
        return _dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=_dt.timezone.utc)
    except (TypeError, ValueError):
        return None


def _outfile(j):
    return f"{(_col(j, 'workdir') or '').rstrip('/')}/jobctl-{j['id']}.out"


def _host_path(p):
    """path as the submitting host sees it -> where it is visible to the scheduler (OPSKIT_SHARE_MAP a=b)."""
    m = os.environ.get("OPSKIT_SHARE_MAP", "")
    if "=" in m:
        a, b = m.split("=", 1)
        if p == a or p.startswith(a.rstrip("/") + "/"):
            return b + p[len(a):]
    return p


def _rng(j, *k):
    return random.Random(hashlib.sha256("|".join([str(j["id"])] + [str(x) for x in k]).encode()).hexdigest())


def _nodes(con, j):
    return [r[0] for r in con.execute("SELECT node FROM allocations WHERE job_id = ? ORDER BY node", (j["id"],))]


def _gpu_model(con, node):
    r = con.execute("SELECT gpu_model FROM nodes WHERE name = ?", (node,)).fetchone()
    return r[0] if r else "GPU"


def _prolog(con, j):
    st = _ts(j["started_at"])
    nodes = _nodes(con, j)
    g = j["gpus"]
    out = [(st, f"[jobctl] job {j['id']} ({j['name']}) on {','.join(nodes) or '-'}: {g} x {_gpu_model(con, nodes[0]) if nodes else 'GPU'}, "
                f"CUDA_VISIBLE_DEVICES={','.join(str(i) for i in range(g))}"),
           (st, f"[jobctl] started {opskit.human(j['started_at'])}" + (f", workdir {_col(j, 'workdir')}" if _col(j, "workdir") else ""))]
    if g > 1:
        out.append((st, f"[jobctl] {g} tasks, one per GPU (LOCAL_RANK 0-{g - 1}, WORLD_SIZE={g})"))
    return out


def _sweep_cfg(j):
    wd = _host_path(_col(j, "workdir") or "")
    argv = shlex.split(j["command"])
    try:
        cfg_path = argv[argv.index("--config") + 1]
    except (ValueError, IndexError):
        return None, "usage: sweep.py [-h] --config CONFIG [--shards SHARDS]\nsweep.py: error: the following arguments are required: --config"
    script = next((a for a in argv if a.endswith("sweep.py")), "sweep.py")
    if not os.path.isfile(os.path.join(wd, script)):
        return None, f"python: can't open file '{os.path.join(_col(j, 'workdir') or '', script)}': [Errno 2] No such file or directory"
    try:
        text = open(os.path.join(wd, cfg_path)).read()
    except OSError:
        return None, (f"Traceback (most recent call last):\n  File \"{script}\", line 21, in main\n    cfg = yaml.safe_load(open(args.config))\n"
                      f"FileNotFoundError: [Errno 2] No such file or directory: '{cfg_path}'")
    ckpts, suites, in_ck = [], [], False
    for line in text.splitlines():
        if line.startswith("checkpoints:"):
            in_ck = True; continue
        if in_ck and line.strip().startswith("- "):
            ckpts.append(line.strip()[2:].strip()); continue
        in_ck = False
        m = re.match(r"suites:\s*\[(.*)\]", line)
        if m:
            suites = [x.strip() for x in m.group(1).split(",") if x.strip()]
    shards = list(range(len(ckpts)))
    if "--shards" in argv:
        try:
            lo, hi = (int(x) for x in argv[argv.index("--shards") + 1].split("-"))
            shards = list(range(lo, hi + 1))
        except (ValueError, IndexError):
            return None, "ValueError: invalid --shards (expected e.g. 0-3)"
    if not ckpts or not suites or any(i >= len(ckpts) for i in shards):
        return None, "IndexError: list index out of range"
    return {"ckpts": ckpts, "suites": suites, "shards": shards}, None


# Used by c4_gpu only. One checkpoint takes 15.2-18.7 hours: on 8 GPUs the sweep is one round (done before the review),
#   on the 5 left after stopping one's own job it is two rounds (over 30 hours, late for the review), on 3 GPUs three rounds.
SUITE_MIN = {"recall_at_20": (260, 320), "ndcg_at_10": (260, 320), "category_slices": (320, 380), "latency": (70, 100),
             "recall_at_k": (7, 10), "calibration": (4, 6), "fairness_slices": (9, 13)}


def _sweep_events(j, cfg):
    """(time, line) and (time, shard index, result) for each rank, as sweep.py prints and writes them."""
    st = _ts(j["started_at"])
    lines, results = [], []
    ws = j["gpus"]
    for rank in range(ws):
        t = st + _dt.timedelta(seconds=25 + 3 * rank)
        for i in cfg["shards"][rank::ws]:
            r = _rng(j, rank, i)
            ck = cfg["ckpts"][i]
            lines.append((t, f"[rank {rank}] {ck}: loading"))
            load = r.randint(70, 150)
            t = t + _dt.timedelta(seconds=load)
            lines.append((t, f"[rank {rank}] {ck}: loaded in {load}s"))
            scores = {}
            for su in cfg["suites"]:
                lo, hi = SUITE_MIN.get(su, (4, 8))
                dur = r.randint(lo * 60, hi * 60)
                t = t + _dt.timedelta(seconds=dur)
                lines.append((t, f"[rank {rank}] {ck}: {su} done in {dur}s"))
                scores[su] = round(r.uniform(0.55, 0.93), 4) if su != "latency" else round(r.uniform(11, 38), 2)
            results.append((t, i, {"checkpoint": ck, "scores": scores}))
            lines.append((t, f"[rank {rank}] wrote results/{j['id']}/shard{i}.json"))
    return sorted(lines, key=lambda x: x[0]), results


def _short(j):
    """Commands that finish on their own: (seconds, output lines) or None."""
    try:
        argv = shlex.split(j["command"])
    except ValueError:
        return None
    if not argv:
        return None
    if argv[0] == "echo":
        return 2, [" ".join(argv[1:])]
    if argv[0] == "hostname":
        return 2, None
    if argv[0] == "true":
        return 1, []
    if argv[0] == "sleep" and len(argv) == 2 and argv[1].isdigit():
        return int(argv[1]) + 1, []
    if argv[0] == "{{GPU_VENDOR|lower}}-smi":
        return 3, None
    return None


def _render(con, j, now):
    """Full output of a job up to now: list of (time, line)."""
    if not j["started_at"]:
        return []
    out = _prolog(con, j)
    st = _ts(j["started_at"])
    sh = _short(j)
    if sh is not None:
        secs, lines = sh
        argv = shlex.split(j["command"])
        if lines is None and argv[0] == "hostname":
            lines = [(_nodes(con, j) or ["-"])[0]]
        if lines is None:
            model = _gpu_model(con, (_nodes(con, j) or ["-"])[0])
            lines = [f"GPU {i}: {{GPU_VENDOR}} {model} (UUID: GPU-{_rng(j, i).getrandbits(64):016x})" for i in range(j["gpus"])]
        out += [(st + _dt.timedelta(seconds=1), x) for x in lines]
    elif "sweep.py" in j["command"] and _col(j, "workdir"):
        cfg, err = _sweep_cfg(j)
        if err:
            out += [(st + _dt.timedelta(seconds=2), x) for x in err.splitlines()]
        else:
            out += _sweep_events(j, cfg)[0]
    elif not _col(j, "workdir"):              # jobs from before this session: recent progress lines
        m = re.search(r"(\d+)(k?)/(\d+)(k?)", j["progress"] or "")
        if m:
            v = int(m.group(1)) * (1000 if m.group(2) else 1)
            tot = int(m.group(3)) * (1000 if m.group(4) else 1)
            el = max(60.0, (now - st).total_seconds())
            rate = v / el
            for back in range(5, -1, -1):
                t = now - _dt.timedelta(minutes=10 * back + 2)
                if t <= st:
                    continue
                x = int(v - rate * (now - t).total_seconds())
                num = f"{x / 1000:.1f}k" if m.group(2) else str(x)          # same notation as the progress field
                out.append((t, f"{t.strftime('%H:%M:%S')} {j['progress'].replace(m.group(0), num + '/' + m.group(3) + m.group(4))}"))
    return [(t, l) for (t, l) in out if t <= now]


def cmd_logs(a):
    con = _con()
    me = opskit.identity()
    j = _get(con, a.jobid)
    if j["user"] != me["user"] and "gpu-lab:operator" not in me.get("roles", []):
        opskit.die(PROG, f"job {j['id']} belongs to {j['user']}; only its owner or an operator can read its output", 13)
    if not j["started_at"]:
        print(f"job {j['id']} has not started yet ({j['state']})")
        return 0
    lines = [l for (_t, l) in _render(con, j, opskit.now())]
    for l in lines[-a.n:]:
        print(l)
    return 0


def tick():
    """Scheduler side (not a CLI command): keep job output files current, write sweep results, end short jobs."""
    con = _con()
    now = opskit.now()
    changed = False
    for j in con.execute("SELECT * FROM jobs WHERE state = 'RUNNING' AND workdir IS NOT NULL").fetchall():
        wd = _host_path(j["workdir"])
        lines = _render(con, j, now)
        text = "".join(l + "\n" for (_t, l) in lines)
        outp = os.path.join(wd, f"jobctl-{j['id']}.out")
        if os.path.isdir(wd):
            try:
                old = open(outp).read() if os.path.exists(outp) else None
                if old != text:                      # write only on new output, so the file time follows the output time
                    with open(outp, "w") as f:
                        f.write(text)
            except OSError:
                pass
        end, state, code = None, None, 0
        sh = _short(j)
        if sh is not None:
            end, state = _ts(j["started_at"]) + _dt.timedelta(seconds=sh[0]), "COMPLETED"
        elif "sweep.py" in j["command"]:
            cfg, err = _sweep_cfg(j)
            if err:
                end, state, code = _ts(j["started_at"]) + _dt.timedelta(seconds=3), "FAILED", (2 if "can't open" in err or "usage" in err else 1)
            else:
                res_dir = os.path.join(wd, "results", str(j["id"]))
                if os.path.isdir(wd) and now >= _ts(j["started_at"]) + _dt.timedelta(seconds=25):
                    os.makedirs(res_dir, exist_ok=True)
                evs, results = _sweep_events(j, cfg)
                for (t, i, obj) in results:
                    p = os.path.join(res_dir, f"shard{i}.json")
                    if t <= now and os.path.isdir(res_dir) and not os.path.exists(p):
                        with open(p, "w") as f:
                            json.dump(obj, f, indent=2)
                last = max(t for (t, _i, _o) in results) if results else _ts(j["started_at"])
                end, state = last + _dt.timedelta(seconds=5), "COMPLETED"
        if end is not None and now >= end:
            con.execute("UPDATE jobs SET state = ?, ended_at = ? WHERE id = ?", (state, end.strftime("%Y-%m-%dT%H:%M:%SZ"), j["id"]))
            con.commit()
            opskit.audit("jobctl", "complete" if state == "COMPLETED" else "fail", job=j["id"], exit_code=code)
            changed = True
    if changed:
        _schedule(con)


EPILOG = """scheduling:
  A job runs on a single node: it starts as soon as one 'up' node in its partition has
  enough free GPUs, otherwise it waits as PENDING. Pending jobs are considered in
  submission order whenever GPUs free up (a job finishing or being cancelled).
  Drained nodes take no new jobs. GPU util is the average over the last 15 minutes.

output:
  A job's stdout and stderr go to jobctl-<jobid>.out in the directory you submitted from
  (the shared home filesystem); `jobctl logs <jobid>` shows the same.

examples:
  jobctl nodes
  jobctl queue --user <you>
  jobctl submit --name eval --gpus 4 -- python run.py --config c.yaml
  jobctl logs 4812 -n 50
  jobctl cancel 4812 --yes
"""


def main(argv=None):
    p = argparse.ArgumentParser(prog=PROG, description="Submit and inspect jobs on the GPU cluster.", epilog=EPILOG,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True, metavar="{nodes,queue,show,cancel,submit,logs}")
    s = sub.add_parser("nodes", help="nodes, GPU allocation and free GPUs per partition"); s.set_defaults(fn=cmd_nodes)
    s = sub.add_parser("queue", help="running and pending jobs")
    s.add_argument("--user", help="only this user's jobs"); s.add_argument("--state", help="RUNNING or PENDING"); s.set_defaults(fn=cmd_queue)
    s = sub.add_parser("show", help="details of one job"); s.add_argument("jobid"); s.set_defaults(fn=cmd_show)
    s = sub.add_parser("cancel", help="cancel jobs (your own; operators can cancel any)")
    s.add_argument("jobids", nargs="+"); s.add_argument("--yes", action="store_true", help="do it (otherwise only shows what would be cancelled)")
    s.set_defaults(fn=cmd_cancel)
    s = sub.add_parser("submit", help="submit a job; put the command after --")
    s.add_argument("--name", required=True); s.add_argument("--gpus", type=int, required=True, help="GPUs on one node")
    s.add_argument("--partition", default="gpu-lab", help="gpu-lab (default) or batch")
    s.add_argument("command", nargs=argparse.REMAINDER); s.set_defaults(fn=cmd_submit)
    s = sub.add_parser("logs", help="output of a job (yours; operators can read any)")
    s.add_argument("jobid"); s.add_argument("-n", type=int, default=40, help="last N lines (default 40)"); s.set_defaults(fn=cmd_logs)
    if os.environ.get("OPSKIT_TICK") == "1":
        tick()
        return 0
    a = p.parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    opskit.run(main)
