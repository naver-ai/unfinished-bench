# Backups

**Owner:** Platform & SRE  
**Last edited by:** Owen Castillo (Senior Site Reliability Engineer)  

## What We Back Up

- **{{SQL_DB_1|short}} databases** (orders-web, catalogue, CRM, warehouse staging) — nightly dumps via the `pg_dump` job on the db hosts. Dumps go to the `mossgrove-backups` bucket in {{CLOUD_PROVIDER|code}}.
- **Object storage** — the `mossgrove-media` bucket (product images, brand assets) and `mossgrove-docs` (finance scans, supplier contracts) are replicated to a second region. Replication is continuous, no versioning on `mossgrove-docs`.
- **Config** — {{IAC_TOOL}} state is backed up to the same bucket as part of the nightly run. Feature flag service config is exported weekly and stored alongside.
- **Legacy CMS** — still doing nightly dumps of the CMS database until the migration to the new content platform is fully complete (see ADR 0015).

## Retention

- {{SQL_DB_1|short}} dumps: 14 days daily, then weekly for 8 weeks, then monthly for 12 months.
- Media bucket: replicated, no additional retention (we keep everything).
- Config exports: 30 days.
- Legacy CMS dumps: 30 days, then deleted — do not extend without checking with Platform first.

## Restore Tests

Each quarter, Platform & SRE runs a restore test on a random nightly dump. We spin up a throwaway instance from the dump and run a set of sanity queries (orders count, recent transactions, catalogue rows). If anything fails, we raise a ticket in `tickets` and re-run the following week.

The quarterly test is booked in the Platform calendar — check with Owen or Dana if you need to move it.

## Asking for a Restore

If you need data restored (e.g. a bad migration, accidental delete, or a store till issue that wiped local data), raise a ticket in `tickets` with the `backups` label and include:

- The database or bucket and table/prefix if relevant
- The point in time you need (we can go back as far as the retention allows)
- Why you need it (one line is fine)

Platform & SRE will action it within one working day. For urgent restores (production down), ping `#incidents` and we'll bump it.

## Loose Ends

- The old backup script on the Wakefield DC file server (`backup_share.sh`) is still referenced in a couple of runbooks — it was retired when we moved to the {{CLOUD_PROVIDER|code}} bucket. If you see it, ignore it.
- The CRM team used to own the {{SQL_DB_1|short}} backup schedule; that moved to Platform a while back, but the CRM on-call page may still say otherwise.
- We should document the restore test procedure properly in `eng-docs/platform/snapshots.md` — it's currently just in Owen's head and the quarterly calendar invite.
