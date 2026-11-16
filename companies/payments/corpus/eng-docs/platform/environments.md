# Environments

**Owner:** Infrastructure · **Last edited by:** Lena Voss

This document covers the environments we run code in, what each one is for, and who deploys to it. If you need to know which environment a given service is running in, check the service's entry in deployctl or ask in #platform.

## Overview

| Environment | Purpose | Who deploys | Data |
| --- | --- | --- | --- |
| dev | Local development and early integration work | Anyone (via deployctl, no approval) | Synthetic only |
| staging | Pre-production validation, integration testing, release rehearsal | Engineering teams (via deployctl, change required for infra-affecting changes) | Masked production data |
| merchant test | External-facing test environment for merchants and partners | Merchant payments, Partner integrations | Synthetic merchant data |
| production (EU) | Live traffic for EU/EMEA merchants | Engineering teams (via deployctl, change required) | Production |
| production (US) | Live traffic for US merchants (sponsor bank programme) | Engineering teams (via deployctl, change required) | Production |

Both production regions run the same core services: the core ledger, payments bus, merchant dashboard, back office, treasury workstation, and the transaction monitoring system. Both regions are run by the engineering teams in Dublin and Vilnius. A small number of services are EU-only — check the service registry in the back office if you're unsure.

## Staging data

Staging runs against a copy of production data that has been through the masking pipeline. The masking job runs from the analytics warehouse and produces a fresh snapshot on a weekly cadence. If you need a more recent slice for a specific test, ask in #data-lake and the ingestion team can trigger a one-off refresh.

The one thing to remember: masked data is still derived from production, so treat it with the same care you would production data. Don't copy it to your laptop, don't put it in a public repo, and don't use it to demonstrate anything outside Kilbarra.

## Merchant test environment

The merchant test environment is the one external merchants and partners hit when they're integrating. It sits behind the same edge as production (separate hostnames). API keys issued for the test environment are clearly labelled — don't reuse a production key there, and don't let a test key near production.

The merchant test environment runs a slightly older release than staging. It gets updated on the release train, but not always on the same day as staging. If a merchant reports something that looks like a regression, check which build is actually live there before assuming it's a production issue.

## Deploying

Most teams deploy to staging and production themselves using deployctl. The general rule:

- **Staging:** no approval needed for application code; network and DNS changes are raised with Infrastructure as a ticket.
- **Production:** a change record is required for all deploys. The change record must name the environment (EU, US, or both) and the expected impact window.
- **Merchant test:** deploys are done by the Merchant payments team. If you need something deployed there outside the normal release train, ask in #payments-dev.

The release train is documented in `eng-docs/dev/release-train.md`. Merging rules are in `eng-docs/dev/merging.md`.

## Notes

- The US production region was added after the EU region, and a few internal tools are still EU-only. The merchant dashboard and the back office are fully regional; the core ledger is regional too. If you're building something new that needs to be available in both regions, plan for it from the start.
- The old staging environment used to run off a nightly dump restored straight into the database. That was retired a while back — if you see a runbook referencing "staging restore" or "staging refresh" that isn't the masking pipeline, it's stale and should be ignored.
- For DNS and merchant custom domains, see `eng-docs/platform/dns-and-domains.md`; internal certificates are covered in `security-docs/pki/ca-overview.md`. The on-call guide in `eng-docs/oncall/oncall-guide.md` has the list of who to page for environment issues.
