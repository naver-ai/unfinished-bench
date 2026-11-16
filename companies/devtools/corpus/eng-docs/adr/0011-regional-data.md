# ADR 0011: Keep EU customer data in the EU region

> Partly out of date since the US region went live — ask in #sre before relying on the implementation notes.

**Status:** Accepted, partly done  
**Owner:** Site reliability  
**Last edited by:** Bruno Costa

## Context

Several enterprise customers — mostly based in the EU — have asked for contractual assurance that their data stays in the EU. Sales and customer success have been fielding these requests for a while, and the answer so far has been "we'll get back to you". We need a concrete position and an implementation path.

The main pieces of customer data that live outside the core database are:

- Git repositories (repository storage behind git-gateway)
- Cloud workspaces (workspace disks and snapshots)
- Code search shards (managed by Search & indexing)
- CI artifacts and logs

There was also a question about whether the editor's local cache counts — it does not, that's ephemeral and on the customer's own machine.

## Decision

When a customer org is created, the admin console will let the org owner pick a data region: **EU (Frankfurt)** or **US (Oregon)** . The default is US. The region is set at org creation time and cannot be changed by the customer afterwards — if they move, they create a new org and we migrate the repos manually (that's a support ticket, not a self-service thing).

What gets pinned to the region:

- Repositories and their refs — repository storage needs region-aware placement keys
- Workspaces — workspace hosts are picked in the chosen region; the Hosted workspaces team has already done most of the work for this
- Code search shards — search indexes for EU orgs are written to EU shards only; queries from EU orgs are routed to those shards
- CI runs — the runner pool selection in the CI pipelines needs to prefer runners in the same region as the org

What does **not** move:

- The billing database — that stays in one place (the EU region). We treat that as internal data, not customer data, for the purposes of this ADR. The finance team has confirmed this is fine for their month-end processes.
- The admin console itself — it reads from the same database, so it's not region-pinned.

## Implementation notes

- The metadata in the billing service already has a region field on the org record; it just isn't populated yet. We need a backfill for existing orgs — defaulting to US is fine, but we should check with customer success whether any existing EU customers have already been promised EU residency. There may be a few.
- The search team has a design for region-aware shard placement; Yasmin has been driving that. It's mostly done but the routing layer still needs the org-to-region lookup.
- The release train and the mobile release train are unaffected — those are our builds, not customer data.

## Open questions

- **Backups:** where do backups live? Currently the backup system writes everything to one location. We need to decide whether EU backups must also stay in the EU, and if so, how long we keep them. The backup docs in infra-docs/storage/backups.md are going to need a section on this. This is the main blocker for calling the ADR fully done.
- **Support access:** when an EU org's data is in the EU region, support engineers in Portland will still need to access it for troubleshooting. We haven't decided whether that requires any special handling — the VPN works, but some folks on the support team have asked whether we need a formal policy. Probably not, but worth writing down.
- **Logs:** the observability stack currently aggregates logs from all regions into one place. We haven't decided whether EU org logs need to be filtered out of the global log stream. The SRE team has mixed opinions on this; it's not blocking the customer-facing commitment.

## Notes

- This ADR is partly done — the workspace and search parts are live, but the repository storage changes are still in progress. Site reliability is tracking that work in #sre.
- The SRE on-call guide in eng-docs/oncall/oncall-guide.md mentions region routing for incidents — that's now slightly stale, since we only have two regions and the routing logic is not in place yet. Will update when the repository storage work lands.
