#!/bin/bash
# Unfinished-Bench
# Copyright (c) 2026-present NAVER Corp.
# Apache-2.0
# Run the full benchmark round by round. Round r = tasklists/round_r.txt (positions doc and user, variant r of every
# scenario) under CONDITIONS, then tasklists/round_r_no-rule.txt if it exists (position no-rule, no_persistence only: the no-rule
# position compares the presence of the rule without persistence). Each list finishes (first pass + REDO_PASSES passes that
# re-run infrastructure failures) before the next one starts, so a run stopped between lists leaves every model and
# condition with the same task set.
#
#   MODELS=gpt-oss-20b,glm-5.3 RUNS_ROOT=$PWD/runs bash harness/run_rounds.sh
#
# Optional: ROUNDS="01 02" (default all 10), CONDITIONS (default no_persistence,persistence), JOBS (default 16),
#           MODEL_JOBS, REDO_PASSES (default 2), ENV_FILE (default .env).
# Start it detached (e.g. setsid/nohup). To stop: touch "$RUNS_ROOT/_STOP_NEW" (running cells finish).
cd "$(dirname "$0")/.." || exit 1
set -a; source "${ENV_FILE:-.env}" 2>/dev/null; set +a
: "${RUNS_ROOT:?set RUNS_ROOT}"; : "${MODELS:?set MODELS (keys from models.json)}"
export RUNS_ROOT
CONDITIONS="${CONDITIONS:-no_persistence,persistence}"; JOBS="${JOBS:-16}"; ROUNDS="${ROUNDS:-01 02 03 04 05 06 07 08 09 10}"
mkdir -p "$RUNS_ROOT"
log(){ echo "[$(date '+%m-%d %H:%M:%S')] $*" | tee -a "$RUNS_ROOT/_rounds.log"; }
stop_check(){ [ -f "$RUNS_ROOT/_STOP_NEW" ] && { log "stop file found; exiting"; exit 0; }; return 0; }
batch(){ python3 harness/run_batch.py --tasks-file "$1" --conditions "$2" --models "$MODELS" --reps 1 --jobs "$JOBS" \
           >> "$RUNS_ROOT/_batch.log" 2>&1 < /dev/null; }
step(){   # step <task list> <conditions> <label>
  log "$3 start ($(grep -vc '^#' "$1") tasks, $2)"
  stop_check; batch "$1" "$2"; log "$3 pass 1 rc=$?"
  for p in $(seq 1 "${REDO_PASSES:-2}"); do
    stop_check; batch "$1" "$2"; log "$3 re-run pass $p rc=$?"
  done
}
log "start code=$(git rev-parse --short HEAD 2>/dev/null) MODELS=$MODELS CONDITIONS=$CONDITIONS JOBS=$JOBS ROUNDS='$ROUNDS'"
for r in $ROUNDS; do
  TF="tasklists/round_$r.txt"; [ -f "$TF" ] || { log "missing $TF"; exit 1; }
  step "$TF" "$CONDITIONS" "round $r"
  [ -f "tasklists/round_${r}_no-rule.txt" ] && step "tasklists/round_${r}_no-rule.txt" no_persistence "round $r no-rule"
done
log "all rounds done"
