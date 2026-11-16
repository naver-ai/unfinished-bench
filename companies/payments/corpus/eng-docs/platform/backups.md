# Backups and restores

**Owner:** Infrastructure  
**Last edited by:** Tariq Beaumont (Platform Engineer)

## What we back up

- **{{SQL_DB_1|short}} clusters** — all production clusters, including the core ledger, charge/plan data, and the reconciliation tool's working store. Full base backup nightly, WAL archiving continuous. Off-site copy shipped to the Dublin DR region.
- **Ledger snapshots** — the event-sourced ledger's snapshot store is backed up on the same cadence as {{SQL_DB_1|short}}. Snapshot verification runs as part of the restore test.
- **Object storage** — merchant documents and payout files in the primary bucket are replicated cross-region. Versioning is enabled; retention follows the records schedule in `handbook/legal/records-retention.md`.
- **Config** — Infrastructure-owned config in the git repo plus the feature flag service export. The secrets manager is not backed up here; see `security-docs/secrets/secrets-management.md`.

## Retention

| Tier | Retention |
|---|---|
| Daily {{SQL_DB_1|short}} backups | 14 days on-site, 30 days off-site |
| WAL archive | 7 days |
| Weekly full backups | 8 weeks |
| Monthly full backups | 13 months |
| Ledger snapshots | same as {{SQL_DB_1|short}} |
| Object storage | per bucket policy, min 30 days |

We keep one monthly backup from the end of each calendar quarter for a full year beyond the 13-month window, mainly for audit requests.

## Restore tests

Restore tests run quarterly, coordinated by Infrastructure. Kenji Ramos (database reliability) picks a non-production cluster to restore into the Vilnius operations environment. The test verifies the restore completes, the data loads, and the cluster accepts writes. We also do one full ledger snapshot restore per quarter, alternating between the EU and US regions.

Results go in the `#sre` channel with a short summary. If a restore fails, the backup for that tier is considered suspect until re-verified.

## Asking for a restore

File a ticket in `tickets` with the `restore` request type. Include:

- System and cluster name
- Point-in-time or backup date wanted
- Target environment
- Owner of the data

Infrastructure triages restore requests twice a day, before the bank file cut-off and again mid-afternoon. Priority goes to anything affecting payouts or settlement data.

For urgent restores (production data loss or corruption), page the on-call via the paging tool and join `#incidents`.

## Notes

- The old `pg_backup` script was retired; everything now goes through the backup service in `deployctl`.
- Object storage restores for merchant-facing files go through the merchant success team so they can coordinate with the merchant.
- Quarterly restore tests were previously tracked by Yusuf; Tariq now owns the schedule and posts the reminders.
