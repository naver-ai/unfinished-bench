# infra-docs

Owner: Infrastructure (Joaquim Serrano). Last edited by Joaquim Serrano.

Index of infrastructure documentation. Each area lists the owning team and the channel where operational questions land.

- **Cloud** — `cloud/` — accounts, regions, tagging. Owned by Infrastructure. Questions in #sre.
- **CI** — `ci/` — pipelines, runner pools, artifact store. Owned by Release engineering & CI. Channel: #dev-productivity.
- **Build farm** — `build-farm/` — overview, image cache. Owned by Build infrastructure. Channel: #buildfarm.
- **Build hosts** — `build-hosts/` — scratch space on the big hosts. Owned by Build infrastructure. Channel: #buildfarm.
- **Lab** — `lab/` — VM leases, lab overview. Owned by the lab team. Channel: #lab-infra.
- **Network** — `network/` — DNS zones, VPN, moving endpoints. Owned by Network engineering. Channel: #netops.
- **Observability** — `observability/` — metrics and dashboards. Owned by SRE. Channel: #sre.
- **Storage** — `storage/` — backups. Owned by SRE. Channel: #sre.

Release engineering & CI owns the artifact store and the runner pools for hosted CI. Build infrastructure owns the build farm itself and the registry image volumes (see `build-farm/image-cache.md`).

For anything not obviously covered here, start in #engineering and someone will point you at the right page.
