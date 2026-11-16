# Backups

**Owner:** IT infrastructure  
**Last edited by:** Olivier Young  

## Context

Restore capability was reviewed with the platform and factory IT teams after the MES storage refresh. The previous arrangement had grown piecemeal, with different teams keeping their own copies of the same data and no single view of what was protected. This note records the agreed baseline.

## What is backed up

- **File shares** — department and project shares and home drives on `pool-b`.
- **Databases** — the ERP and MES databases are backed up nightly. The orders database is included via the ERP backup job; the calibration database is backed up with the lab systems.
- **Mail** — mailboxes and archives are covered by the mail system's own retention and are not part of the file-level backup sets. See the mail archive note in `tech-docs/messaging/mail-archive.md` for details.
- **MES shop-floor PCs** — configuration files and recipe masters are captured on the same schedule as the MES database. Individual PC images are not backed up; reimaging follows the standard build documented in `tech-docs/factory-it/mes-and-shopfloor.md`.

## Retention

- **Daily backups** — kept for 14 working days.
- **Weekly backups** — kept for 8 weeks.
- **Monthly backups** — kept for 12 months.
- **Yearly backups** — one set per calendar year, kept for 3 years.

Restore points follow the working-day calendar; a bank holiday does not shift the schedule.

## Restore tests

A restore test is run each quarter. The test covers one file share, one database restore and one MES configuration restore, rotated so that every share and database is exercised at least once per 18 months. Results are logged in the service desk portal under the backup project. The test is owned by IT infrastructure; the platform team runs the database portion and factory IT runs the MES portion.

The last three quarterly tests passed. The file-share portion of the most recent test used a share from the Greenville site to verify cross-site restore.

## Asking for a restore

Open a ticket in the service desk portal, category **Backup / Restore**. Include:

- the path or database name and the point in time you need
- which site the data belongs to (Reutlingen, Telford or Greenville)
- whether you need the data on the original share or delivered elsewhere (for example, a separate folder for comparison)

Restores are normally completed within one working day for file shares and on the same day for databases if the request is in before the mid-afternoon cut-off. Urgent restores for a down production line can be escalated through the on-call rota — mention that in the ticket and contact the service desk by phone.

## Loose ends

- Backup job names changed for the shares that have already moved to `pool-b`; `tech-docs/storage/nfs-a-retirement.md` still uses the old names in places.
- The monthly backup tape for the calibration database is still logged under the old lab calendar entry.
- The restore test schedule was previously maintained by the lab team; ownership moved to IT infrastructure but the calendar entry still shows the old owner. A ticket is open to update it.

## Related

- `tech-docs/storage/file-shares.md` — share layout and quotas
- `tech-docs/factory-it/mes-and-shopfloor.md` — MES configuration and reimaging
- `tech-docs/messaging/mail-archive.md` — mailbox retention and archive
