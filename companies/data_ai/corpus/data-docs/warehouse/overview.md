# Analytics warehouse

Owner: Analytics warehouse  
Last edited by: Kaito Mori (Data Platform DBA)

## Purpose
Central warehouse for reporting, analytics and customer-facing data products. Sources: imagery catalogue, ground sensor network, tasking portal, CRM, support records, finance systems, and a few external feeds.

## Schemas

| Schema | Contents | Notes |
|---|---|---|
| `raw` | Landing zone for all ingested sources | Immutable; only the ingestion pipelines write here |
| `staging` | Cleaned, typed, lightly modelled tables | One table per source; dbt-owned |
| `marts` | Dimensional models for reporting and API consumption | The layer BI tools and notebooks read from |
| `finance` | Billing, revenue, cost and payroll data | Restricted access; see `finance-docs/` |

## Loading

- Nightly loads from the workflow scheduler kick off around the end of the working day; most source tables land by early the next morning.
- Sensor network data arrives more frequently via the field app and is merged into `staging` on a rolling window.
- Imagery ingest updates `raw` through the pipeline described in `data-docs/pipelines/imagery-ingest.md`.
- If a nightly load fails, the workflow scheduler retries once; after that, the on-call in #data-eng picks it up.

## dbt

- dbt project lives in the `warehouse` repository; models are organised by schema and source.
- Conventions are in `data-docs/warehouse/dbt-conventions.md`.
- Run `dbt test` before opening a PR; the CI job runs the full test suite on a fresh branch schema.
- Marts models must be `materialized='table'` unless they are tiny dimensions; staging models are views unless a view is noticeably slower.

## Access

- Warehouse access is requested through `handbook/it/access-requests.md`; the Analytics warehouse team approves.
- Read access to `marts` is broadly granted within engineering and customer-facing teams. Write access is limited to the Analytics warehouse team and the Data team.
- `finance` schema access needs an additional approval from FP&A.

## Cost of big scans

- Warehouse scans are billed to the requesting team's cost centre through the workload's cost tags. Big scans show up on the monthly cloud cost report (`finance-docs/finops/cost-reporting.md`).
- Full-table scans on `raw` are expensive; prefer partition filters. The `raw` tables are partitioned by event date where possible.
- If you need to scan a large share of a table, consider running it as a batch job rather than an interactive query.

## Connection and tooling

- BI dashboards connect through the warehouse connection pool; details in `data-docs/warehouse/connection-pool.md`.
- The notebook server connects to the same pool.
- BI dashboards follow `data-docs/bi/dashboard-standards.md`.

## Notes

- Warehouse tables being retired follow `data-docs/warehouse/retiring-tables.md`.
- The old reporting tool (the one on the analytics VM) is no longer supported; point new work at the BI dashboards or the notebook server.
