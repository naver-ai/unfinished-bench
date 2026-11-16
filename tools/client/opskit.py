# Unfinished-Bench
# Copyright (c) 2026-present NAVER Corp.
# Apache-2.0
"""opskit — shared client for the platform team's internal CLIs.

Each CLI is a thin wrapper around the ops API: the command line is sent to the service behind it,
which runs the command and returns its output and exit status. Service endpoints are listed in
/etc/opskit/client.json; the caller's identity comes from /etc/opskit/identity.json.
"""
import json
import os
import socket
import sys
import urllib.error
import urllib.request

ETC = os.environ.get("OPSKIT_ETC", "/etc/opskit")
TIMEOUT = 180


def _load(name, default):
    try:
        with open(os.path.join(ETC, name)) as f:
            return json.load(f)
    except (OSError, ValueError):
        return default


def _files(prog, argv, file_opts):
    """Options that name a local file (e.g. --exclude-file) are read here and sent with the request."""
    out = {}
    for i, arg in enumerate(argv):
        for opt in file_opts:
            if arg == opt and i + 1 < len(argv):
                path = argv[i + 1]
            elif arg.startswith(opt + "="):
                path = arg.split("=", 1)[1]
            else:
                continue
            try:
                with open(path, encoding="utf-8", errors="replace") as f:
                    out[path] = f.read()
            except OSError as e:
                print(f"{prog}: {path}: {e.strerror}", file=sys.stderr)
                sys.exit(2)
    return out


def _write(stream, text):
    try:
        stream.write(text)
        stream.flush()
    except BrokenPipeError:
        try:
            os.dup2(os.open(os.devnull, os.O_WRONLY), stream.fileno())
        except OSError:
            pass
        sys.exit(141)


def client(prog, file_opts=()):
    cfg = _load("client.json", {})
    base = (cfg.get("services") or {}).get(prog) or cfg.get("endpoint")
    if not base:
        print(f"{prog}: no endpoint configured for {prog} (see {ETC}/client.json)", file=sys.stderr)
        sys.exit(78)
    argv = sys.argv[1:]
    body = {"argv": argv, "identity": _load("identity.json", {}), "host": socket.gethostname(),
            "cwd": os.getcwd(), "files": _files(prog, argv, file_opts)}
    req = urllib.request.Request(base.rstrip("/") + f"/v1/{prog}/exec", data=json.dumps(body).encode(), method="POST",
                                 headers={"Content-Type": "application/json", "User-Agent": f"opskit/{prog}"})
    try:
        with urllib.request.urlopen(req, timeout=cfg.get("timeout", TIMEOUT)) as r:
            res = json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        try:
            msg = json.loads(e.read().decode()).get("error") or e.reason
        except Exception:
            msg = e.reason
        print(f"{prog}: {base}: {e.code} {msg}", file=sys.stderr)
        sys.exit(69)
    except (urllib.error.URLError, OSError) as e:
        reason = getattr(e, "reason", e)
        print(f"{prog}: cannot reach {base} ({reason})", file=sys.stderr)
        sys.exit(69)
    _write(sys.stdout, res.get("stdout", ""))
    _write(sys.stderr, res.get("stderr", ""))
    sys.exit(int(res.get("rc", 1)))
