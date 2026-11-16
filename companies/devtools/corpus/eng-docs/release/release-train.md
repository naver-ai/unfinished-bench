# Release train

Owner: Release engineering & CI · Last edited by Zainab Bauer

This document describes how changes to Gantline Cloud reach production. It covers the daily train, canary rollout, rollback, and the release captain rota. If you are looking for how individual services are built and packaged, see [builds and runtimes](builds-and-runtimes.md).

## Merge to main

1. All changes land on `main` through pull requests. CI runs the full build, unit tests, and the security scanner stage on every PR. A green PR can be merged by its author or a reviewer.
2. Merging to `main` does **not** deploy anything by itself. A merge only updates the source tree and triggers the daily train's build inputs.
3. If a PR is urgent and the train has already been cut, do not merge it and hope. Talk to the release captain (see below) — they can decide whether to hold the train or let it go without your change.
4. Fixes to a broken `main` are the exception. If `main` is red, the owning team is expected to revert or fix within the working day. The release captain can pause the train if `main` stays red past the cut-off.

## The daily train

1. The train runs once a day, shortly after the end of the Lisbon working day. The exact time is announced in #releases each morning; it shifts a little depending on public holidays in Portugal or the US.
2. The train picks up the current `main` head at the cut-off. Commits merged after the cut-off wait for the next train.
3. The train builds all deployable services, runs the integration suite against a fresh staging environment, and produces a single build manifest. The manifest records every service's commit SHA and artifact digest. A service that fails to build is left out of that train's manifest and keeps running its last good build; the rest of the train goes ahead.
4. The build manifest is stored with the artifacts in the CI artifact store (`infra-docs/ci/artifact-store.md`). The manifest name is the train ID, which is an incrementing number plus the short `main` SHA (for example, `train-4821-9f3c2a1`).
5. If the integration suite fails, the train stops. The release captain works with the owning team to fix or revert. The train is re-run once the fix is on `main`.
6. When the train is green, the release captain promotes the manifest to the canary region.

## Canary and rollout

1. The canary region is the US region (Oregon). All services in the manifest are deployed there first.
2. The rollout is automated: `gnt deploy promote --train <train-id> --region us` from the release captain's machine, or from the admin console under **Releases → Promote**. Both paths require the captain's SSO session and a second factor.
3. After promotion, the captain watches the rollout. The dashboard set is the "Release train" dashboard group in the metrics dashboards: error rate, p95 latency, queue depth, and pod restart count per service, plus the top-level customer-facing availability panel.
4. The canary window is at least one hour. During that hour, the captain keeps #releases updated with a short status line. If nothing looks wrong, the captain promotes to the EU region (Frankfurt), which gets its own one-hour window.
5. The EU promotion does **not** have to wait for the full US window if the dashboards are clean after the first half hour, but the two regions are never promoted at the same time.
6. The full rollout across both regions takes a couple of hours. The captain stays contactable during the rollout, but does not need to watch the dashboards continuously after the first region — the paging tool will alert on the core SLOs. The captain checks in at least every couple of hours.
7. When the last region is live, the captain marks the train as **complete** in the admin console. That clears the train for the next day and updates the status page's "current build" field.

## If it goes wrong

1. If a dashboard shows a sustained error-rate increase or latency degradation in the canary region, the captain's first action is to roll back to the previous build: `gnt deploy rollback --train <train-id> --region us`. This restores the previous manifest's artifacts for all services in that region.
2. Rollback is the default response. Do not try to debug in the canary region while it is broken — roll back first, then investigate with the owning team.
3. If the problem only shows up in the EU region, roll back that region the same way. The captain then decides whether to roll the US region back too — the right call if the issue looks like it will affect both.
4. After a rollback, the captain posts a summary in #incidents with the train ID, the region, the symptom, and the rollback time. The owning team opens a follow-up ticket and works on a fix for the next train.
5. A rolled-back train is **not** re-promoted. The fix goes through the normal PR and train cycle.
6. If the rollback command fails (for example, the previous manifest is unavailable), the captain pages the on-call engineer for Release engineering & CI. The on-call engineer can promote the previous manifest manually from the admin console.

## Merge freezes

1. The release captain declares a merge freeze when a company event makes a broken deploy especially costly: the quarterly product launch, the first working day of the fiscal year, and the days around the company all-hands. The freeze list is posted in #releases at least a couple of working days ahead.
2. During a freeze, merges to `main` are blocked by a branch protection rule. The release captain can lift the block for an individual PR if the change is a revert or a fix to something already broken.
3. Freezes do not stop the train. The train still runs, but the expectation is that it will be a low-risk train — mostly dependency bumps and docs. If a freeze day's train fails, the captain rolls back and does not expect a fix until the freeze lifts.

## Release captain rota

1. The release captain is a rotating duty in Release engineering & CI. The rota lives in the team calendar and covers every working day. Each shift starts at the beginning of the working day and ends when the day's train is complete.
2. The captain's duties: confirm the train cut-off, watch the canary window, promote regions, roll back if needed, and post status in #releases. The captain is also the first point of contact for "can we get this in today?" questions — the answer is usually "it goes on the next train".
3. If the captain is unavailable (sick, off-site), they swap with another member of the team. The swap is recorded in the team calendar. If no swap is possible, the on-call engineer for Release engineering & CI covers the captain duties.
4. The rota is published at the start of each month in #releases. Anyone outside Release engineering & CI who needs to know the captain for a given day can ask in #releases or check the team calendar.
