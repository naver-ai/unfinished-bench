# Unfinished-Bench
# Copyright (c) 2026-present NAVER Corp.
# Apache-2.0
# Agent image: the OpenAgentSafety base task image with hermes-agent 0.19.0 in its own venv.
# The system Python stays untouched for the task evaluators; Hermes lives in /opt/hermes-venv.
# Build: docker build -t unfinished-bench/agent:base -f docker/agent.Dockerfile docker
FROM ghcr.io/sani903/openagentsafety_base_image-image:1.0

RUN python3 -m venv /opt/hermes-venv \
 && /opt/hermes-venv/bin/pip install --no-cache-dir --upgrade pip \
 && /opt/hermes-venv/bin/pip install --no-cache-dir "hermes-agent==0.19.0"

# sanity: import AIAgent at build time so a broken install fails the build
RUN /opt/hermes-venv/bin/python -c "import sys; sys.path.insert(0,[p for p in sys.path if 'site-packages' in p][0]); from run_agent import AIAgent; print('AIAgent import OK')" || \
    /opt/hermes-venv/bin/python -c "from run_agent import AIAgent; print('AIAgent import OK (direct)')"
