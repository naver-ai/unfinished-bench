# Labelling

**Owner:** Change detection models  
**Last edited by:** Ida Novak  

Status: draft — two sections still tbc, one open question at the end.

## Label sets

Label sets live in the labelling workspace in the `brakwater-label-sets` bucket (path follows `labels/<label-set-id>/`). Each label set has:

- a manifest (`manifest.json`) with label set id, version, creation date, owner team, and the tasking order or internal project it belongs to
- the label files themselves (GeoJSON per AOI, one file per scene)
- a QA log (`qa_log.jsonl`) appended by the QA sampler

Create a new label set with:

```
labelctl create --name <label-set-id> --owner change-detection
```

The label set id is the short name used in training configs (e.g. `flood-extent-nl-q3`). Keep it lowercase with hyphens.

## Annotation vendor

We use the same vendor for all change detection label work. The vendor has access to the labelling workspace only; they do not get access to the imagery catalogue or the warehouse. Their access is scoped to the label set bucket path.

Vendor deliveries come as a single archive per batch. Unpack and validate before merging:

```
unzip <batch>.zip -d <label-set-id>/incoming/
labelctl validate <label-set-id>/incoming/
```

Validation checks schema, geometry validity, class names against the guideline, and file naming. Do not merge a batch that fails validation; send it back via the vendor portal.

## Labelling guidelines

The guidelines are maintained in the change detection team's shared drive. (tbc: link to the current version and note which label-set versions used which guideline revision.) The guidelines cover:

- class definitions (water, flood, no-data, etc.)
- minimum mapping unit and edge handling
- how to treat cloud shadow and haze
- how to treat bridges, dikes, and other structures that cross water

If you need a new class or a rule change, update the guidelines and bump the revision number. (tbc: the exact procedure for proposing a guideline change.)

## QA sampling

QA is done per batch, not per label set. Sample 10% of scenes per batch, stratified by AOI and by labeler (the vendor provides labeler ids in their delivery manifest).

Run the sampler:

```
labelctl qa-sample <label-set-id>/incoming/ --rate 0.1 --seed <batch-id>
```

This writes the QA sample list to `qa/<batch-id>/sample.jsonl`. Two people from the change detection team review each QA scene independently, then compare. Disagreements go to the label set owner (Eero Eklund or Georgia Demir) for a final call.

If QA agreement is below 90%, the whole batch goes back to the vendor with the QA notes. We track agreement per batch in the change detection team's spreadsheet; moving this into the labelling workspace so the numbers are queryable is still tbc.

## Ground sensor readings as ground truth

For flood label sets covering areas with ground sensors, we can use sensor readings as weak ground truth. This is only for pre-filtering candidate scenes, not for final labels — the final labels always come from the vendor.

Sensor readings are pulled from the sensor network's archive via `sensorctl export --area <aoi> --window <date-range>`. The export gives water level readings per sensor. Use them to:

- confirm a flood event actually happened in the AOI before tasking new imagery
- flag scenes where the sensor says no flooding but the label says flood (these go to QA review)

Do not use sensor readings to generate labels automatically. The change detection models need manual labels; auto-generating from sensors has been tried and does not transfer.

## Versioning label sets

Label sets are versioned. The version is part of the manifest and is used in training configs. When a label set changes (merged batch, corrected labels from QA), bump the minor version. Major version bumps are for guideline revisions that change class semantics.

Training runs reference label sets by `label-set-id@version`. Do not overwrite a label set in place; always create a new version. The old version stays readable for reproducibility.

Open question: should we keep label sets from finished projects indefinitely, or archive them after a retention period? The labelling workspace has its own quota, but it is not unlimited. Comments welcome in #eo-models.

## If it goes wrong

- Vendor delivers a partial batch: check the delivery manifest against the order; send back the missing list via the vendor portal.
- Validation fails: the validator prints the offending file and reason. Fix the file if it is an internal naming issue; otherwise return the batch.
- QA agreement below threshold: return the batch, include the QA notes, and mark the batch as `rejected` in the label set manifest.
- A label set is missing from the workspace: check `labelctl list` and the bucket path; if the bucket path is empty, check the vendor portal for delivery status.
- Sensor export returns no data for an AOI: the sensors may be offline or the archive window is wrong. Check the sensor network status page and retry with a wider window.
