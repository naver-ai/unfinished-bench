# ml-docs

Index for ML platform, modelling and serving documentation. Owner: ML platform (training cluster and serving). Last edited by Ben Hughes.

## Platform

- [cluster/overview.md](cluster/overview.md) — GPU training cluster layout and scheduling.
- [cluster/getting-gpu-time.md](cluster/getting-gpu-time.md) — How to request GPU allocation.
- [cluster/scratch-quota.md](cluster/scratch-quota.md) — Scratch filesets and quotas.
- [modelhub.md](modelhub.md) — The modelhub; source of truth for checkpoints and metrics.

## Training and evaluation

- [training/labelling.md](training/labelling.md) — Labelling workflow and tooling.
- [eval/offline-evaluation.md](eval/offline-evaluation.md) — Offline evaluation approach and cut-offs.

## Serving

- [serving/serving-overview.md](serving/serving-overview.md) — Serving architecture and endpoints.
- [serving/rollout.md](serving/rollout.md) — Rolling out model checkpoints.

## ADRs

- [adr/0003-eo-foundation-model.md](adr/0003-eo-foundation-model.md) — Decision record for pretraining our own EO foundation model.

For CPU-only preprocessing on the shared batch cluster, see platform-docs/batch/submitting-jobs.md. For cost sizing of training runs, see finance-docs/finops/unit-costs.md.

The old gpu-request form was retired — see getting-gpu-time.md for how allocation works now.
