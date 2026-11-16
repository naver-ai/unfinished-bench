# Analytics warehouse

**Owner:** Data platform  
**Last edited by:** Mia Palmer (Data Platform Manager)

## Purpose

The analytics warehouse is the single place for reporting and analysis across Kilbarra. It holds transformed data from the data lake, organised into schemas that reflect our core business objects. Most reporting, the merchant dashboard's analytics views, and the treasury workstation's daily summaries read from here.

## Main schemas

- `core.transactions` — card transactions, payouts, refunds, chargebacks, and adjustments. One row per event; joins to `core.merchants` on `merchant_id`.
- `core.merchants` — current merchant record, risk tier, segment, acquiring bank, settlement currency. History lives in the lake; this is the point-in-time view.
- `core.payouts` — payout runs and individual payout legs, including bank reference and settlement date. Treasury reconciles against this weekly.
- `core.disputes` — dispute lifecycle, from first notification through representment and outcome. Used by risk and merchant success for chargeback monitoring.
- `finance.daily` — daily aggregates used by the month-end close (revenue, fees, float). Owned by Finance engineering; changes go through `#finance-eng`.
- `risk.signals` — outputs from the transaction monitoring system and risk model scores. Retained per the records retention schedule; do not add consumers without checking with risk.

## Loads

- Nightly loads from the data lake land in `staging` before the dbt run. The load window is between the lake's evening cut-off and the start of the Dublin business day.
- The dbt project lives in `analytics/dbt` in the data platform repo. Models are organised by schema; `staging` → `core` → `marts`.
- Load failures page the data platform on-call. The runbook is in `eng-docs/data/lake-pipelines.md`; warehouse-specific steps are covered in the same flow — ask in `#data-lake` if the section has moved.
- Backfills are run manually from the analytics VM. Do not run a backfill that touches `core.transactions` without posting in `#data-lake` first — the disputes team has had surprises from late adjustments.

## Cost

- Big queries are the main cost driver. The warehouse is sized for our nightly transforms and dashboard traffic, not for ad-hoc scans over the full transaction history.
- If a query touches more than ~1B rows or runs over an hour, it will be killed. Use the `marts` tables for anything interactive.
- For heavy analysis, copy the data you need into your own scratch schema (`scratch_<name>`) and drop it when done. Scratch schemas are purged after 30 days.
- Query cost is attributed to the team of the service account used. The monthly warehouse cost breakdown goes to each team lead; if yours looks off, check for scheduled jobs pointing at the old `analytics_legacy` project.

## Access

- Read access to `core` and `finance` is granted through the `warehouse_reader` group in the analytics warehouse tool. Request via the access form in `#it-help`; approvals follow the data classification in `handbook/security/data-classification.md`.
- `risk.signals` is restricted to risk and compliance. Requests go to `#risk-controls`.
- Write access to `core` schemas is only for the service accounts used by the dbt runs. If you need a one-off write, use your scratch schema.
- Access reviews for the warehouse are part of the quarterly access review in `security-docs/access/access-reviews.md`.

## Notes

- The `analytics_legacy` project is still around for the old reports that haven't been migrated. Do not point new work at it; the migration list is tracked by Data platform and most of it has moved.
- Shreya Bergstrom owns the dbt model for `core.payouts`; ping her for changes to payout logic.
- If you are building a new mart, add it to the dbt project and get a review from Data platform before merging. The merge process is `eng-docs/dev/merging.md`.
