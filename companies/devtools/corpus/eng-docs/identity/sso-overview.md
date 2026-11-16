# Workforce SSO

**Owner:** Identity & Access  
**Last edited by:** Camille Andersen

## Overview

Gantline uses a single identity provider for workforce sign-in across both offices and for remote staff. Every employee, contractor, and intern gets an account provisioned through the HR system. The Identity & Access team manages the IdP configuration, but the day-to-day account lifecycle starts with HR data.

## Identity provider

We run {{IDENTITY_PROVIDER}} as our workforce IdP. It is the source of truth for authentication to Gantline Cloud admin, the helpdesk, chat, the HR system, the expense tool, the CRM, the status page, the paging tool, the password manager, the email platform, the data warehouse, and the feature flag service. Internal engineering tools like `gnt` authentication and the artifact stores use the same IdP where feasible; anything that cannot integrate directly uses a service account (see below).

## Group sync from the HR system

Groups are derived from HR system attributes through the HR system's SCIM connector. The Identity team does not hand-edit group memberships in the IdP; if a group looks wrong, the fix goes through the HR system. Key synced groups:

- **All staff** – everyone with an active employment or contract record.
- **per-office** – `lisbon` and `portland`.
- **per-team** – based on the department and team fields, e.g. `team-identity`, `team-sre`, `team-customer-success`.
- **per-role** – e.g. `role-manager`, `role-oncall-engineer`.

Group names follow `team-<slug>` and `role-<slug>` conventions. If a team changes its name, the group slug stays stable unless the team explicitly asks Identity to rename it.

## Adding a new internal app to SSO

To onboard a new internal application:

1. File a ticket in the change tracker with the app name, the team that owns it, and the expected user population.
2. Identity & Access reviews the request and creates an {{IDENTITY_PROVIDER}} app integration. We default to OIDC; SAML only when the app requires it.
3. The requesting team provides the redirect URIs and any service account needs up front.
4. Once the integration is configured, the app owner tests with a small set of users before we roll it to the full group.
5. We add the app to the SSO page and note the owner in the identity runbook.

The requesting team is responsible for keeping their app's redirect URIs current. Identity will flag stale entries during periodic reviews, but we do not actively police every URI.

## Service accounts

Service accounts exist for machine-to-machine auth where interactive SSO is not possible. Each service account must have a named human owner in the identity inventory. The owner is responsible for rotating credentials, keeping the purpose description current, and requesting removal when the account is no longer needed.

When an owner leaves the company, Identity & Access contacts the owner's team lead to assign a new owner. If no one claims the account within a few working days, we disable it and follow up with the team. We do not delete service accounts automatically because some are referenced in pipeline configs that are hard to find.

## SCIM deprovisioning

The HR system pushes joiners, movers, and leavers to the IdP over SCIM. When someone leaves, the HR system marks the end date and the IdP disables the account at the start of the next working day. The deprovisioning flow covers:

- Disabling the {{IDENTITY_PROVIDER}} account and terminating active sessions.
- Removing group memberships.
- Triggering account suspension in connected apps that support SCIM (chat, the helpdesk, the CRM, the email platform).
- Informing the paging tool so on-call schedules drop the leaver.

The full process is described in the joiners, movers and leavers doc. If a leaver's account is needed for a handover, the manager must request a temporary extension before the end date; Identity does not grant extensions retroactively.

## Loose ends

- Some internal tools still use local credentials because they predate SSO. We are tracking those in the identity backlog and asking each owner to migrate on their next major version.
- SCIM coverage for the data warehouse is incomplete; the warehouse team relies on scheduled syncs instead.
- Group sync is near-real-time, but the HR system's export can lag by up to an hour. If someone just moved teams and needs access to a group immediately, ping Identity & Access in #identity and we can trigger a manual sync.
