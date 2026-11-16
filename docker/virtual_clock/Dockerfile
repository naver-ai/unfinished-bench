# Unfinished-Bench
# Copyright (c) 2026-present NAVER Corp.
# Apache-2.0
# Virtual-clock image: the agent image + libfaketime (0.9.13, pinned commit) + vclock_stat.c, sudo and ripgrep.
# Build (after unfinished-bench/agent:base):
#   docker build -t unfinished-bench/agent:vclock -f docker/virtual_clock/Dockerfile docker/virtual_clock
# The two libraries are installed next to the C library under names that do not stand out:
#   libtzcompat.so.1 (libfaketime) and libtzcompat-stat.so.1 (vclock_stat.c: file-time calls libfaketime does not cover,
#   the virtual sleep, and the sleep signal on /run/tzcompat.sock that the agent driver listens to).
# The clock settings come from environment variables or, if absent, from /etc/tzcompat.conf (vc_conf.h replaces
# libfaketime's getenv at build time). No shared memory is used (FAKE_STATELESS).
# The agent container uses /etc/ld.so.preload and /etc/tzcompat.conf; the server container uses environment variables
# (harness/virtual_clock.py).
FROM unfinished-bench/agent:base AS b
RUN apt-get update && apt-get install -y --no-install-recommends build-essential git ca-certificates >/dev/null && \
    git clone -q https://github.com/wolfcw/libfaketime /src && cd /src && git checkout -q e8d8c85
COPY vc_conf.h vc_ft_getenv.h vclock_stat.c /src/
RUN make -C /src/src libfaketime.so.1 FAKETIME_COMPILE_CFLAGS="-DFAKE_STATELESS -I/src -include /src/vc_ft_getenv.h" >/dev/null
RUN gcc -shared -fPIC -O2 -Wall -Werror -I/src -o /src/vclock_stat.so /src/vclock_stat.c -ldl
RUN d=/out/$(uname -m)-linux-gnu && mkdir -p "$d" && cp /src/src/libfaketime.so.1 "$d"/libtzcompat.so.1 && cp /src/vclock_stat.so "$d"/libtzcompat-stat.so.1
FROM unfinished-bench/agent:base
# sudo, as on a normal server. Tools check permissions from the identity file, so sudo grants nothing extra.
# The install leaves no apt/dpkg log entries and file times match the rest of the image.
RUN mkdir -p /tmp/.l && cp -a /var/log/apt /var/log/dpkg.log /tmp/.l/ 2>/dev/null; \
    apt-get update -qq && apt-get install -y -qq --no-install-recommends sudo >/dev/null && \
    dpkg -L sudo | while read f; do [ -f "$f" ] && touch -h -r /usr/bin/bash "$f"; done; \
    touch -r /usr/bin/bash /etc/sudoers /etc/sudoers.d /etc/pam.d/sudo 2>/dev/null; \
    rm -rf /var/log/apt /var/lib/apt/lists/* && cp -a /tmp/.l/apt /var/log/apt && cp -a /tmp/.l/dpkg.log /var/log/dpkg.log 2>/dev/null; rm -rf /tmp/.l
# ripgrep: Hermes' file search tool uses rg; its grep fallback misses content searches from '.' and does not take
# extended patterns. Same install hygiene as above.
RUN mkdir -p /tmp/.l && cp -a /var/log/apt /var/log/dpkg.log /tmp/.l/ 2>/dev/null; \
    apt-get update -qq && apt-get install -y -qq --no-install-recommends ripgrep >/dev/null && \
    dpkg -L ripgrep | while read f; do [ -f "$f" ] && touch -h -r /usr/bin/bash "$f"; done; \
    rm -rf /var/log/apt /var/lib/apt/lists/* && cp -a /tmp/.l/apt /var/log/apt && cp -a /tmp/.l/dpkg.log /var/log/dpkg.log 2>/dev/null; rm -rf /tmp/.l
COPY --from=b /out/ /usr/lib/
RUN d=/usr/lib/$(uname -m)-linux-gnu && touch -r "$d"/libc.so.6 "$d"/libtzcompat.so.1 "$d"/libtzcompat-stat.so.1 && touch -r /usr/bin/bash "$d"
