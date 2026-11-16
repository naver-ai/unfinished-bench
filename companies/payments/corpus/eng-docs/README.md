# eng-docs

Engineering documentation index. Owner: Engineering. Last edited by Mateo Silva.

## Areas

- **architecture/** — system overview and ADRs. ADRs live in `adr/`, numbered and immutable once accepted.
- **data/** — warehouse and lake pipeline runbooks, mostly for the data platform on-call.
- **dev/** — merging, release train, and general workflow notes.
- **edge/** — partner access at the edge, WAF-related notes.
- **incidents/** — incident process and status page guidance.
- **merchant-api/** — webhooks and API-facing behaviour.
- **oncall/** — the on-call guide; start here before any rotation.
- **payments-bus/** — message store internals.
- **platform/** — deploys, environments, backups, DNS, data transfers, change management.
- **sre/** — monitoring and SLOs.

## Adding a page

Create the file under the relevant area directory. Keep titles short. Link to it from the area README if one exists, or from `architecture/overview.md` for cross-cutting topics. If you add an ADR, follow the numbering in `adr/` and get it reviewed in #platform before committing.

## Notes

- `eng-docs/platform/change-management.md` references the tickets project; the process now runs through the change board in #sre.
- ADR numbers are never reused, even for ADRs that were withdrawn.
