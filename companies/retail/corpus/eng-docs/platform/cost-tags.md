# Cloud cost tagging

Owner: Platform & SRE · Last edited: Diego Gallagher

## Required tags

Every cloud resource must carry these three tags:

- `team` — the team that owns the resource (e.g. `platform`, `web`, `finance-ops`, `wholesale`, `stores-ops`)
- `service` — the service or workload it belongs to (e.g. `shop-web`, `orders-web`, `pos-back-office`, `ledgerctl`, `logctl`)
- `env` — `prod`, `staging`, `dev`, or `dr`

Resources without all three tags will be flagged in the monthly report. Tagging is checked at deploy time for anything managed through deployctl; manually created resources are on the owning team to tag.

## Untagged resources report

The report is generated on the first working day of each month and posted to #platform and #finance-ops. It lists every untagged resource with its estimated monthly cost, grouped by the account it sits in.

If you see your team's resource in the report, add the tags within two working days. After that, the resource is included in the FinOps review as unowned and may be flagged for shutdown if it looks abandoned.

## FinOps review

Each month, Platform & SRE reviews the cost report with finance. We go through:

- Largest untagged or mis-tagged resources
- Spend by team and service versus the previous month
- Idle or oversized resources (especially in dev and staging)
- GPU lab usage from jobctl — any job queue beyond the allocated hours is charged back to the requesting team

Findings and agreed actions are summarised in #finance-ops. Teams can appeal a chargeback by replying to the summary thread within five working days.

For naming conventions, see `data-docs/catalogue.md`. For VM snapshot costs, see `eng-docs/platform/snapshots.md`.
