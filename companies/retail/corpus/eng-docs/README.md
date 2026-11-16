# eng-docs

Index of engineering documentation, by team and topic. Owner: Engineering. Last edited by Helen Garside.

- **Web (shop-web, checkout, orders-web)**: `web/` — shop runbook, feature flags, cache tier, checkout latency, orders-web overview.
- **Platform (infra, {{SQL_DB_1|short}}, DNS, backups)**: `platform/` — environments, change management, runtime config, snapshots, backups, cost tags, DNS.
- **Data (warehouse, pipelines, sharing)**: `data/` — warehouse notes, pipeline on-call. See also `data-docs/` for catalogue and DPIA notes.
- **ML (recommendations)**: `ml/` — GPU lab, model release, recs overview.
- **Security**: `security/` — access reviews, log tiers, secrets, vuln management.
- **On-call**: `oncall/` — incident process, on-call guide.

ADRs live in `adr/` (numbered, e.g. `0007-move-to-managed-database.md`). New decisions go there; see `0001` for the process.

To add a page: create the file under the relevant subfolder, add one line to this README, and link it from the team's doc index in `#platform` or `#data-eng`. Keep naming consistent — kebab-case, no dates in filenames.

Check `logctl` docs in `security/log-tiers.md` if you're touching log storage. Warehouse schema changes go through `#data-eng` review first.
