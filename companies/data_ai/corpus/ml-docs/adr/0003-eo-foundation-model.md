# ADR 0003: Pretrain our own EO foundation model

**Status:** Accepted  
**Owner:** Earth observation models  
**Last edited by:** Laszlo Fonseca  

## Context

Most of our models are task-specific and trained from scratch per customer or per geography. Each new flood detection or crop condition model requires label effort from the labelling team, a dedicated training run, and careful tuning. With 310 staff and a growing imagery archive, this does not scale.

We hold a large archive of satellite imagery covering our operating regions, plus our own ground sensor network. The imagery is already stored as COGs with a STAC catalogue (see `platform-docs/adr/0004-imagery-as-cogs.md`). We also have a good sense of the tasks our customers ask for: water extent, crop stage, soil moisture proxies, and change over time.

## Decision

Pretrain a single earth observation foundation model on the full imagery archive, using self-supervised objectives that work well for remote sensing data. Fine-tune this model for each customer task instead of training from scratch.

- Pretraining data: all suitable imagery from the archive, masked where clouds or shadows are detected.
- Model family: vision transformer with a patch size that matches our typical sensor resolution.
- Fine-tuning: per-task heads on top of the shared trunk; label effort should drop substantially for new tasks.
- Evaluation: keep the existing offline evaluation sets for each task; add a held-out pretraining set to check representation quality.

## Compute estimate

The full pretraining run is large for our current cluster. Rough numbers:

- About 14 days on a multi-node job using most of the {{GPU_MODEL_1}}-class capacity we have.
- Memory per node is the constraint; we will use gradient checkpointing.
- We will use the cluster scheduler's pre-emption support so the job yields when shorter work needs capacity.

The ML platform team is aware and the GPU cluster has enough headroom for this to be acceptable. We will revisit sizing when we have a clearer view of the data mix.

## Consequences

- The GPU cluster will see long-running pretraining jobs; interactive work should be scheduled around them where possible.
- The eval sets become the gate for whether the foundation model is good enough to replace task-specific training. Elias Asante owns those eval sets and will need to extend them for pretraining quality checks.
- The labelling queue shifts: less effort per task, but we need a small set of labelled scenes for each customer geography to make fine-tuning work.
- The modelhub will need a section for the pretrained checkpoint and its fine-tuned derivatives.

## Loose ends

- Exact masking strategy for cloudy scenes still needs a decision; Sebastian Lee and Diego Tanaka are looking at options.
- We should check with Hugo Brandsma about how this interacts with the serving rollout process once we have a checkpoint worth serving.
- The pretraining run will need a temporary scratch quota raise on its project fileset.

## References

- `ml-docs/eval/offline-evaluation.md` for the eval set structure.
- `ml-docs/modelhub.md` for where the checkpoint will live.
- `ml-docs/cluster/getting-gpu-time.md` for how the pretraining job will be scheduled.
