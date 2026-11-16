# GPU training cluster

This document covers the GPU training cluster that the ML platform team runs for training and evaluating earth observation models. The cluster is shared by the ML teams in Rotterdam and Denver, and is also used by the applied ML group for smaller experiments.

## Partitions

The cluster has three partitions: `train`, `short`, and `eval`. All three run on the same {{HPC_SCHEDULER}} controller, but they have different node types and time limits.

- **train** — the main partition for training runs. Nodes are a mix of {{GPU_MODEL_1}} and {{GPU_MODEL_2}} GPUs. Jobs here can run up to seven days. Most pretraining and fine-tuning work lands here.
- **short** — a smaller set of nodes (mostly A100s, some V100s still around for legacy workloads) with a four-hour time limit. This is for quick experiments, debugging a dataloader, or testing a code change before committing to a long run. The idle time on these nodes is usually low.
- **eval** — reserved for evaluation jobs. These are typically short (under an hour) but can be run at higher priority than train jobs. The nodes are A100s. If you need to run a large evaluation suite that takes longer, put it in `train` with a comment in the job name.

The scheduler priority is configured so that `eval` jobs preempt `train` jobs when the cluster is under pressure. This is intentional — we do not want evaluation to wait behind a long training run when a model is up for rollout. If you see your training job preempted by an evaluation, that is expected behaviour.

## Reservations

Large pretraining runs can reserve a set of nodes for the full duration of the run. Reservations are handled by the ML platform team — reach out in #ml-platform with the proposed start time, duration, and number of GPUs. We usually ask for at least a few working days of notice so we can check the schedule and avoid colliding with another team's reservation.

When a reservation is in place, the nodes are held exclusively for that run. No other jobs will be scheduled on them. The reservation shows up in {{HPC_SCHEDULER}} with the `reservation` flag, so you can see it with `scontrol show reservation`.

Reservations are not for routine fine-tuning. If you think you need one, talk to the ML platform team first — there may be a way to fit your run into the normal queue without holding nodes idle.

## Scratch filesets

The cluster mounts {{PARALLEL_FS}} scratch at `/scratch`. Each project gets a fileset with a quota. The quota is set when the project is created and can be adjusted by the ML platform team on request. We do not automatically grow filesets — if you run out of space, check what is in your directory before asking for more.

The convention is:

- `/scratch/<project>/` — working space for the project. Code, datasets, intermediate checkpoints.
- `/scratch/<project>/runs/` — training run directories, created by the training harness. Each run gets its own subdirectory with a name that matches the run ID from runsctl.

Anything in `/scratch` is not backed up. If a node fails, the fileset is still there ({{PARALLEL_FS}} is shared across the cluster), but if the fileset itself has issues, we do not have a recovery path. Treat scratch as temporary.

Checkpoints are written to the run directory on scratch during training. When a run finishes, the final checkpoint is copied to the modelhub (see below). The run directory on scratch stays after the run ends so you can go back and inspect logs or intermediate checkpoints, but scratch is not a permanent store — the modelhub is.

## Modelhub

The modelhub is the central place for storing and versioning model checkpoints. It lives outside the cluster, so checkpoints there survive cluster maintenance and are accessible from the serving infrastructure.

When a training run finishes, the harness copies the final checkpoint to the modelhub automatically. The copy is done from the node that ran the job, so if you are writing a custom training loop, make sure the checkpoint is written in a format the harness can pick up. The modelhub has a simple registry with metadata — run ID, model architecture, dataset used, and the metrics from the last evaluation. That metadata is what serving reads when a checkpoint is rolled out.

If you need to manually push a checkpoint (for example, a model trained outside the cluster), use the `modelhub push` command with the run ID and a note in the metadata. Do not push checkpoints that were not produced by a logged run — it makes it impossible to trace which data went into the model.

## Monitoring

The cluster has a {{DASHBOARD_TOOL}} dashboard, linked from the #ml-platform channel description. There is one dashboard per partition, plus a cluster-wide view. The dashboards show GPU utilisation, memory usage, job queue depth, and node health. We also track how long jobs wait in the queue before starting — if that number creeps up, it usually means the partition is saturated and we should look at reservations or priorities.

There is also a per-fileset view of scratch usage, so you can see if a project is close to its quota before a job fails.

## Alerts

Alerts from the cluster go to the `gpu-alerts` feed in chat. The main ones are:

- Node down or unreachable — the node is marked as `down` in {{HPC_SCHEDULER}} and needs intervention.
- GPU errors (XID errors) on a node — the node is drained and the ML platform team checks whether it needs a reboot or replacement.
- Fileset usage above 90% of the hard quota — this is a warning (the soft quota is 85%); the hard limit is enforced by {{PARALLEL_FS}} and jobs will start failing if the fileset fills up.
- Job failures at a high rate — if multiple jobs from the same project fail within a short window, we get a page and investigate before assuming it is a code issue.

If you see an alert that looks like it is about your job, check the dashboard first. Most of the time it is a node issue and your job will be rescheduled by {{HPC_SCHEDULER}} automatically. If your job keeps failing and there is no alert, reach out in #ml-platform — it may be a problem with the job itself.

## Getting help

The ML platform team owns the cluster. For questions about partitions, quotas, or reservations, use #ml-platform. For issues with a specific job, include the job ID and the run ID. The team is distributed across Rotterdam and Denver, so responses may come from either office depending on the time of day.
