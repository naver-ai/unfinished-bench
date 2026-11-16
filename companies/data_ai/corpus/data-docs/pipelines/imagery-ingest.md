# Imagery ingest

**Owner:** Imagery acquisition and processing — Ana Asante's team  
**Last edited by:** Lucia Fonseca

This page describes how scenes arrive from our satellite providers and drone partners, and what happens between raw acquisition and the COGs and STAC items that the rest of the company consumes. It is maintained by the Imagery Operations team; if you spot something outdated, mention it in #imagery-ops.

## Providers and channels

We receive imagery through two main channels: direct downlinks from the satellite operators we task through the tasking portal, and file-based deliveries from our drone partners who fly for agricultural co-ops and for port surveys. A third, smaller channel is archive scenes bought from resellers, which follow the same ingest path once the files land.

Each provider has a delivery contract that specifies format, projection, bit depth and the maximum delay between acquisition and delivery. The tasking portal holds the order details and the expected delivery window; the imagery catalogue records what actually arrived and when.

## Ingest path

When a delivery lands on the ingest bucket, a workflow in the scheduler picks it up. The workflow checks the manifest against the order, verifies checksums, and registers a raw scene record in the imagery catalogue. From there the scene moves through:

1. **Orthorectification** — done on the batch pool using GCPs from our ground control library where available, otherwise from the provider's rational polynomial coefficients. We keep the ortho parameters in the STAC item's processing metadata so we can re-run when the provider re-releases a scene with updated coefficients.
2. **Cloud masking** — our cloud detector runs as part of the same job. The mask is stored as an asset alongside the COG, never burned into the pixel values, because downstream models and analytics customers both want the raw reflectance where possible.
3. **COG conversion** — the orthorectified, cloud-masked scene is converted to a Cloud Optimized GeoTIFF with overviews and an internal tiling scheme that matches our catalogue's zoom levels. The conversion step also writes the STAC item and attaches the QA flags.
4. **Registration** — the STAC item is published to the imagery catalogue and the scene becomes searchable through the data catalogue and the customer API console.

The whole path is one pipeline with retries on transient batch failures. If a step fails permanently, the workflow marks the scene as failed and sends a message to #imagery-ops with the run id and the provider order reference. We do not auto-retry scene-level failures more than twice; after that, a human looks at it.

## QA flags

Each STAC item carries a small set of QA flags that downstream consumers are expected to check:

- `cloud_cover` — percentage from the cloud mask, rounded to one decimal.
- `cloud_mask_quality` — one of `good`, `degraded`, `unusable`. Degraded means the detector had to fall back to a coarser model because of unusual atmospheric conditions; unusable means the mask is not trustworthy and the scene should be treated as unmaskeed.
- `ortho_quality` — set from the GCP residual statistics. `good` when residuals are within contract tolerance, `review` when they are not.
- `ingest_status` — `complete`, `partial`, `failed`. Partial is used when a scene arrived but one or more bands are missing or corrupt.

These flags are written by the ingest pipeline itself, not by a separate QA step. The reasoning is that the pipeline has the most context on each stage's own outputs. If you see a flag that looks wrong, raise it in #imagery-ops rather than editing the STAC item directly, because the catalogue is the source of truth for downstream subscriptions.

## Reprocessing on provider re-release

Satellite providers occasionally re-release a scene — same acquisition, new processing level, sometimes with updated RPCs or a corrected geolocation. The tasking portal shows a re-release notice for affected orders. When that happens, the Imagery Operations team reviews the notice and decides whether the change warrants reprocessing our COG and STAC item.

The decision rule is simple: if the re-release changes geolocation by more than half a pixel at our typical delivery resolution, or if the provider says the original release had a defect, we reprocess and the new version replaces the old one in the catalogue. The old STAC item is kept as a prior version in the imagery catalogue; it is not deleted. Downstream analytics runs that already consumed the old version keep their references, but any new query for that acquisition will get the reprocessed item.

Reprocessing is a manual trigger in the workflow scheduler, not automatic. Ana's team reviews each re-release notice and triggers the rerun through the same ingest pipeline with a `reprocess` flag. The pipeline reuses the already-downloaded raw files if the provider did not change them, but if the re-release includes a new raw scene, the download step runs again.

## Ground sensor tie-in

For flood monitoring products, the ingest pipeline also attaches the nearest ground sensor readings from the sensor network to the STAC item as a sidecar asset. This is done at ingest time, not on query, so the catalogue entry is self-contained for the subscriptions that use it. The sidecar is regenerated if we reprocess the scene, because the sensor time series is append-only and we want the asset to reflect the latest readings.

## Operational notes

- The ingest bucket is separate from the analytics data lake. Once COGs are written and registered, the raw files are retained for a rolling period and then archived to cold storage. See the ADR on COG storage for the reasoning.
- Provider deliveries that arrive outside the contract window are flagged in the catalogue and reported through the tasking portal's order status. We do not block ingest on late arrivals, but the flag is visible to customer-facing teams so they can set expectations.
- If a provider sends a scene that does not match the ordered AOI or band list, the ingest pipeline rejects it and sends a notice to #imagery-ops. The provider is then contacted through the tasking portal channel, not by phone or chat.
- Drone partner deliveries follow the same path, except the orthorectification step uses the drone's onboard GNSS and our local GCPs from the field app rather than provider RPCs. The sensor network team maintains the field GCP library and flags any GCP that has moved between field visits.

For questions about the catalogue schema, see the data catalogue. For questions about orthorectification parameters or cloud mask model versions, ask in #eo-models or #applied-ml. For anything about the pipeline code itself, the {{WORKFLOW_SCHEDULER|lower}} DAGs live in the data engineering repo and the on-call guidance for the scheduler is in the pipelines on-call page.
