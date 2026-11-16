# Environments

Last edited by: Dina Ozturk (Site Reliability Engineer)  
Owner: Platform & SRE

This page describes the main runtime environments for Mossgrove's customer-facing and internal services. If you need to know where something runs, or whether you can deploy to it, start here.

## Overview

| Environment | Purpose | Who can deploy | Notes |
|---|---|---|---|
| Development (`dev`) | Local and shared dev instances for engineering | Any engineer (via `deployctl`) | No SLA; data may be reset at any time |
| Staging (`staging`) | Pre-production validation, integration testing, release rehearsal | Platform & SRE, Release Management; teams that deploy their own service (Payments platform for `billing-api`) | Masked customer data; refreshed from production snapshots periodically |
| Production (`production`) | Live customer traffic (UK, IE, US) | Platform & SRE; teams that deploy their own service (Payments platform for `billing-api`); releases coordinated by Release Management | Change windows; see `change-management.md` |

## What runs where

| Service | Dev | Staging | Production |
|---|---|---|---|
| `shop-web` (storefront) | Yes | Yes | Yes, multi-region (UK/IE, US) |
| `orders-web` (order management) | Yes | Yes | Yes |
| `billing-api` | Yes | Yes | Yes |
| `recs` (recommendations) | Dev instances per engineer | Yes (with masked data) | Yes, behind feature flags |

Staging runs the same service versions as production, minus the most recent hotfixes. The recommendation models in staging are trained on masked data and are not representative of production quality — treat any recs output from staging as indicative only.

## Data in staging

All customer personal data in staging is masked at rest and in transit between services. This includes names, email addresses, phone numbers, and order histories. The masking happens as part of the snapshot restore pipeline; if you spot unmasked data in staging, raise it with Platform & SRE via `#platform`.

Masked data is still subject to the data classification rules in the handbook — treat it as internal data, not public.

## Deploying

- **Dev**: engineers deploy directly to their own dev instances or shared dev via `deployctl`. No approval needed.
- **Staging**: Platform & SRE or Release Management can deploy. For most services this is automatic after a merge to the main branch; check the pipeline status in `#releases` if unsure. `billing-api` is not on the automatic pipeline — Payments platform deploy it themselves.
- **Production**: deploys are done with `deployctl`, by Platform & SRE or, for services a team deploys itself (such as `billing-api`), by engineers on that team who hold the service's deployer role. Release Management coordinates the timing; production deploys are changes, and `eng-docs/platform/change-management.md` describes how changes are raised and scheduled.

## Old notes

- The legacy CMS used to run in its own staging environment (`cms-staging`); that has been retired. Anything pointing at it should be using the current content platform instead.
- `shop-web` staging used to be managed by the web team directly; it is now under Platform & SRE like everything else.

## Related documents

- `eng-docs/platform/change-management.md` — change windows and approvals
- `eng-docs/oncall/oncall-guide.md` — what on-call can do in production
- `eng-docs/security/access-reviews.md` — who has access to which environments
- `handbook/it/access-requests.md` — requesting access to environments
