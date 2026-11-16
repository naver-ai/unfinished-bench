# Vulnerability management

Owner: Security engineering. Last edited by Kasia Vogel.

This page covers how we find and fix vulnerabilities across Mossgrove systems. If you're not sure whether something counts as a vulnerability, ask in #security rather than sitting on it.

## Scanners

- **CI scanner**: Every pull request that touches code in the main repos (orders-web, shop-web, checkout, the POS back office, data pipelines) runs the static scanner and dependency check. The scanner runs on the merge commit, not just the branch head. If a PR introduces a new finding, the build fails and the PR cannot merge.
- **Container images**: Images pushed to the registry are scanned at push time. Findings at critical or high level block promotion to production. Medium and low findings are logged and tracked in the security backlog.
- **Infrastructure**: The platform team runs a weekly scan of our cloud accounts, including the warehouse, the GPU lab cluster, and the Wakefield DC internal tools. Findings are imported into the same tracker as the CI scanner.

Severity ratings follow the CVSS v3.1 reference, adjusted where the exposure is internal-only or where compensating controls already exist. If you disagree with a rating, raise it in the tracker and tag Security engineering.

## Severity SLAs

| Severity | Time to first response | Time to fix (fix available) | Notes |
| --- | --- | --- | --- |
| Critical | 4 working hours | 2 working days | Fix can be a rollback or disabling the affected feature via the feature flag service. |
| High | 1 working day | 5 working days | |
| Medium | 2 working days | 30 calendar days | |
| Low | 5 working days | Next quarterly review | |

Time to first response starts when the finding is assigned to a team. If the finding is in a library or dependency that no one owns, Security engineering will assign an owner from the team that uses it most.

For production incidents caused by an exploited vulnerability, follow the incident process in `eng-docs/oncall/incident-process.md` first, then come back to the SLA clock.

## Exceptions

If a vulnerability cannot be fixed within the SLA, the owning team can request an exception. Exceptions are tracked in the tickets system and must include:

- The finding ID and severity
- Why the fix can't be done in time (e.g. upstream dependency not yet patched, store hardware refresh cycle)
- What we're doing to reduce exposure in the meantime (network restriction, manual review, disabled feature)
- A review date, which cannot be more than 90 days out

Exceptions are approved by a member of Security engineering. They expire on the review date unless they are renewed. Renewal requires a new request; the previous request does not carry over automatically. When an exception expires, the original finding is re-opened at the same severity and the SLA clock restarts.

## Penetration testing

We run an external penetration test twice a year against the main customer-facing properties: shop-web, orders-web, the checkout flow, and the membership area. The test is coordinated by Security engineering and covers both the UK/IE and US storefronts.

The wholesale ordering portal and the POS back office are tested once a year, usually in the same engagement as the main test but scoped separately. If a test uncovers findings, they are tracked in the same system as scanner findings and follow the same SLAs.

Occasionally we run a smaller, targeted test against a specific feature (for example, when the gift card flow changed, or before a new payment provider integration goes live). Security engineering will announce these in #security ahead of time so teams know to expect traffic from the test provider.

## Old stuff

The scanner used to be a separate {{CI_SERVER}} job that ran nightly and emailed a report to #security. That job was retired when the CI scanner was added. If you see references to "nightly scan" in old tickets or runbooks, that's what it refers to. The current scanner output lives in the security tracker, and the dashboard link is pinned in #security.
