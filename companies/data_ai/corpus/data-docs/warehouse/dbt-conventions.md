# dbt conventions

Owner: Data engineering · Last edited by Isaac Kaplan

## Model naming

- [ ] All models live under `warehouse/models/` in the analytics warehouse repo.
- [ ] File name equals the model name; use `snake_case`, no prefixes like `fct_` or `dim_` unless the table genuinely is a fact or dimension for the BI layer.
- [ ] For domain-specific models, prefix with the domain: `flood_`, `crop_`, `imagery_`, `sensor_`, `customer_`, `finance_`, `ground_`.
- [ ] Staging models: `stg_<source>_<entity>.sql` (e.g. `stg_imagery_catalogue_scenes.sql`).
- [ ] Intermediate models: `int_<domain>_<purpose>.sql`.
- [ ] Mart models: `mart_<domain>_<measure>.sql` only when they are consumed by the BI dashboards or the customer API console.
- [ ] Do not reuse a name that has been retired; check the data catalogue before creating something similar.

## Folders per domain

- [ ] Directory layout mirrors domains, not teams: `staging/`, `intermediate/`, `marts/`, then per-domain subfolders (`flood/`, `crop/`, `imagery/`, `sensor/`, `customer/`, `finance/`).
- [ ] Shared utilities (date spines, address helpers) go under `intermediate/shared/` with a comment at the top naming a Data engineering contact.
- [ ] If a model is used by two domains, put it one level up in `intermediate/` and reference it from there.
- [ ] Keep the `sources.yml` for a source system next to the staging models that read from it.

## Tests every model needs

- [ ] Every model gets a `unique` test on its primary key column (or a documented reason why not in the model header).
- [ ] Every model gets a `not_null` test on the primary key and on any column used as a join key in downstream models.
- [ ] Columns that are used for partitioning or clustering in the warehouse config get a `not_null` test too.
- [ ] Add `relationships` tests for foreign keys that point to a model in `marts/` or `staging/` — do not add relationships tests to raw source tables.
- [ ] Freshness tests on staging models for the ingestion pipelines: `imagery_ingest`, `sensor_network`, and `customer_api_events`.
- [ ] Add at least one `accepted_values` test on status or type columns; if the list is long, put it in a YAML variable and share it.
- [ ] Do not add `dbt_utils` tests unless they are already used in the same folder; ask in #data-eng if unsure.

## Docs blocks

- [ ] Every model file starts with a `{{ config(...) }}` block and a one-paragraph comment saying what the model is for and which team owns it.
- [ ] Use `docs` blocks for anything a BI user would need to interpret a column (units, null meaning, aggregation level).
- [ ] Column descriptions for `mart_` models go in `marts/<domain>/schema.yml`; keep them short and avoid restating the column name.
- [ ] If a model is deprecated or scheduled for retirement, mark it in the header comment.

## CI runs

- [ ] Every pull request to the warehouse repo runs dbt `build --select state:modified+` against a fresh schema named `dbt_ci_<branch>`.
- [ ] The CI run uses the `warehouse_ci` connection profile; do not point CI at the production `warehouse` profile.
- [ ] CI must pass all tests on the changed models and their direct parents before merge.
- [ ] If CI fails because of a failed test on an unchanged model, flag it in the PR and rerun; do not `--skip` tests silently.
- [ ] Only Data engineering can merge to `main`; the workflow scheduler picks up the merged state and runs the `dbt build` job on the production warehouse.
- [ ] The production run is the `dbt_warehouse_main` job; check its run history in the workflow scheduler before assuming a model is current.

## Backfilling a model

- [ ] For a small backfill (fewer than 10 partitions or a single day), run `dbt run --select <model> --vars '{"full_refresh": true}'` on a feature branch and then merge.
- [ ] For a large backfill, create a dedicated branch, run the backfill against a temp schema, and validate row counts against the old table before switching.
- [ ] Large backfills run through the batch cluster, not on a local machine or the notebook server.
- [ ] If the backfill changes numbers that are already published in the BI dashboards, post in #bi before starting and after finishing.
- [ ] Backfills that touch `finance_` models need a heads-up in #finance first.
- [ ] After a backfill, check the changed table in the data catalogue and confirm the partition layout matches the documented one.
