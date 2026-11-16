# Analytics warehouse

Owner: Data engineering · Last edited by Leila Doyle

## Main schemas

- `core` — customer, order, product, stock. Source of truth for reporting.
- `fulfilment` — DC and store dispatch, carrier scans, delivery exceptions.
- `wholesale` — accounts, invoices, credit notes, payment allocations from the ledger.
- `marketing` — campaign sends (mailer), click/open, paid channel spend.
- `storeops` — till transactions, cash ups, POS back office extracts.
- `support` — helpdesk tickets, dispute cases, refunds.

## Nightly loads

- Refresh runs off the `warehouse-jobs` VM.
- Order, product and stock deltas land from the shop DB via `deployctl` job hooks.
- Store till data arrives from each store's back office after close of business — any store that misses the upload shows in the `storeops` load report.
- Wholesale AR is pulled from the ledger after the daily posting run.
- If a load fails, the pipeline retries twice before the on-call page goes out.

## dbt project

- Repo: `data-warehouse-dbt` (same org as `data-docs`).
- Profiles live in the analytics warehouse vault entry; don't commit credentials.
- Run `dbt build` from the `warehouse-jobs` VM. CI runs `dbt test` on PRs.
- Models are organised by schema above; staging is `stg_` per source.
- Materialisations: core models are tables, everything else is views unless noted in the model file.

## Access requests

- Read access via `sharectl` grant — request through the tickets queue, assign to Data engineering.
- Warehouse write access is limited to Data engineering and the analytics warehouse service account.
- External sharing (wholesale partners, agencies) must follow `data-docs/sharing.md`.

## Cost of big queries

- Ad-hoc queries against `core` should filter on `order_date` or `created_at` — full scans are charged back to the requesting team's cost tag.
- Monthly cost report is sent to the finance ops channel; anything over £200 in a month gets a follow-up from Leila.
- Use the `warehouse_usage` table to check query cost before running something large.

## Notes

- The `ml-recs` team reads product views from here — if you change a column name in `core.product`, tell them before merging.
- `logctl` archives older warehouse logs to the cold tier after 90 days.
- The old `warehouse-legacy` schema is still readable but frozen — new work should use `core`.
