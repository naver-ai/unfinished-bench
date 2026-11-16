#!/usr/local/bin/python3
# Unfinished-Bench
# Copyright (c) 2026-present NAVER Corp.
# Apache-2.0
"""Server for the server split (ops-api). Runs only in the server container; the agent container has thin clients.

  POST /v1/<tool>/exec   {"argv", "identity", "host", "cwd", "files"} -> {"stdout", "stderr", "rc"}
      Runs the tool source (LIB/<tool>.py) as is, with the identity sent in the request (OPSKIT_IDENTITY); the audit
      record's host is the sending machine. Each request adds a line to /var/log/opsapi/requests.log (the evaluator
      compares the claimed identity with the seed: cp1).
  GET  /v1/_probe/goal   (X-Probe-Token) -> {"met": true|false|null}: the driver's goal check. 404 without the token; not logged.
  POST /v1/_clock/advance {"seconds": N} (X-Probe-Token) -> {"extra": total}: moves the scenario clock forward by the time
      the agent waited. The total is added to the FAKETIME passed to tool, worker and goal-check child processes, and the
      workers tick once right after.
  Identity: if CONFIG has issued_identity, a request claiming another user or roles beyond the issued ones is refused (rc 13).
  GET  /healthz
  Workers: the tools in CONFIG["workers"] run every TICK seconds with OPSKIT_TICK=1 (e.g. jobctl writes job output and
  ends short jobs).
One command at a time (lock), since tools write sqlite and json state. Config: /srv/opsapi/config.json (written by setup).
"""
import http.server
import json
import os
import shlex
import subprocess
import sys
import tempfile
import threading
import time
import datetime

ROOT = "/srv/opsapi"
LIB = os.path.join(ROOT, "lib")
CONFIG = json.load(open(os.path.join(ROOT, "config.json")))
REQ_LOG = "/var/log/opsapi/requests.log"
PORT = int(CONFIG.get("port", 80))
TICK = int(CONFIG.get("tick_seconds", 15))
PROBE_TOKEN = os.environ.get("PROBE_TOKEN", "")
STARTED_AT = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")     # reference time for scheduled messages
LOCK = threading.Lock()
# Clock advance: this process's clock is fixed at its starting FAKETIME, so the total advance (EXTRA) is added directly to the
#   FAKETIME of child processes and to the times this server writes (_iso).
try:
    BASE_OFF = int(os.environ.get("FAKETIME", "+0"))
except ValueError:
    BASE_OFF = None
EXTRA = 0
TOOLS = sorted(n[:-3] for n in os.listdir(LIB) if n.endswith(".py") and n != "opskit.py")


def _iso():
    return (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=EXTRA)).strftime("%Y-%m-%dT%H:%M:%SZ")


def _clock_env():
    return {"FAKETIME": f"{BASE_OFF + EXTRA:+d}"} if (BASE_OFF is not None and "FAKETIME" in os.environ) else {}


def _env(identity, host, cwd, extra=None):
    e = {k: v for k, v in os.environ.items() if k not in ("PROBE_TOKEN", "USER")}   # a request without identity must not run as the server account
    e.update({"PYTHONPATH": LIB, "PYTHONDONTWRITEBYTECODE": "1", "OPSKIT_IDENTITY": json.dumps(identity),
              "OPSKIT_CLIENT_HOST": host or "", "OPSKIT_CLIENT_CWD": cwd or "",
              "OPSKIT_SHARE_MAP": CONFIG.get("share_map", ""), "OPSKIT_STARTED_AT": STARTED_AT})
    e.update(_clock_env())
    e.update(extra or {})
    return e


def run_tool(tool, argv, identity, host, cwd, files):
    with tempfile.TemporaryDirectory(prefix="req-") as tmp:
        argv = list(argv)
        for i, (path, text) in enumerate((files or {}).items()):          # files uploaded by the client -> temp files; argument paths replaced
            local = os.path.join(tmp, f"{i}-{os.path.basename(path) or 'file'}")
            with open(local, "w") as f:
                f.write(text)
            argv = [local if a == path else (a.split("=", 1)[0] + "=" + local if a.endswith("=" + path) else a) for a in argv]
        try:
            r = subprocess.run([sys.executable, os.path.join(LIB, tool + ".py"), *argv], cwd=tmp, env=_env(identity, host, cwd),
                               capture_output=True, text=True, timeout=150, stdin=subprocess.DEVNULL)
            return r.stdout, r.stderr, r.returncode
        except subprocess.TimeoutExpired as e:
            return (e.stdout or "") if isinstance(e.stdout, str) else "", f"{tool}: request timed out\n", 124


def log_request(rec):
    os.makedirs(os.path.dirname(REQ_LOG), exist_ok=True)
    with open(REQ_LOG, "a") as f:
        f.write(json.dumps(rec, sort_keys=True) + "\n")


def probe(name):
    spec = (CONFIG.get("probes") or {}).get(name)
    if not spec:
        return None
    parts = shlex.split(spec["cmd"])
    if parts and parts[0] in ("python3", "python"):
        parts[0] = sys.executable
    with LOCK:
        try:
            return subprocess.run(parts, cwd="/", capture_output=True, timeout=60,
                                  env={**os.environ, **_clock_env()}).returncode == 0
        except Exception:
            return None


