# ADR 0009: One shared batch cluster

**Status:** Accepted  
**Owner:** Batch compute  
**Last edited by:** Aiko Bergstrom (Batch Compute Lead)

## Context

We have been running three small batch clusters: one for pricing runs, one for search index refreshes, and one for imagery reprocessing jobs. Each cluster was sized for its team's peak demand and sits idle most of the time. The pricing cluster, for example, runs heavy jobs for a few hours each quarter and is otherwise empty. Search refreshes are steady but low-volume. Imagery reprocessing is bursty and unpredictable.

This arrangement triples the operational overhead: three sets of node images to patch, three autoscaler configs to tune, three places to look when a job fails to start. It also makes it harder to use spare capacity — a reprocessing job cannot borrow pricing nodes without manual juggling.

## Decision

We will consolidate to one shared batch pool managed by the Batch compute team. All batch workloads — pricing, search, imagery reprocessing, and anything new — run on the same pool from the same job specs, and `batchctl` stays the way to see the pool and the jobs on it. The three separate clusters will be decommissioned once their workloads have migrated.

Each team keeps its own memory limit and its own resource request shape. The pool autoscaler handles the rest. We will use cost tags per workload so the showback in the monthly cost report reflects actual usage by team.

## Consequences

- At peak times, jobs may wait in queue longer than they would have on a dedicated cluster. We will monitor queue wait times per workload and tune priorities if needed.
- One set of node images to patch and one autoscaler to maintain. Security patching should become simpler, not harder.
- Per-team usage is visible in the monthly cost report. Teams that run unusually heavy jobs should expect a conversation about sizing.
- The Batch compute team owns the pool configuration. Workload owners still size their own jobs.

## Open questions

- Whether to reserve a small fraction of nodes for interruptible or priority workloads — to be decided after we see queue behaviour for a few weeks.
- Whether imagery reprocessing should keep a separate queue priority during large ingest campaigns. The imagery ops team will flag if they see contention.
- Node image lifecycle: we are standardising on one image but need to confirm the rollout cadence for node upgrades.

## Migration notes

- Workload owners should test their job submissions against the shared pool before their old cluster is retired.
- The decommissioning order is: search first, then pricing, then imagery reprocessing. Dates will be posted in #batch-cluster.
- Any job that cannot run on the shared pool should be raised with Batch compute before the old cluster is turned down.
