# Backups and restore

**Owner:** Cloud platform  
**Last edited by:** Malik Mbeki  
**Status:** In force  

## What we back up

- **{{SQL_DB_1|short}} databases** (all environments, including the warehouse control plane and the imagery catalogue's metadata store) — nightly full dump plus continuous WAL archiving. Restore point objective is 15 minutes.
- **The STAC catalogue** — the catalogue's backing database is included in the nightly dump. The catalogue's config (ingest rules, projection definitions) lives in the infrastructure repo and is covered by the repo's own history.
- **Configuration** — anything that defines what runs in the platform ({{IAC_TOOL}} state, {{K8S_PACKAGE_TOOL}} values, pipeline definitions) is versioned in git. We do not snapshot these separately; the repo history is the backup.
- **The imagery archive** — object storage versioning is enabled on the archive buckets. We keep 30 days of version history on the raw ingest bucket and 90 days on the processed COG bucket. Deletions and overwrites are recoverable within those windows without a restore request.

## What we do not back up

- **Scratch and intermediate outputs** — anything under the training cluster's scratch filesets or the batch pool's working directories is not backed up.
- **Application logs** — logs are retained in the log store per the platform retention policy, not as a backup.
- **Customer-delivered data** — if a customer uploads data through the tasking portal or the customer API console, that data is in the relevant service database and is covered by the nightly dump. We do not take separate copies.

## Retention

- Nightly database dumps: 14 days on disk, then 60 days in the cold bucket.
- WAL archives: 7 days.
- Imagery archive versions: as above (30 / 90 days).

## Restore tests

We run a restore test each quarter. The test restores the warehouse control plane database into a scratch project, verifies the catalogue metadata is readable, and checks that a sample of recent imagery objects can be retrieved from the archive version history. Results are posted to #cloud-platform. If a restore test finds an issue, the backup configuration is treated as an incident and triaged through the normal incident process.

## Asking for a restore

Open a ticket in tickets with the `restore` label and include:

- what needs to be restored (database name, bucket prefix, or config commit)
- the point in time to restore to (approximate is fine; we can work back from a known event)
- which environment

Cloud platform on-call picks these up. Routine restores are handled within one working day. If the restore is needed because of an active incident, raise it in #incidents instead and the on-call will take it from there.

## Loose ends

- The old backup tool (snapshotctl) is still referenced in a couple of runbooks; the current pipeline is the nightly dump plus WAL archiving described above. The runbooks should be updated when someone next touches them.
- The quarterly restore test was previously coordinated by the data platform team. It is now owned by cloud platform, but the calendar invite still lists the old coordinator. We should update that.
- The object storage versioning policy on the archive buckets was set when we migrated to the current storage class; it has not been revisited since. If the archive grows much faster than expected, the 90-day window on the processed bucket may need to be revisited.
- The cold bucket retention for dumps (60 days) is a round number from the original setup; there is no particular requirement forcing it. If storage costs on the cold tier become material, we can shorten it.
