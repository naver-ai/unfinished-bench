# Submitting jobs to the batch cluster

The batch cluster is the shared pool for all compute that doesn't need a GPU. If you need GPU time, see `ml-docs/cluster/getting-gpu-time.md` instead. This page covers how to submit a job, pick sensible memory, read logs, and what to do when a submission fails.

## Job spec basics

A job spec is a YAML file. The minimal spec needs a `name`, a `command`, and an `image`. Most jobs also set `memory` and `queue`. The scheduler picks up specs from the `jobs/` folder on your project repo's main branch: a spec with a `schedule` is queued at those times, and one without is queued once each time it is merged or changed.

The fields you'll actually use:

- `name` — must be unique per project. Use `project-shortname-description`, e.g. `imagery-ingest-reproject-nl`.
- `command` — the shell command to run. Keep it a single line; if you need more, write a script into your image and call that.
- `image` — the registry path and tag. Always pin a tag; never use `latest`.
- `memory` — see below.
- `queue` — `normal` (default), `high`, `low`. Most jobs belong in `normal`. Use `high` only for things that block a customer-facing pipeline and can't be rescheduled. `low` is for experiments and anything where a few hours of delay is fine.
- `schedule` — when to queue the job, in cron syntax. Leave it out for by-hand jobs.
- `retries` — how many times the scheduler restarts the job if it exits non-zero. Default 0. Set this only for idempotent commands.
- `timeout` — the max runtime in seconds. The scheduler kills jobs that exceed this. Set it; it's the main protection against a stuck job holding its memory.
- `env` — a map of environment variables. Don't put secrets here; use the secrets mechanism from `platform-docs/security/secrets.md`.

## Choosing the memory reservation

The memory field is the amount of RAM the scheduler reserves for your job. It is not a limit — the job can use more, but if it does, the kernel OOM killer may terminate it. The reservation also determines which nodes your job can land on.

A job that requests 8 GiB will often sit alongside other small jobs on the same node. A job that requests 256 GiB will land on one of the big-memory nodes, and will wait until one is free. For long-running ingest jobs, check what the previous run actually used before bumping the reservation. The peak of earlier runs is on the "Batch cluster" dashboard in BI.

If you're unsure, start with 4 GiB for a typical Python processing job and adjust from the observed peak. Don't request 64 GiB "just in case" — that's how the big-memory nodes stay idle while small jobs queue.

## Queues and priority

The scheduler looks at `high` first, then `normal`, then `low` (how memory is handed out is in `batch-pool.md`). `high` is for customer-impacting work only. If you submit to `high` and the job is not obviously urgent, someone from Batch compute will move it back to `normal` and ping you in #batch-cluster. The `low` queue runs only when there is spare capacity; jobs can be preempted, so make sure anything you run there can be restarted cleanly.

## Logs

Standard output and error from your job go to the batch log store, under `batch-logs/<team>/<job-id>/`. `batchctl show <job-id>` gives the exact path.

Logs are retained for 30 days. If you need longer, copy them into the warehouse or an object store as part of your job. Don't rely on the log store as an archive.

For jobs that produce a lot of output, write to a file in your project's object storage prefix and tail that instead of flooding the log store.

## Checking your jobs

`batchctl jobs` lists running and recently finished jobs with their team, queue, memory and state. `--mine` narrows it to your team's jobs, `--team <team>` to another team's, and `--state RUNNING` to the ones still running. Queued jobs, and each team's usage next to its limit, are in `batchctl pool`.

`batchctl show <job-id>` gives the team and owner, queue, state, memory reservation, progress and where the logs are. Use this first when something looks wrong.

## Checkpointing long jobs

If a job runs for more than a few hours, it should be able to resume from where it left off. The scheduler can retry a job on failure, but only if the job itself is written to be resumable. The pattern:

1. Write state (processed files, offsets, partial results) to object storage as you go.
2. On startup, look for existing state and continue from there.
3. Set `retries` to 1 or 2 so a transient node failure doesn't lose the work done so far.

An ingest job that processes a folder of imagery should track which scenes are already done. A training job should save checkpoints regularly — see `ml-docs/cluster/getting-gpu-time.md` for checkpointing guidance on the GPU side.

Without checkpointing, a 6-hour job that dies at hour 5 restarts from zero. With it, the restart is minutes.

## Common submission errors

- **`name already exists`** — either pick a new name or change the existing spec instead of adding a second one.
- **`image not found`** — the registry path is wrong, or the tag doesn't exist. Check the spelling; registry paths are case-sensitive.
- **`memory must be a multiple of 256Mi`** — round your reservation up to the nearest 256 MiB.
- **`timeout must be at least 60`** — the minimum timeout is 60 seconds. If your job legitimately finishes faster, it probably shouldn't be on the batch cluster.
- **`invalid image: tag latest`** — the scheduler refuses `latest`. Pin a specific tag.

## If it goes wrong

If a job fails and its logs don't make the reason clear, look at the "Batch cluster" dashboard in BI — a node that's been drained or is showing high error rates will fail jobs in a way that looks random.

If the scheduler itself seems broken — jobs stuck in `queued` for hours, submissions timing out — ping #batch-cluster. The on-call person for Batch compute will pick it up. Don't resubmit a large job multiple times while it's stuck; that just makes the queue harder to read.

Questions about queues, node types or the pool itself go to #batch-cluster.
