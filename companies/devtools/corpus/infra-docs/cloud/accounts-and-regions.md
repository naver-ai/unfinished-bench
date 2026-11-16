# Cloud accounts and regions

Owner: Site reliability  
Last edited by: Ava Fleming

## Account layout

Gantline Cloud infrastructure is split across {{CLOUD_PROVIDER|code}} accounts by environment and region. EU customer data stays in the EU region (see [ADR 0011](/eng-docs/adr/0011-regional-data.md)); US customer data is in the US region. Internal tooling (the admin console, helpdesk, chat, metrics) runs in a separate internal account per region.

| Account | Purpose | Region |
|---|---|---|
| `gnt-prod-us` | Production customer workloads, US | us-west-2 |
| `gnt-prod-eu` | Production customer workloads, EU | eu-central-1 |
| `gnt-staging-us` | Staging for US region | us-west-2 |
| `gnt-staging-eu` | Staging for EU region | eu-central-1 |
| `gnt-dev-us` | Development and CI for US region | us-west-2 |
| `gnt-dev-eu` | Development and CI for EU region | eu-central-1 |
| `gnt-internal-us` | Internal services, US | us-west-2 |
| `gnt-internal-eu` | Internal services, EU | eu-central-1 |
| `gnt-net` | Shared networking (transit gateways, DNS, egress) | us-west-2 |
| `gnt-buildfarm` | Build farm hosts, runner pools, image volumes | us-west-2 |

### Naming conventions

- Resources are tagged with `env`, `region`, `service`, and `team` per the [cost tagging policy](/infra-docs/cloud/cost-and-tagging.md).
- {{OBJECT_STORAGE|code}} buckets use the account name as a prefix: `gnt-prod-us-artifacts`, `gnt-internal-eu-backups`, etc.
- IAM roles follow `{service}-{env}-{purpose}`.

## Console access

Console access is granted through the identity provider (see [workforce SSO](/eng-docs/identity/sso-overview.md)). Most engineers get read-only access to the dev accounts on request; production access is limited to Site reliability, the hosted runners team, and the public API team.

To request access, open a ticket with the IT helpdesk and note which account and permission level you need. Approvals come from the team lead for the account in question (for `gnt-net` and `gnt-buildfarm`, that is Site reliability). Access reviews happen twice a year.

Break-glass access to the production accounts is handled through the paging tool; see the [on-call guide](/eng-docs/oncall/oncall-guide.md).

## Shared networking accounts

`gnt-net` holds the transit gateways and shared DNS zones. It is owned by network engineering; Site reliability has admin access for change implementation. The build farm account is owned by build infrastructure and is reachable over the VPN only.

For moving an endpoint between balancers, see [moving endpoints](/infra-docs/network/moving-endpoints.md).

## Notes

- The legacy `gnt-prod` account (pre-region split) is still readable for audit purposes. Write access was removed when the region split landed.
- `gnt-buildfarm` was previously called `gnt-registry`; old documentation and some dashboards still use the old name.
