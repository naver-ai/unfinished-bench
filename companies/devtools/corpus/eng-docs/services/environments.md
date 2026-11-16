# Environments

This page describes the environments used by the Gantline Cloud platform and the internal tooling around it. It is owned by Site reliability; reach out in #sre if something here is unclear.

## What runs where

| Environment | Region | Purpose | Customer data |
| --- | --- | --- | --- |
| dev | EU (shared, Lisbon) | Local development, feature work, integration testing against real services | Synthetic data only |
| staging | EU (shared, Lisbon) | Pre-production validation of releases, load checks, migration rehearsals | No customer data ever. Seeded with generated orgs and repos. |
| production (EU) | EU (Frankfurt) | Customer-facing service for EU customers | Yes |
| production (US) | US (Oregon) | Customer-facing service for US customers | Yes |

Production runs as two separate regions. Each region has its own control plane, data stores, and runner fleet. The code deployed to both regions comes from the same release train; the configuration that differs between regions lives in the per-region settings in the admin console.

Staging is the only place where we run a full copy of the service topology (API, billing-service, search index, runner pools) on a smaller scale. It shares the build farm with dev but has its own namespaces. The nightly builds run against staging before any release candidate is promoted.

## Deploying

| Environment | Who can deploy | How |
| --- | --- | --- |
| dev | Any engineer | `gnt deploy dev` from a working tree, or via the CI pipeline on merge |
| staging | Any engineer, on merge to the staging branch | CI pipeline promotes the built artifact |
| production (EU and US) | The release captain for the day, or Site reliability on duty | The daily release train (`gnt deploy promote`), see `eng-docs/release/release-train.md` |

Production deploys go out with the daily release train: canary in the US region, then the EU region. The release captain runs the train.

Staging holds no customer data, so destructive migrations can be tried there freely. A migration that touches production is rehearsed on staging first, with the runbook linked in the PR.

## Notes

- The US region was added after the original EU deployment; some older dashboards still label it "prod-west". The metrics dashboards have been updated, but a couple of alerts in the paging tool have not caught up.
- The lab hypervisors (see `infra-docs/lab/lab-overview.md`) are a separate environment entirely; they are not part of the dev/staging/production split above.
- VPN access is required to reach the admin console and the internal API for staging; production APIs are reachable over the public endpoints with the right credentials.
