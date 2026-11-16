# Service catalogue

Owner: Product engineering · Last edited by Ingrid Holm

This catalogue lists the main services that make up Gantline Cloud, who owns them, and where to find the team. It is meant as a quick pointer for anyone triaging an issue or looking for the right channel to raise something in. For build and runtime details of a service, see the service's own repo and `eng-docs/release/builds-and-runtimes.md`.

| Service | Owning team | Tier | Repo | Channel |
| --- | --- | --- | --- | --- |
| git-gateway | Site reliability | 1 | `git-gateway` | #sre |
| workspaces-api | Hosted workspaces | 1 | `workspaces-api` | #engineering |
| runner-scheduler | Hosted runners | 1 | `runner-scheduler` | #engineering |
| search-indexer | Search & indexing | 2 | `search-indexer` | #search |
| search-query | Search & indexing | 1 | `search-query` | #search |
| public-api | Public API | 2 | `public-api` | #api-platform |
| auth | Identity & access | 1 | `auth` | #identity |
| billing-service | Billing engineering | 1 | `billing-service` | #billing-ops |
| notifications | Mobile apps | 2 | `notifications` | #mobile |

Tier 1 services are the ones where an outage pages the on-call engineer. Tier 2 services page during business hours only. The on-call rotation and what to do when paged are in `eng-docs/oncall/oncall-guide.md`.

The owning team is the one that reviews changes to the service and owns its roadmap. That does not mean only that team touches the repo — for example, `auth` gets contributions from Product security and Site reliability regularly. If in doubt about a change, start a thread in the channel listed and someone from the owning team will pick it up.

Two services deserve a little extra context:

- **runner-scheduler** allocates build work to hosted runners and to the internal runner pools. It is separate from `git-gateway`, which handles repository traffic. If a customer reports slow queues, check the scheduler's dashboards first; if they report pushes hanging, that is more likely `git-gateway`.
- **public-api** is the surface that customers and partners integrate against. It depends on `auth` for caller identity and on `search-query` for code search endpoints, so incidents there often have a dependency chain worth checking before paging multiple teams.

For anything that touches billing data or customer account state, the billing-service repo is the right home; the Billing operations team watches `#billing-ops` and can help route edge cases.

Changes to this catalogue (new services, tier changes, ownership moves) should go through a PR with the owning team's review. Ingrid's team keeps an eye on the file and will flag stale entries.
