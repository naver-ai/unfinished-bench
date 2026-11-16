# Backups

**Owner:** Site reliability  
**Last edited by:** Bruno Costa (Site Reliability Engineer)

## Scope

This document covers what Gantline backs up for our own production systems: databases, git repository storage, object storage, and configuration. It does not cover customer-managed data or the lab environment.

## What is backed up

- **{{SQL_DB_1|short}} and {{SQL_DB_2}} databases** — all production databases across the EU and US regions, including billing-service, identity, search metadata, and the code search index store. Backups run via the nightly `backup-db` job on the build farm.
- **Git repository storage** — the primary git store (the one behind code hosting) is snapshotted on a rolling schedule. We keep the snapshot chain on separate storage from the live store.
- **Object storage** — the main object store buckets (CI artifacts, editor uploads, mobile release assets) are copied to the alternate region on the same account. This does not cover the artifact store's internal caches.
- **Configuration** — service configuration, feature flag definitions, and balancer configs are exported nightly and stored in the config vault. This includes the CI pipeline definitions.

## Retention

- Database backups: daily for 14 days, weekly for 8 weeks, monthly for 12 months. The monthly chain is kept in the cold storage tier.
- Git store snapshots: 7 days of hourly snapshots, then daily for 30 days.
- Object storage copies: 30 days in the alternate region, then the copy expires.
- Configuration exports: 90 days.

## Restore tests

We run restore tests each quarter. The test covers one database (rotating through the services), one git store snapshot, and one object storage bucket copy. The restore test uses a couple of lab VMs for the database portion. Results are posted in #sre and tracked in the metrics dashboards.

The quarterly test rotates which service's database gets restored. If a restore fails, the on-call engineer follows the incident process in `eng-docs/oncall/incident-process.md`.

## Asking for a restore

To request a restore outside of the quarterly tests:

1. Open a ticket in the helpdesk, type **Incident**, and tag **Site reliability**.
2. Include the service name, the environment (production or staging), and the approximate point in time you need to restore to.
3. State whether you need the restore in place (overwriting the live data) or to a separate location.

Restores for production databases require a second person from the requesting team to confirm in the ticket. We do not restore into production without that confirmation.

For git store or object storage restores, mention which repo or bucket and the snapshot time if you know it. The on-call SRE will pick the nearest snapshot.

## Loose ends

- The restore test for the search index has been deferred twice; it needs a scheduled slot that does not clash with the search reindex window. Elena's team has been copied on the calendar invites.
- The cold storage monthly chain is still on the old `backup-vault` tool; the migration to the current storage tool was scoped but not scheduled.
- Restore permissions for the config vault are managed through the identity team's group structure. If you need access, ask in #it-help.

## Related

- `eng-docs/services/environments.md` — which environments are covered by these backups
- `infra-docs/cloud/accounts-and-regions.md` — region pairs and storage layout
- `eng-docs/oncall/oncall-guide.md` — how to reach the on-call SRE
