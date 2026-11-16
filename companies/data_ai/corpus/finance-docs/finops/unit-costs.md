# Unit cost notes

Owner: FinOps (cloud cost)  
Last edited by: Nadia Okafor

Working notes on unit economics for the main cost drivers we track. These are not the formal cost report (see `finance-docs/finops/cost-reporting.md`) — these are the per-unit figures we use for product pricing sanity checks, capacity planning and customer conversations.

## Imagery processing cost per 100 km²

- **What it covers:** the full pipeline from raw satellite scene to analysis-ready COG in the imagery archive, including ingest, cloud-masking, atmospheric correction and the tile generation step.
- **Current figure:** we use €4.20 per 100 km² as the planning number. This is the blended rate across optical and SAR scenes; SAR is roughly 1.6× optical.
- **How it is calculated:** take the monthly compute + storage egress cost for the imagery ingest pipeline (from the billing export for the `imagery-prod` account), divide by the area processed that month (from the imagery catalogue), and apply a 15% buffer for retries and re-runs. Cost tags on the ingest jobs are the source of truth; see `finance-docs/finops/cost-tags.md`.
- **Known gaps:** the figure does not include the cost of pulling scenes from the archive for reprocessing, and it assumes the batch pool is not contended. When the pool is busy, the wall-clock time goes up but the unit cost stays roughly flat, so this is acceptable for now.
- The breakdown by sensor type is in the BI dashboard under `Imagery ops > Unit costs`.

## Cost per thousand API calls

- **What it covers:** the analytics API, including auth, request validation, tile serving and the underlying warehouse queries.
- **Current figure:** €0.34 per thousand calls. This is dominated by warehouse compute — about 70% of the total. Tile requests are cheaper than vector queries by a factor of about 4, but we deliberately quote a blended rate so pricing stays simple.
- **How it is calculated:** monthly API-related warehouse spend plus the serving layer cost, both from the billing export, divided by the call volume from the customer API console. The warehouse share is estimated from the query service's tagged workload.
- **Known gaps:** we do not separate read-only calls from calls that trigger heavier aggregations. Some customers run very heavy spatial joins and the blended figure understates those. There is a loose end to introduce a cost multiplier per endpoint tier, but it has not been prioritised.

## Storage per TB-month in the imagery archive

- **What it covers:** the COG objects plus the STAC catalogue metadata, but not the raw scenes before they are converted.
- **Current figure:** €7.10 per TB-month. This is the standard rate from the cloud provider; we do not add our own markup because the archive is a cost centre, not a product.
- **How it is calculated:** total archive storage spend for the month divided by the TB-months reported in the imagery catalogue. The catalogue already tracks object size and age, so the calculation is mostly a join between that and the cost report.
- **Known gaps:** we do not track the cost of the backup copies separately. The backup policy in `platform-docs/cloud/backups-and-restore.md` says the archive is backed up to a different region, and that cost is currently buried in the overall backup line. Also, the figure assumes the archive stays in the standard storage tier; if we move older scenes to a colder tier, the number will change and we should update this note.

## GPU hours per training run for the EO models

- **What it covers:** a full training run for one of the earth observation models, from data loading through to the checkpoint that gets pushed to the modelhub.
- **Current figure:** we plan on 2,100 GPU hours for a foundation-model fine-tune and 11,000 GPU hours for a full pretraining run. The pretraining figure is the one that matters for budget conversations.
- **How it is calculated:** from the cluster scheduler's accounting for completed runs, summing the GPU allocation for each job. The cluster metrics in `ml-docs/cluster/overview.md` give the per-job breakdown. We then take the median across the last several runs and round up to a round number.
- **Known gaps:** the figure does not include the GPU time spent on evaluation or on failed runs that get restarted. Both are real costs. Also, the pretraining figure is from before the cluster moved to the reservation scheme; pre-emption changes wall-clock behaviour, so the next time we do a full pretraining run we should re-check the number. Bruno Olsen has been tracking this informally and the `eo-models` channel is the place to ask.

## Open items

- The per-endpoint API cost multiplier keeps getting deferred. Ines Carvalho was going to look at it but got pulled onto other work. It is still on the FinOps backlog.
- The backup cost for the imagery archive should be split out so the TB-month figure is cleaner. The platform team knows this is coming.
- The pretraining GPU figure should be revisited after the next full run. There is a note in `ml-docs/cluster/getting-gpu-time.md` about how to get a compute estimate for a proposed run, and that is the right place to record the actuals.
