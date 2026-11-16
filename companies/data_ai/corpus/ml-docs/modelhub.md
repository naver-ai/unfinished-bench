# The modelhub

The modelhub is the central registry for trained model checkpoints, their metadata, and their promotion path to serving. If you trained a model and want it served, it goes through the modelhub. The ML platform team owns the modelhub; contact us in #ml-platform with questions.

## Registering a checkpoint

1. After a training run finishes, create the modelhub entry from the run ID:
   ```
   modelhub register --run-id <run-id>
   ```
   The modelhub pulls the run's configuration, metrics, and the checkpoint path from the run directory automatically.

2. Give the model a name. The naming convention is `<model>-v<n>-<MMDD>` where `<n>` is the model's version (incrementing per architecture family) and `<MMDD>` is the month/day the checkpoint was produced. For example, `floodseg-v3-0214`. Do not reuse a name; if you need to re-register, bump the version.

3. Fill in the model card. The modelhub pre-fills what it can from the run, but you must add:
   - Intended use and target geography (which basins, coastlines, or crop regions)
   - Known limitations (sensor drift, time-of-day bias, areas without ground truth)
   - Training data summary: which imagery collection and which label set version
   - Evaluation results summary, pointing to the offline evaluation report if one was run

4. Save the entry. The modelhub assigns a canonical ID (e.g. `mh-40117`) and records you as the owner.

## Lineage

Every modelhub entry keeps lineage back to:

- The training run (its run ID and run directory, including the config and the seed)
- The label set version used for training and for evaluation (see `ml-docs/training/labelling.md`)
- The imagery collections that went into the training data, referenced from the imagery catalogue
- Any parent checkpoints (for fine-tunes or continued pretraining)

If the lineage cannot be resolved, the modelhub will refuse to register the checkpoint. Do not try to work around this; it means the run or label set was not recorded properly and needs to be fixed first.

## Promoting to a serving candidate

To put a checkpoint forward for serving:

1. On the model entry, click "Promote to serving candidate". This creates a serving candidate and triggers the serving evaluation suite.
2. The serving evaluation suite runs the checkpoint through the offline evaluation harness and a smoke inference pass on the serving stack. Results are attached to the candidate.
3. Add a short note in the candidate's summary explaining what changed since the last served version (data, architecture, or training setup).
4. Notify #model-governance that a candidate is waiting. The model governance group reviews the candidate and, if accepted, it becomes the next candidate for rollout per `ml-docs/serving/rollout.md`.

The modelhub shows the current rollout status of each candidate so you can see where it is in the queue.

## If it goes wrong

- If registration fails on lineage, check that the run ID is correct and that the label set version still exists. Re-run with the corrected values.
- If the model card is rejected for missing fields, the modelhub tells you exactly which fields are missing. Fill them in; do not mark fields "n/a" unless they truly do not apply.
- If promotion fails at the evaluation step, the serving evaluation logs are attached to the candidate. Common causes are input shape mismatches or the checkpoint path being inaccessible from the serving host. Fix those and re-run promotion.
- If you suspect the modelhub itself is broken, check the status page, then #ml-platform.
