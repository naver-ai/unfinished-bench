# ADR 0004: Store imagery as COGs with a STAC catalogue

**Status:** Accepted  
**Owner:** Imagery acquisition and processing  
**Last edited by:** Kofi Gupta  

## Context

The scene archive currently holds imagery in the native provider formats we receive from the satellite operators. When a customer requests a tile or a mosaic over an AOI, the serving pipeline has to convert on the fly from the original format, which is slow and puts a lot of load on the tiling workers. We have also had complaints from the analytics API team about latency on large-area requests, and the data science teams keep asking for direct read access to the archive instead of having to go through the tile service.

We looked at converting to Cloud-Optimized GeoTIFFs (COGs) with a STAC catalogue as the index layer. COGs let us serve tiles directly from object storage without a conversion step, and STAC gives us a standard way to describe the scenes, their footprints, and the acquisition metadata. The catalogue will be the single entry point for finding imagery, used by the tasking portal, the imagery catalogue, and the customers' API console.

## Decision

- All new imagery ingested into the archive will be converted to COG format as part of the ingest pipeline and stored in the existing imagery buckets.
- A STAC catalogue will be maintained alongside the COGs, with one item per scene. The catalogue will include the scene footprint, acquisition time, cloud cover, and a link to the COG asset.
- The tiling service will read directly from the COGs instead of converting from the provider format.
- The imagery catalogue and the analytics API will be pointed at the STAC catalogue as the discovery layer.
- Historical scenes will be converted in batches, starting with the most frequently accessed areas and the scenes referenced in open data releases.

## Consequences

- Ingest time will increase slightly because of the conversion step, but the serving path gets much faster and the tiling workers will need less CPU.
- Storage cost goes up a bit because COGs can be larger than the original compressed formats, but we can offset this by using the lower-cost storage class for older scenes after conversion.
- The STAC catalogue becomes a dependency for several downstream systems, so we need to monitor its availability in the same way we monitor the imagery buckets.
- Teams that currently read the provider formats directly will need to switch to the COG files. The warehouse team is unaffected, but the applied ML teams should update their training data loaders.

## Migration notes

- The conversion jobs run on the shared batch pool, coordinated through the workflow scheduler. Each job handles one scene or one small batch of scenes.
- Any scene that fails conversion is left in the original format and flagged in the STAC catalogue; the ingest pipeline will retry on the next run.
- The old provider-format files are kept for now and deleted after the COG has been verified readable by the tile service. Lucia Fonseca's script from the imagery ops folder does the verification.
- The STAC catalogue uses the same bucket naming convention as the imagery archive. The old catalogue index in the imagery catalogue app is being retired once the migration is complete.

## Loose ends

- Multi-band products and the radar scenes need a bit more work on the COG layout; the ingest pipeline handles the optical scenes first.
- The search ranking team wants to add a few extra STAC properties for better filtering; that will go through the normal catalogue schema change process.
- The sensor network team has asked whether the ground sensor readings can also be exposed through STAC; that is out of scope for this ADR and will be discussed separately.
- A few of the older scenes have unusual CRS definitions and may not convert cleanly; those will stay in the original format until we sort out a reprojection step.
