# Code review

Owner: Product engineering · Last edited by Ingrid Holm

## Pull request size

- [ ] Keep PRs small enough that a reviewer can give useful feedback in one sitting. A few hundred lines is a good target; anything over ~800 lines of real change should be split unless there is a reason (mechanical rename, generated code, lockfile bumps).
- [ ] If a PR must be large, say so in the description and suggest how to review it (commit-by-commit, or which files matter most).
- [ ] Prefer stacked or sequential PRs over long-lived branches.

## Approvals

- [ ] Most repos need **one** approval from a maintainer.
- [ ] Infrastructure repos (the {{IAC_TOOL}} repos, `runner-images`, the build farm config) need **two** approvals, one of which should be from the owning team.
- [ ] A PR that touches both product code and infrastructure (for example a service change plus the {{IAC_TOOL}} for its new queue) needs two approvals — the second covers the infra part.
- [ ] Do not merge your own PR unless the repo explicitly allows it (some small internal tools do; product repos do not).
- [ ] If an approval comes with blocking comments, the comments need to be resolved before merge, not just dismissed.

## Turnaround

- [ ] Review requests are triaged within the same working day when the request falls in your team's overlap with the author's site.
- [ ] Lisbon and Portland overlap is limited to the late Lisbon afternoon — use that window for reviews that need a quick back-and-forth.
- [ ] For PRs from the other office, expect a turnaround of one working day. If you will not get to it that day, say so on the PR rather than going silent.
- [ ] Use draft PRs for work that is not ready for review. A draft signals "do not spend time on this yet" and resets expectations on turnaround.
- [ ] If you are the author and a review is blocking your next step, nudge once in #engineering after a working day, then escalate to the owning team's lead.

## Nit etiquette

- [ ] Prefix trivial comments with `nit:` so the author knows they can address them without a round-trip.
- [ ] Do not block a merge on nits. Batch them into a follow-up if the author prefers.
- [ ] Style nits that are not enforced by the linter are still worth raising, but do not ask for a re-review just for those.
- [ ] If you leave more than a handful of nits, call that out explicitly so the author can decide how to handle them.

## Code owners

- [ ] Respect `CODEOWNERS`. The listed owners must approve changes to their paths even if the repo already has the required number of approvals.
- [ ] For cross-team changes, ask the owning team before opening the PR if the change is non-trivial — a CODEOWNERS approval is easier when the team already knows the change is coming.
- [ ] If a code owner is out for a few days, mention it on the PR and ask the team's lead to cover, rather than waiting silently.
