# Backups and restores

**Owner:** Infrastructure & SRE  
**Last edited by:** Sebastian Marchetti, Infrastructure Manager

## What is backed up

- **EHR database** — full nightly backup via the database maintenance window. Transaction log shipping to the South Bend DR site every 15 minutes.
- **File shares** — primary shares in South Bend and Kalamazoo, including the scanned chart staging area before it moves to chartarc. Backed up nightly, incremental with a full copy each quarter.
- **Configuration** — network device configs, VPN gateway configs, and the interface engine route definitions. These are exported after each change and copied to the backup vault weekly.
- **Research Institute study data** — the EDC database and the study data sharing service are backed up on the same schedule as the EHR database. The eIRB system and CTMS are covered by the file share backup.
- **Claims systems** — the claims payment queue and prior authorization queue databases are included in the nightly database backup set. The records platform's document archive buckets are not part of this backup schedule.

## Retention

| Backup type | Retention |
| --- | --- |
| Nightly full (databases) | 35 days |
| Transaction logs | 7 days |
| File share incrementals | 60 days |
| Quarterly full (file shares) | 18 months |
| Config exports | 6 months, then archived |

The EHR database nightly backups are also copied to the Kalamazoo campus once per week for the Research Institute's internal reporting warehouse.

## Restore tests

The Infrastructure & SRE team performs a restore test once each quarter. The test covers:

- EHR database restore to a non-production instance
- One file share restore (rotates between South Bend, Valparaiso, and Kalamazoo shares)
- One config export restore

The quarterly test is scheduled through the change management process. Results are posted to #infrastructure. If a restore test fails, the issue is tracked as a major incident and the backup job for the affected system is paused until the root cause is confirmed.

## Requesting a restore

Open a ticket through **tickets** with the **Backup & Restore** category. Include:

- System or share name
- Point-in-time (date and approximate time of day)
- Files or database objects needed
- Business reason

Restores are handled in priority order:

- **Priority 1** — patient safety events, EHR downtime recovery, active clinical care
- **Priority 2** — claims payment runs, member-facing communications
- **Priority 3** — research data, non-clinical file shares, administrative requests

The on-call engineer can approve and perform priority 1 restores outside business hours. Priority 2 and 3 restores are performed during business hours by the Infrastructure & SRE team.

For EHR database restores, coordinate with the HIS platform team through the ticket — they need to shut down the interface engine feeds before the restore starts. The service desk has the current list of who to page for that.

## Loose ends

- The old backup server in Valparaiso (the one that ran the pre-chartarc archive) is still listed in the monitoring dashboard but has been decommissioned. The dashboard entry should be removed.
- Lucia's backup verification script from the last quarterly test was never merged into the backup job definitions. It lives in the infrastructure scripts folder if anyone wants to pick it up.
- The restore test schedule was moved earlier in the quarter — the change management ticket references the old timing. The change management doc should be updated to match what we actually do.
