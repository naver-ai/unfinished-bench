# ADR 0007: Move to managed {{SQL_DB_1|short}}

**Status:** Accepted  
**Owner:** Platform & SRE  
**Last edited by:** Laszlo Ikeda  

## Context

Mossgrove runs several self-hosted {{SQL_DB_1|short}} clusters across the Leeds DC and the Wakefield DC. The main OLTP databases for shop-web and orders-web have been on self-managed instances since before the Columbus operation existed. Over the past two years the operational burden has grown: minor version upgrades, vacuum tuning, and failover testing consume a disproportionate amount of Platform & SRE time. We have also had two incidents where a misconfigured replica lag caused read timeouts for the wholesale portal during peak order processing.

At the same time, the Dublin tech hub has been standardising on the managed {{SQL_DB_1|short}} offering from our cloud provider for newer services. The analytics warehouse team already uses it for staging copies of the warehouse schema. The sentiment from #platform and #data-eng is that managed instances would free up roughly one full-time equivalent across the quarter.

The stores estate adds some urgency: the POS back office reads from replicated copies of the orders database for store-level reporting, and those replicas are maintained manually by Noor's team through a set of scripts that predate the current change management process. A managed service gives us automated replica management and clearer upgrade windows.

## Decision

We will migrate the self-hosted {{SQL_DB_1|short}} clusters that back shop-web, orders-web, and the wholesale order management interface to managed {{SQL_DB_1|short}} instances. The migration will happen in phases:

1. **Phase 1** – Stand up managed instances in the same region as the current primary, configure logical replication from the existing primaries, and run a parallel read-only workload against the managed replicas for one full working week.
2. **Phase 2** – Switch write traffic to the managed instances during a planned maintenance window coordinated through the change management process. Keep the old clusters available for one week for rollback.
3. **Phase 3** – Decommission the old clusters, and update the runbooks in `eng-docs/platform/environments.md` and the orders-web runbook.

The migration will use the existing event bus (ADR 0012) to drain in-flight order events before the cutover, so no orders are lost. The warehouse and reporting replicas will be re-pointed to the managed instances after Phase 2.

## Consequences

- Operational overhead for patching and failover moves to the provider. We retain responsibility for schema migrations, connection pooling, and query performance.
- Cost will increase slightly; we will track this under the existing cost tags in `eng-docs/platform/cost-tags.md`.
- The POS back office replica reads should become more reliable, which Retails ops has flagged as a win for store closing procedures.
- Some existing tooling that wraps `pg_ctl` and custom backup scripts will be retired. Backups will use the managed snapshot facility instead, and the backup verification steps in `eng-docs/platform/backups.md` will be updated.
- The `pgbench`-based load generation we used to validate the old hardware will no longer be needed.

## Migration notes

- The Dublin team has already migrated the recommendation service's smaller database to managed {{SQL_DB_1|short}} and reported no issues. Their notes on connection limits are in the `#ml-recs` channel.
- The wholesale credit control team uses a direct read-only connection for reporting; we need to update the connection strings in their finance warehouse import job before Phase 2.
- Grant access to the new instances via the existing secrets mechanism in `eng-docs/security/secrets.md`.
- A rollback plan is documented in the change ticket; it involves flipping the DNS entries back and re-pointing the replicas, which we expect to take under an hour.

## Deciders

Daniel Kruger, Owen Castillo, and the Platform & SRE team. Input from Tom Whitlock on cost approval, and from the Web team on the orders-web cutover window.
