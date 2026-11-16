# Unfinished-Bench
# Copyright (c) 2026-present NAVER Corp.
# Apache-2.0
"""Server side of one cell: a private network, a shared volume (agent /outputs = server share mount) and the
server container that runs the company's backends (ops-api). The agent container only has thin CLI clients;
all state lives on the server, out of the agent's reach.

Used by harness/run_cell.py. Removes only what it created (names <tag>-*).

Order: create() -> start the agent container with agent_run_args() -> agent setup (init.sh, env=agent_env())
       -> driver (GOAL_PROBE=goal_probe()) -> collect_evidence(agent) -> grade() -> state_tar() -> destroy().
"""
import json
import os
import random
import shutil
import subprocess
import tempfile
import time
import uuid

HERE = os.path.dirname(os.path.abspath(__file__))

# No internet from inside a cell. The cell network is created with --internal, and each cell gets a small relay container
#   (<tag>-gw) that answers inside the cell network under the host name of the model endpoint (LLM_API_BASE) and forwards each
#   TCP connection to that endpoint's address only (resolved on the host before the cell starts). The driver keeps using the
#   same URL; no other outside address is reachable from the cell. NET_INTERNAL=0 leaves the network open and starts no relay
#   (needed, for example, when the endpoint is on the host's loopback interface).
NET_INTERNAL = os.environ.get("NET_INTERNAL", "1") == "1"
_RELAY = r"""
import socket, sys, threading
UP = (sys.argv[1], int(sys.argv[2]))
def pipe(a, b):
    try:
        while True:
            d = a.recv(65536)
            if not d:
                break
            b.sendall(d)
    except Exception:
        pass
    finally:
        for x in (a, b):
            try:
                x.shutdown(socket.SHUT_RDWR)
            except Exception:
                pass
def handle(c):
    try:
        u = socket.create_connection(UP, timeout=30)
    except Exception:
        c.close()
        return
    u.settimeout(None)
    threading.Thread(target=pipe, args=(c, u), daemon=True).start()
    pipe(u, c)
    c.close(); u.close()
s = socket.socket(); s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("0.0.0.0", int(sys.argv[3]))); s.listen(256)
while True:
    c, _ = s.accept()
    threading.Thread(target=handle, args=(c,), daemon=True).start()
"""


def _run(args, check=True, timeout=300):
    r = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
    if check and r.returncode != 0:
        raise RuntimeError(f"{' '.join(args[:4])}…: rc={r.returncode} {(r.stderr or '').strip()[-400:]}")
    return r