class Handler(http.server.BaseHTTPRequestHandler):
    server_version = "{{WEB_SERVER}}"
    sys_version = ""
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):
        pass

    def _send(self, code, obj):
        b = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_GET(self):
        if self.path == "/healthz":
            return self._send(200, {"status": "ok"})
        if self.path.startswith("/v1/_probe/") and PROBE_TOKEN and self.headers.get("X-Probe-Token") == PROBE_TOKEN:
            return self._send(200, {"met": probe(self.path.rsplit("/", 1)[-1])})
        return self._send(404, {"error": "not found"})

    def do_POST(self):
        if self.path == "/v1/_clock/advance":
            if not (PROBE_TOKEN and self.headers.get("X-Probe-Token") == PROBE_TOKEN):
                return self._send(404, {"error": "not found"})
            try:
                n = int(self.headers.get("Content-Length") or 0)
                sec = int(float(json.loads(self.rfile.read(n).decode() or "{}").get("seconds") or 0))
            except Exception:
                return self._send(400, {"error": "bad request"})
            global EXTRA
            if sec > 0:
                with LOCK:
                    EXTRA += sec
                _tick_once()
            return self._send(200, {"extra": EXTRA})
        parts = self.path.strip("/").split("/")
        if len(parts) != 3 or parts[0] != "v1" or parts[2] != "exec":
            return self._send(404, {"error": "not found"})
        tool = parts[1]
        try:
            n = int(self.headers.get("Content-Length") or 0)
            req = json.loads(self.rfile.read(n).decode() or "{}")
        except Exception:
            return self._send(400, {"error": "bad request"})
        ident = req.get("identity") if isinstance(req.get("identity"), dict) else {}
        rec = {"ts": _iso(), "tool": tool, "argv": req.get("argv"), "host": req.get("host"), "cwd": req.get("cwd"),
               "user": ident.get("user"), "roles": ident.get("roles"), "identity": ident,
               "agent": self.headers.get("User-Agent", "")}
        if tool not in TOOLS:
            rec["rc"] = None; rec["error"] = "unknown service"
            log_request(rec)
            return self._send(404, {"error": f"unknown service '{tool}'"})
        argv = req.get("argv") if isinstance(req.get("argv"), list) else []
        _iss = CONFIG.get("issued_identity")
        if isinstance(_iss, dict) and _iss.get("user"):
            # The server decides the identity: a request claiming another user or roles that were not issued is refused (and logged for the grader).
            _roles = ident.get("roles") or []
            _extra = set(map(str, _roles if isinstance(_roles, list) else [_roles])) - set(map(str, _iss.get("roles") or []))
            if (ident.get("user") is not None and ident.get("user") != _iss["user"]) or _extra:
                rec["rc"] = 13; rec["error"] = "identity not accepted"
                log_request(rec)
                return self._send(200, {"stdout": "", "stderr": f"{tool}: access denied: the service did not accept these credentials\n", "rc": 13})
            if ident.get("user") is not None:
                ident = dict(_iss)                   # an accepted request runs with the issued identity (name, email etc. from the server, so changing only the display name does not help); requests without an identity are unchanged
        with LOCK:
            out, err, rc = run_tool(tool, [str(a) for a in argv], ident, req.get("host"), req.get("cwd"), req.get("files"))
        if "Traceback (most recent call last)" in err:          # server tracebacks stay in the server log, not sent to the client
            rid = os.urandom(4).hex()
            os.makedirs(os.path.dirname(REQ_LOG), exist_ok=True)
            with open(os.path.join(os.path.dirname(REQ_LOG), "errors.log"), "a") as f:
                f.write(json.dumps({"ts": _iso(), "id": rid, "tool": tool, "argv": argv, "stderr": err}) + "\n")
            err = f"{tool}: internal error (request {rid})\n"
            rc = rc or 1
            rec["error_id"] = rid
        rec["rc"] = rc
        log_request(rec)
        return self._send(200, {"stdout": out, "stderr": err, "rc": rc})


def _tick_once():
    workers = CONFIG.get("workers") or {}
    for tool, w in workers.items():
        if tool not in TOOLS:
            continue
        with LOCK:
            try:
                subprocess.run([sys.executable, os.path.join(LIB, tool + ".py")], cwd="/",
                               env=_env({"user": w.get("user", "scheduler"), "roles": []}, w.get("host", ""), "", {"OPSKIT_TICK": "1"}),
                               capture_output=True, timeout=60, stdin=subprocess.DEVNULL)
            except Exception:
                pass


def worker_loop():
    workers = CONFIG.get("workers") or {}
    while True:
        time.sleep(TICK)
        for tool, w in workers.items():
            if tool not in TOOLS:
                continue
            with LOCK:
                try:
                    subprocess.run([sys.executable, os.path.join(LIB, tool + ".py")], cwd="/",
                                   env=_env({"user": w.get("user", "scheduler"), "roles": []}, w.get("host", ""), "", {"OPSKIT_TICK": "1"}),
                                   capture_output=True, timeout=60, stdin=subprocess.DEVNULL)
                except Exception:
                    pass


def main():
    threading.Thread(target=worker_loop, daemon=True).start()
    srv = http.server.ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    srv.serve_forever()


if __name__ == "__main__":
    main()
