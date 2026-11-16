# Offline evaluation

**Owner:** Earth observation models  
**Last edited by:** Magnus Pereira (Research Engineer)

## Purpose

This document describes how we maintain frozen evaluation sets for the three core tasks, how we report metrics, and how eval reports are stored alongside checkpoints in the modelhub. It is the reference for anyone preparing an eval run or interpreting an eval report.

## Evaluation sets

We keep three frozen eval sets, one per task:

- **Flood extent** – built from labelled flood events across the Netherlands, the US Gulf Coast, and the Mekong delta. Slices: region, water body type (river, coastal, pluvial), and season. Sensor slices cover {{EO_SATELLITE_1}}, {{EO_SATELLITE_2}}, and our own ground sensor returns where they overlap.
- **Field boundaries** – labelled parcels from agricultural co-ops in the Netherlands, northern Germany, and the US Midwest. Slices: region, crop group, and field size band. Sensor slices: optical only ({{EO_SATELLITE_2}} and, where available, high-resolution tasking imagery).
- **Change detection** – pairs of images with labelled change from the imagery archive, covering construction, vegetation change, and water course shifts. Slices: region, change type, and time gap between acquisitions (short, medium, long).

The eval sets are frozen: we do not add or remove samples without a decision recorded in the `#eo-models` channel and a note in the eval set's metadata file. Elias Asante approves any change to the frozen sets.

## Running an evaluation

Eval runs go to the `eval` partition on the GPU training cluster, using the standard eval job template. Each run produces a report in the modelhub under `modelhub://evals/<checkpoint-id>/`. The report includes:

- Metrics per task and per slice.
- A comparison against the previous checkpoint for the same task, where one exists.
- A short log of any known data issues noticed during the run (for example, a region slice with fewer samples than expected because of cloud cover in the source imagery).
- The exact commit of the eval set used, so results are reproducible.

We report the standard metrics per task:

- **Flood extent:** IoU, F1, and precision/recall at the operational threshold.
- **Field boundaries:** IoU on boundaries, F1 on parcels, and a simple count of over- and under-segmented fields per region slice.
- **Change detection:** F1, precision/recall, and time-to-detection for the water course shift slice.

We do not report a single aggregated score across tasks. Each task is evaluated independently, and the modelhub shows the per-task metrics side by side.

## What we compare against

Every eval report includes a comparison against the current production checkpoint for that task. The report shows, per task, where the proposed checkpoint improves and where it regresses against the tolerance in the eval set's metadata. Regressions in specific slices are called out in the report.

## Generating a report

The eval job writes the report itself. To generate one:

1. Start the eval job from the checkpoint's page in the modelhub. The job picks up the correct eval set based on the task the checkpoint is registered for.
2. Wait for the job to finish on the eval partition. Most eval jobs finish in under an hour; flood extent on the full set is the slowest.
3. The report is written back to the modelhub automatically. Check the "eval" tab on the checkpoint page.
4. If the report shows a slice with zero samples, rerun with the `--allow-empty-slices` flag and note the empty slice in the report. Do not silently skip a slice.

## Loose ends

- The change detection eval set still has a small number of pairs from an older river flooding event in the Netherlands that we have not fully re-labelled. Georgia Demir is reviewing those labels; until that is done, the time-to-detection slice for that event should be read with some care.
- We do not yet have a frozen eval set for crop type classification. Daisuke Yamamoto is scoping one; until it exists, crop type metrics are reported from ad hoc runs and are not comparable across checkpoints.
- The field boundaries eval set will be extended with more US Midwest parcels in the next labelling round. The frozen set stays as is until that round is complete and we decide to release a new frozen version.

## Related documents

- `ml-docs/modelhub.md` – how checkpoints and eval reports are stored.
- `ml-docs/serving/rollout.md` – release review criteria and rollout steps.
- `ml-docs/training/labelling.md` – how labels for the eval sets are produced.
- `ml-docs/cluster/overview.md` – partitions on the GPU training cluster.
