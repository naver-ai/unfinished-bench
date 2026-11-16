# Glossary

Owner: Data governance and open data · Last edited by Georgia Nunez

New to Brakwater and hitting terms you don't recognise? This page covers the ones that come up most in the first few weeks. It is deliberately short — one or two lines each, enough to get you unstuck in a meeting or a chat thread.

## Orders and imagery

| Term | Meaning |
|---|---|
| AOI | Area of interest — the polygon you give us when ordering imagery or running an analytics query. Stored on the order and used by ingest to clip products. |
| Tasking order | An order for imagery that has not been captured yet; we task the satellite to acquire it over the AOI on a future pass. |
| Archive order | An order for imagery already in our catalogue; delivered from the archive, usually within a couple of working days. |
| GSD | Ground sample distance — the pixel size on the ground, in metres. Smaller GSD means finer detail. Our tasking options are quoted by GSD class. |
| Revisit | How often a satellite passes over the same point. Affects how frequently we can refresh a customer's monitoring AOI. |
| Cloud cover threshold | The maximum acceptable cloud fraction over the AOI for an order to be considered usable. Set per order; if the acquired scene exceeds it, the tasking portal offers a re-task or archive alternative. |
| Orthorectification | Geometric correction that removes terrain and sensor distortion so the image aligns to a map projection. All delivered products are orthorectified before they reach the customer. |

## Data formats and storage

| Term | Meaning |
|---|---|
| COG | Cloud Optimised GeoTIFF — a TIFF layout that allows range requests instead of downloading the whole file. Our default delivery format for raster products (see platform-docs/adr/0004-imagery-as-cogs.md). |
| STAC item | A single JSON document describing one scene or asset — footprint, acquisition time, cloud cover, links to the COGs. The atomic unit in the imagery catalogue. |
| Tile | A fixed grid square in a tiling scheme (zoom level plus x/y). Used for analytics outputs and for serving imagery to dashboards; not to be confused with a STAC item, which is scene-based. |

## Sensors and labels

| Term | Meaning |
|---|---|
| Gauge | A water-level sensor in our ground network, mounted on a structure, reporting continuously. Typically in rivers, canals and ports. |
| Probe | A soil-moisture or temperature sensor buried at a plot, read on a schedule via the field app. Different maintenance route from gauges; see data-docs/sensors/sensor-network.md. |
| Ground truth | Field observations used to check or train our models — gauge readings, probe readings, or survey notes. Always carries a timestamp and a source. |
| Label set | A curated collection of ground truth plus the imagery pixels they correspond to, prepared for training a model. Managed in the labelling workflow (ml-docs/training/labelling.md). |
| Frozen eval set | A fixed set of labelled scenes held aside for comparing model checkpoints. Changes to a frozen set are agreed in #eo-models and recorded in its metadata. See ml-docs/eval/offline-evaluation.md. |

## Finance periods

| Term | Meaning |
|---|---|
| P1–P13 | The thirteen accounting periods in our financial year. P1 starts at the beginning of the financial year; P13 is the closing period. Close tasks in finance-docs/period-close.md refer to periods, not calendar months; the cloud cost report (finance-docs/finops/cost-reporting.md) is the exception and runs by calendar month. |

A few things worth knowing that don't fit in a table:

- When a customer says "order", they may mean a tasking order, an archive order, or a standing monitoring subscription that produces repeated deliveries. The tasking portal distinguishes these clearly, but conversation often doesn't — ask which one they mean if it affects delivery time or price.
- "Revisit" and "GSD" are the two numbers most customers compare us on, and they trade off against each other: finer GSD usually means a narrower swath and a longer revisit for the same area. If a customer asks for both extremes, point them at the customer success team rather than over-committing in a chat.
- The imagery catalogue stores STAC items, not tiles. Tiles are derived at query time. If you find yourself about to write a query that assumes tiles are stored, check data-docs/catalogue.md first.
- Orthorectification is applied automatically in ingest for archive and tasking deliveries. The only place you will see raw (unrectified) scenes is inside the ingest pipeline itself — never in a customer product.
- Frozen eval sets are the closest thing we have to a common currency between the EO models team and applied ML. If you are proposing a change to one, expect it to go through model governance, not just the team that owns the model.
