# data-docs

Index of data documentation for the warehouse, pipelines, sensors, imagery and governance.

## Where to start

- [Data catalogue](catalogue.md) — source of truth for dataset owners, freshness and access. If a dataset isn't in there, it isn't tracked.
- [Warehouse overview](warehouse/overview.md) — what lives in the warehouse and how it maps to the catalogue.
- [dbt conventions](warehouse/dbt-conventions.md) — read before touching models.
- [Connection pool](warehouse/connection-pool.md) — the warehouse connection pool.
- [Imagery ingest](pipelines/imagery-ingest.md) — how scenes land in the catalogue and warehouse.
- [Sensor network](sensors/sensor-network.md) — ground sensor streams and field app sync.

## Who to ask

- Warehouse: Analytics warehouse (Owen Gallagher's team). dbt: Data engineering (Joanna Kowalski's team).
- Pipelines and scheduler: Data engineering on-call, see [scheduler-oncall](pipelines/scheduler-oncall.md).
- Imagery catalogue and ingest: Imagery acquisition and processing (Dara or Lucia).
- Ground sensors: Sensor network engineering (Xavier).
- Access to data: follow [data-access](governance/data-access.md); approvals go through the data owner listed in the catalogue.

## Conventions

- Retiring tables: [retiring-tables](warehouse/retiring-tables.md).
- Open data releases: [open-data](governance/open-data.md).
- DPIA notes live in [dpia-notes](governance/dpia-notes.md).
- Heavy warehouse reads can run as batch jobs — see platform-docs/batch/submitting-jobs.md.

Owner: Data engineering. Last edited by Isaac Kaplan.