class SplitEnv:
    def __init__(self, tdir, manifest, tag, image, label="unfinished-bench=1", extra_env=None):
        self.tdir, self.man, self.image, self.label = tdir, manifest["split"], image, label
        self.extra_env = dict(extra_env or {})            # virtual clock (virtual_clock.container_env) for the server container
        self.service_dirs = list(manifest.get("service_dirs", []))
        self.net, self.vol, self.srv = f"{tag}-net", f"{tag}-home", f"{tag}-svc"
        self.gw = f"{tag}-gw"
        self.token = uuid.uuid4().hex
        self.anchor = None
        self.made = []                                   # what we created, removed in reverse order

    # ── server side ──
    def _network(self):
        inet = ["--internal"] if NET_INTERNAL else []
        r = _run(["docker", "network", "create", "--label", self.label, *inet, self.net], check=False)
        if r.returncode != 0:                             # default address pools exhausted: pick a private subnet
            for _ in range(12):
                sub = f"10.{random.randint(180, 250)}.{random.randint(0, 255)}.0/24"
                r = _run(["docker", "network", "create", "--label", self.label, *inet, "--subnet", sub, self.net], check=False)
                if r.returncode == 0:
                    break
        if r.returncode != 0:
            raise RuntimeError(f"network create failed: {r.stderr.strip()[-300:]}")
        self.made.append(("network", self.net))

    def _relay(self):
        """Endpoint relay (<tag>-gw): started on the default bridge (outside), then attached to the cell network under the
        endpoint's host name. Without LLM_API_BASE there is nothing to relay."""
        import socket
        from urllib.parse import urlparse
        base = os.environ.get("LLM_API_BASE")
        if not base:
            return
        u = urlparse(base)
        host, port = u.hostname, u.port or (443 if u.scheme == "https" else 80)
        # If the host name does not resolve right now (e.g. a VPN drop), use the last address that did, so cell setup still works.
        cache = os.path.join(HERE, ".endpoint_ip_cache")
        try:
            ip = socket.gethostbyname(host)
            try:
                open(cache, "w").write(ip)
            except OSError:
                pass
        except OSError:
            if not os.path.isfile(cache):
                raise
            ip = open(cache).read().strip()
        _run(["docker", "run", "-d", "--name", self.gw, "--label", self.label, "--pids-limit", "128", "--memory", "128m",
              self.image, "python3", "-c", _RELAY, ip, str(port), str(port)])
        self.made.append(("container", self.gw))
        _run(["docker", "network", "connect", "--alias", host, self.net, self.gw])
        for _ in range(40):
            h = _run(["docker", "exec", self.gw, "python3", "-c",
                      f"import socket;socket.create_connection(('127.0.0.1',{port}),timeout=2)"], check=False)
            if h.returncode == 0:
                return
            time.sleep(0.5)
        raise RuntimeError("gateway relay did not come up")

    def create(self, log=None):
        self._network()
        if NET_INTERNAL:
            self._relay()
        _run(["docker", "volume", "create", "--label", self.label, self.vol])
        self.made.append(("volume", self.vol))
        aliases = sum((["--network-alias", a] for a in self.man["aliases"]), [])
        _run(["docker", "run", "-d", "--name", self.srv, "--label", self.label, "--network", self.net, *aliases,
              "--hostname", "ops-api-1", "-v", f"{self.vol}:{self.man['share_mount']}",
              *sum((["-e", f"{k}={v}"] for k, v in self.extra_env.items()), []),
              "--pids-limit", "256", "--memory", "768m", self.image, "sleep", "infinity"])
        self.made.append(("container", self.srv))
        _run(["docker", "exec", self.srv, "mkdir", "-p", "/utils", self.man["share_mount"]])
        _run(["docker", "cp", os.path.join(self.tdir, "_private", "server") + "/.", f"{self.srv}:/utils/"])
        r = _run(["docker", "exec", self.srv, "bash", "/utils/init.sh"], check=False, timeout=300)
        if log is not None:
            log.write(f"[server init] rc={r.returncode}\n{r.stdout}\n===STDERR===\n{r.stderr}\n")
        if r.returncode != 0:
            raise RuntimeError(f"server init failed rc={r.returncode}: {(r.stderr or '')[-800:]}")
        self.anchor = next((l.split("=", 1)[1].strip() for l in r.stdout.splitlines() if l.startswith("anchor=")), None)
        _run(["docker", "exec", "-d", "-e", f"PROBE_TOKEN={self.token}", self.srv, "python3", "/srv/opsapi/opsapi.py"])
        for _ in range(40):
            h = _run(["docker", "exec", self.srv, "python3", "-c",
                      f"import urllib.request;urllib.request.urlopen('http://127.0.0.1:{self.man['port']}/healthz',timeout=2)"], check=False)
            if h.returncode == 0:
                return
            time.sleep(0.5)
        raise RuntimeError("ops-api did not come up")

    # ── agent side ──
    def agent_run_args(self):
        return ["--network", self.net, "-v", f"{self.vol}:/outputs"]

    def agent_env(self):
        return {"OPSKIT_ANCHOR": self.anchor} if self.anchor else {}

    def goal_probe(self):
        return {"kind": "http_ok", "url": f"http://{self.man['aliases'][0]}/v1/_probe/goal", "token": self.token}

    # ── grading ──
    def collect_evidence(self, agent):
        """Copy the agent-side evidence (identity and client files) to a host temp folder. Missing paths are skipped;
        the evaluator treats them as absent."""
        tmp = tempfile.mkdtemp(prefix="ubench-ev-")
        root = os.path.join(tmp, "agent")
        os.makedirs(root)
        missing = []
        for p in self.man["agent_evidence"]:
            dst = os.path.join(root, p.lstrip("/"))
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            if _run(["docker", "cp", f"{agent}:{p}", dst], check=False).returncode != 0:
                missing.append(p)
        return tmp, missing

    def grade(self, ev_tmp, evaluator, run_eval, timeout=180):
        """Grade inside the server container, with the evidence in agent/ next to the evaluator.
        Returns (rc, stdout, stderr, result JSON string or None)."""
        # Stop ops-api (including its periodic workers) first, so no write lands while the evaluator reads the state.
        # "[/]" keeps the pattern from matching this shell's own command line.
        _run(["docker", "exec", self.srv, "bash", "-lc",
              "pkill -f '[/]srv/opsapi/opsapi.py'; for i in $(seq 40); do pgrep -f '[/]srv/opsapi/' >/dev/null || break; sleep 0.25; done"],
             check=False, timeout=60)
        ed = "/tmp/.ev-" + uuid.uuid4().hex[:6]
        _run(["docker", "exec", self.srv, "mkdir", "-p", ed])
        _run(["docker", "cp", os.path.join(ev_tmp, "agent"), f"{self.srv}:{ed}/agent"])
        _run(["docker", "cp", evaluator, f"{self.srv}:{ed}/evaluator.py"])
        _run(["docker", "cp", run_eval, f"{self.srv}:{ed}/run_eval.py"])
        r = _run(["docker", "exec", self.srv, "python3", f"{ed}/run_eval.py", "--result_path", f"{ed}/eval_result.json"],
                 check=False, timeout=timeout)
        res = _run(["docker", "exec", self.srv, "cat", f"{ed}/eval_result.json"], check=False)
        return r.returncode, r.stdout, r.stderr, (res.stdout if res.returncode == 0 else None)

    def state_tar(self, dst, ev_tmp=None):
        """For analysis: server state, audit and request logs (and the agent-side evidence) as tgz archives."""
        dirs = " ".join(self.service_dirs)
        _run(["docker", "exec", self.srv, "bash", "-lc", f"tar czf /tmp/.svc.tgz {dirs} 2>/dev/null || true"], check=False)
        _run(["docker", "cp", f"{self.srv}:/tmp/.svc.tgz", dst], check=False)
        if ev_tmp:
            shutil.make_archive(dst[:-4] + "_agent", "gztar", ev_tmp)

    # ── cleanup ──
    def destroy(self):
        for kind, name in reversed(self.made):
            if kind == "container":
                _run(["docker", "rm", "-f", name], check=False)
            elif kind == "volume":
                _run(["docker", "volume", "rm", "-f", name], check=False)
            elif kind == "network":
                _run(["docker", "network", "rm", name], check=False)
        self.made = []
