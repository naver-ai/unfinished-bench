# Unfinished-Bench
# Copyright (c) 2026-present NAVER Corp.
# Apache-2.0
"""Virtual clock: inside the containers, "now" is the time the scenario was written for, not the real time.

At launch we take the scenario's local weekday and time (manifest "clock_gate", in the user's time zone) and
pick the date with that weekday closest to today (-3..+3 days). That instant is the anchor V. Both containers
(server and agent) shift their clocks by the same offset V - real_now with libfaketime plus a small stat() and
sleep shim (docker/virtual_clock). After start the clock runs at real speed, except that the agent driver moves it
forward when the agent waits (harness/agent_driver.py). Date placeholders in the scenario are filled from V
(OPSKIT_ANCHOR), so weekday and time of day match what the scenario was written for.

The two libraries are installed next to the C library as libtzcompat.so.1 (libfaketime) and libtzcompat-stat.so.1
(the shim). The agent container reads its offset from CONF (via /etc/ld.so.preload, so nothing shows in the agent's
environment); the server container gets it from environment variables.
"""
import datetime as _dt
import subprocess as _sp
import zoneinfo as _zi

CONF = "/etc/tzcompat.conf"
_ARCH = {"arm64": "aarch64", "amd64": "x86_64"}


def lib_dir(image):
    """Directory of the clock libraries in the image (the multiarch library directory of its architecture)."""
    r = _sp.run(["docker", "image", "inspect", "-f", "{{.Architecture}}", image], capture_output=True, text=True)
    arch = (r.stdout or "").strip()
    if r.returncode != 0 or not arch:
        raise RuntimeError(f"cannot inspect image {image}: {(r.stderr or '').strip()[-200:]}")
    return f"/usr/lib/{_ARCH.get(arch, arch)}-linux-gnu"


def preload(image):
    d = lib_dir(image)
    return f"{d}/libtzcompat-stat.so.1 {d}/libtzcompat.so.1"


def virtual_anchor(gate, real_now=None):
    """gate = manifest clock_gate {tz, hour (local hour, fractional), weekday (0 = Monday)}. Returns a UTC datetime or None."""
    if not gate or "weekday" not in gate:
        return None
    tz = _zi.ZoneInfo(gate["tz"])
    real_now = real_now or _dt.datetime.now(_dt.timezone.utc)
    today = real_now.astimezone(tz).date()
    k = (gate["weekday"] - today.weekday()) % 7
    if k > 3:
        k -= 7
    d = today + _dt.timedelta(days=k)
    local = (_dt.datetime.combine(d, _dt.time(0)) + _dt.timedelta(minutes=int(round(gate["hour"] * 60)))).replace(tzinfo=tz)
    return local.astimezone(_dt.timezone.utc).replace(microsecond=0)


def container_env(v, image, real_now=None):
    """Environment for the containers' clock shift. real_now is the real time just before the containers start."""
    real_now = real_now or _dt.datetime.now(_dt.timezone.utc)
    off = int(round((v - real_now).total_seconds()))
    return {"LD_PRELOAD": preload(image),
            "FAKETIME": f"{off:+d}", "FAKE_UTIME": "1", "FAKETIME_DONT_FAKE_MONOTONIC": "1",
            "OPSKIT_ANCHOR": v.strftime("%Y-%m-%dT%H:%M:%SZ")}


def docker_e(env):
    return sum((["-e", f"{k}={v}"] for k, v in env.items()), [])
