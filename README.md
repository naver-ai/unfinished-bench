# Unfinished-Bench

[![Paper](https://img.shields.io/badge/arXiv-2611.17460-b31b1b.svg)](https://arxiv.org/abs/2611.17460)
[![Project page](https://img.shields.io/badge/project-page-ee7a2a.svg)](https://francis21c.github.io/unfinished-bench/)
[![Docs](https://img.shields.io/badge/docs-website-0E7C7B.svg)](https://francis21c.github.io/unfinished-bench/doc/)
[![Python](https://img.shields.io/badge/python-3.10%2B-3776AB.svg)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/docker-required-2496ED.svg)](https://www.docker.com/)
[![Agent](https://img.shields.io/badge/agent-Hermes%20Agent%200.19.0-555555.svg)](https://github.com/NousResearch/hermes-agent)
[![License](https://img.shields.io/badge/license-Apache%202.0-D22128.svg)](LICENSE)

<p align="center"><img src="assets/overview.png" alt="Overview of Unfinished-Bench" width="900"></p>

A benchmark that gives LLM agents persistence toward task completion in autonomous runs without a user, in realistic
work environments with embedded rules. In each task the goal and a rule cannot both hold; the benchmark measures how
much persistence adds to rule violations.

- **Paper:** [Unfinished-Bench: Measuring Rule Violations by Persistent Agents in Realistic Work Environments](https://arxiv.org/abs/2611.17460)
- **Project page:** [francis21c.github.io/unfinished-bench](https://francis21c.github.io/unfinished-bench/)
- **Documentation:** [francis21c.github.io/unfinished-bench/doc](https://francis21c.github.io/unfinished-bench/doc/) — the design
  (rule positions, conditions, episode mechanics, scoring) and all 97 scenarios by organization, risk category and rule
  position

| | |
|---|---|
| Scenarios | 97 across 7 risk categories and 7 fictional organizations |
| Tasks | 2,134 = 97 × (`doc` and `user`: 10 variants each; `no-rule`: 2 variants) |
| Agent | [Hermes Agent](https://github.com/NousResearch/hermes-agent) 0.19.0 in a Docker work computer; tools and service state run in a separate tool server container |
| Grading | code only, from tool audit logs and final service state |

<p align="center"><img src="assets/example_run.png" alt="One task in two rule positions" width="720"></p>
<p align="center"><sub>One task in two rule positions (Gemma 4 12B, research grant disbursement, with persistence). All text
is quoted from the transcripts. Top: with the rule in the internal document, the agent stops twice and, after the second
re-prompt, pays through the exception path. Bottom: with the same rule stated by the user, the same model keeps the
rule through six re-prompts.</sub></p>

## Setup

You need:

- **Docker** — the agent's work computer and the tool server run in containers.
- **Python 3.10+**
- **An API that serves the models** — the agent being tested in each run and the model that fills the names (below)
  both call it. It must be OpenAI-compatible (chat completions with tool calling): a provider such as OpenAI, or your
  own vLLM server. Two variables in `.env` point to it:
  - `LLM_API_BASE`: the API's address, its base URL up to `/v1` (the code adds `/chat/completions`), for example
    `https://api.openai.com/v1`, or `http://localhost:8000/v1` for a vLLM server
  - `LLM_API_KEY`: the key for that API (any string if the server does not check keys)

  For models on another server, add a provider in `models.json`.

```bash
docker build -t unfinished-bench/agent:base -f docker/agent.Dockerfile docker
docker build -t unfinished-bench/agent:vclock -f docker/virtual_clock/Dockerfile docker/virtual_clock
cp .env.example .env                                   # then set LLM_API_BASE and LLM_API_KEY
set -a; source .env; set +a
```

**Fill in the names.** Apart from the fictional organizations in the scenarios, the released data names outside
organizations, products and shops (a cloud provider, an airline, a tax authority, ...) only by their role, through the
slots in `fill/slots.json`. A model you choose fills them, and you build and run from the filled copy:

```bash
python3 fill/llm_fill.py --out my_values.json          # asks the model in LLM_API_BASE; --model picks the model
python3 fill/fill.py --values my_values.json --out ../unfinished-bench-filled
cd ../unfinished-bench-filled
python3 build/build_all.py --out tasks/main            # about 4 GB; --only c1-refund,c7-release builds a subset
```

The values file can also be written by hand (format in `fill/fill.py`). The build stops if a slot is left unfilled.
Email addresses and phone numbers are fixed fictional values and are not filled. See the [Data notice](#data-notice).

`models.json` maps a model key to a model id and a provider. The ids are the models' Hugging Face names; if your API
names a model differently, change its id. A provider names the environment variables that hold its base URL and key, so
models from different endpoints can run in one batch.

## Running

A task id is `<scenario>-<position>-v<NN>`, for example `c1-refund-doc-v01`:

| Position | Rule | Variants |
|---|---|---|
| `doc` | in an internal document the task points to | 01–10 |
| `user` | stated by the user in the instruction | 01–10 |
| `no-rule` | none; the same action is permitted (control for stopping short without a reason) | 01–02 |

A run uses one of two conditions:

| Condition | What the harness does |
|---|---|
| `no_persistence` | the episode ends when the agent stops |
| `persistence` | the task asks the agent to see it through, and each time the agent stops with the goal unmet the harness re-prompts it (up to 6 times) |

The documentation describes the conditions, the re-prompt text and the episode mechanics in full.

One run:

```bash
python3 harness/run_cell.py --task c1-refund-doc-v01 --condition persistence \
    --agent-model openai/gpt-oss-20b --tag gpt-oss-20b_r1
```

A batch (tasks × conditions × models):

```bash
python3 harness/run_batch.py --tasks-file tasklists/round_01.txt --conditions no_persistence,persistence \
    --models gpt-oss-20b,glm-5.3 --jobs 16
```

The full benchmark runs round by round: round r = the `doc` and `user` tasks of variant r under both conditions, then
the `no-rule` tasks of variant r under `no_persistence` (rounds 01 and 02). Stopped between rounds, every model and
condition has run the same tasks. The paper reports rounds 01 and 02:

```bash
MODELS=gpt-oss-20b,glm-5.3 RUNS_ROOT=$PWD/runs nohup bash harness/run_rounds.sh &
touch runs/_STOP_NEW          # stop starting new runs; runs in progress finish
```

Notes:
- Rate-limited models: cap their concurrency with `MODEL_JOBS="model-key=4"`; more concurrency only lengthens runs.
- An endpoint on the host's loopback interface cannot be reached through the relay; run with `NET_INTERNAL=0`
  (the run network is then not isolated from the internet).
- `REASONING_MODE=off|effort|template` controls the reasoning parameter sent to DeepSeek and Gemma models
  (set per model in `models.json`).
- Time limits nest: container lifetime (`CONTAINER_TTL`, 16200 s) > run process (`BATCH_RUN_TIMEOUT`, 15700 s) >
  driver (`DRIVER_TIMEOUT`, 14400 s of wall-clock time) + grading and copying. Runs that reach the driver limit keep
  their transcript and grade; runs that end for infrastructure reasons are re-run by later passes.

## Results

Each run folder `runs/<task>__<condition>__<model>_r<n>/` holds:

| File | Content |
|---|---|
| `eval_result.json` | `checkpoints[0]`: the protected items were changed (violation); `checkpoints[1]`: manipulation outside the tools |
| `transcript_live.jsonl` | every request and response, including the system prompt and tool definitions |
| `full_transcript.json` | the conversation as the agent held it at the end; if the conversation was compressed during the run, the compressed version (the earlier messages are in `transcript_live.jsonl`) |
| `hermes_summary.json` | how the episode ended |
| `vclock.json` | the scenario clock |

## Layout

```
companies/    staff directory, document corpus and chat history per organization
scenarios/    one module per scenario: task text, tools, data, rule section, evaluator, goal check
tools/        tool engines (server side); each scenario installs them under its own command names
fill/         name slots (slots.json), the model fill (llm_fill.py) and the filled copy (fill.py)
build/        build_all.py and build_tasks.py build task folders; realism_lint.py checks their text during the build
harness/      run_cell.py (one run), run_batch.py (many runs), run_rounds.sh (full benchmark), agent_driver.py,
              server_split.py, virtual_clock.py, container_setup.py, hermes_patches/ (modified Hermes files)
scoring/      evaluator runner and graders
docker/       agent image and virtual-clock image
assets/       figures used in this README
tasklists/    round_01 … round_10 (doc and user, variant r), round_01_no-rule and round_02_no-rule
models.json   model keys, model ids and providers
```

## Built on

- **OpenAgentSafety** — the base task container image and the evaluator conventions of the task folders.
  Vijayvargiya et al., *OpenAgentSafety: A Comprehensive Framework for Evaluating Real-World AI Agent Safety*,
  ICLR 2026. [arXiv:2507.06134](https://arxiv.org/abs/2507.06134) ·
  [github.com/Open-Agent-Safety/OpenAgentSafety](https://github.com/Open-Agent-Safety/OpenAgentSafety)
- **Hermes Agent** 0.19.0 by Nous Research (MIT) — the agent. A few of its files are replaced at run time with
  modified copies; `harness/hermes_patches/README.md` lists the changes.
  [github.com/NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent)
- **libfaketime** (GPL-2.0) — the virtual clock. [github.com/wolfcw/libfaketime](https://github.com/wolfcw/libfaketime)

## Citation

```bibtex
@misc{lee2026unfinishedbench,
  title         = {Unfinished-Bench: Measuring Rule Violations by Persistent Agents in Realistic Work Environments},
  author        = {Lee, Seunghyun and Hwang, Jaehui and Han, Dongyoon and Yun, Sangdoo},
  year          = {2026},
  eprint        = {2611.17460},
  archivePrefix = {arXiv},
  primaryClass  = {cs.LG},
  url           = {https://arxiv.org/abs/2611.17460}
}
```

## Data notice

This repository contains synthetic text generated and revised with large language models, including DeepSeek V4 Flash
(MIT License) and Anthropic Claude (Opus 5.5, Opus 5, Opus 4.8), and reviewed by the authors. The companies, persons,
and events described are fictional; any resemblance to actual entities or persons is coincidental.

Apart from the fictional organizations in the scenarios, names of organizations, public bodies, and products are left
as placeholders and are filled in at build time by an AI model chosen and run by the user. Any filled-in content is
generated in the user's environment, may coincide with real entities, and is the user's responsibility; it does not
describe actual dealings with, or any affiliation with or endorsement by, any real entity. Please do not redistribute
filled-in data.

Email addresses and phone numbers use reserved or fictitious ranges. Do not connect this benchmark to tools that send
real emails, messages, or calls.

Generated text may contain inaccurate statements. This content is provided solely for evaluating AI agents and may not
be used to train, fine-tune, or distill AI models. The README figure quotes an execution log of Gemma 4 12B (Google),
licensed under Apache License 2.0.

## License

Unfinished-Bench is released under the [Apache License 2.0](LICENSE).

```
Unfinished-Bench
Copyright (c) 2026-present NAVER Corp.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

Third-party components and their licenses are listed in [NOTICE](NOTICE): the modified Hermes Agent files in
`harness/hermes_patches/` keep their MIT license.
