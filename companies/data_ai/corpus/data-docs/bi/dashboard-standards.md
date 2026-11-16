# Dashboard standards

Owner: BI and reporting. Last edited: Mina Silva.

## Naming

- Dashboard titles follow `[Subject] – [Audience or purpose]`, e.g. "Imagery tasking – weekly ops review".
- File names are kebab-case and match the dashboard title after the dash, e.g. `imagery-tasking-weekly-ops-review`.
- Prefix internal-only dashboards with `int-`; customer-facing dashboards (shared via the customer API console) get no prefix.
- Use the data catalogue names for metrics; do not invent synonyms in titles.

## Certification

- A dashboard is `certified` when the BI and reporting lead has signed off on the underlying warehouse tables and the metric definitions.
- Certified dashboards show the badge in the BI dashboards tool; everything else is `draft` by default.
- Draft dashboards may be shared within a team but should not be linked from the handbook or used in customer-facing materials.
- Certification review happens when the dashboard is created and again after any change to its underlying tables.

## Refresh

- Set refresh to match the data cadence: daily for sensor network and imagery ingest dashboards, twice a week for warehouse cost views, monthly for finance and subscription metrics.
- Dashboards reading large warehouse tables get a refresh no more often than hourly.
- If a refresh fails twice in a row, the owning team sees a notification in #bi and the dashboard is marked stale until fixed.

## Ownership

- Every dashboard has exactly one owner, listed in the dashboard metadata and in the BI dashboards tool.
- The owner is responsible for refresh health, access requests, and answering questions in #bi.
- When someone leaves a team, the BI and reporting lead reassigns their dashboards within a month; the old owner's name is removed from metadata at that point.

## Retiring

- A dashboard with no views for two consecutive quarters is flagged in the monthly BI review.
- The owner either confirms it stays (and why) or schedules retirement; retired dashboards are archived, not deleted, for a year.
- Before retiring, check the CRM and support docs for links; update or remove them the same working day.
