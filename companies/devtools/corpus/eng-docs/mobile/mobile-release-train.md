# Mobile release train

**Owner:** Mobile apps  
**Last edited by:** Otto Reyes (Mobile Platform Engineer)

This covers the cadence and mechanics for shipping the Gantline mobile apps ({{MOBILE_OS_1}} and {{MOBILE_OS_2}}) to the {{APP_STORE_1}} and {{APP_STORE_2}}. It applies to the main Gantline app; other mobile properties follow their own release notes in their repos.

## Cadence

- We ship a release every two weeks, alternating platforms: {{MOBILE_OS_1}} one cycle, {{MOBILE_OS_2}} the next, so each store sees a submission every four weeks.
- The release train departs on the first working day of the cycle. Cutoff for code merges is mid-afternoon Portland time on that day.
- Store review times vary; we do not hold the train for review. If a store is slow, the next cycle still departs on schedule.

## Release branches

- Cut `release/{{MOBILE_OS_1|lower}}/<version>` and `release/{{MOBILE_OS_2|lower}}/<version>` from `main` at cutoff.
- Version numbers follow [eng-docs/release/versioning.md](../release/versioning.md). The mobile repos use the same scheme as backend services: MAJOR.MINOR.PATCH, with PATCH incremented for hotfixes.
- After the cut, only fixes the release captain agrees to (or the engineering manager, if the captain is out) go into the release branch. Everything else waits for the next train.

## Builds

- Release builds are triggered from the release branch by the release pipeline (`.gnt/pipelines/release.yml` in each mobile repo), on the `{{DESKTOP_OS_1|lower}}-{{MOBILE_OS_1|lower}}` pool for {{MOBILE_OS_1}} and `{{DESKTOP_OS_3|lower}}-large` for {{MOBILE_OS_2}}. The build produces:
  - {{MOBILE_OS_1}}: an `.ipa` via `gnt build {{MOBILE_OS_1|lower}} --release`
  - {{MOBILE_OS_2}}: an `.aab` via `gnt build {{MOBILE_OS_2|lower}} --release`
- Upload to the stores is done from the build artifacts. Use the `gnt mobile upload` command with the store credentials from the password manager — never paste API keys into chat or tickets.
- After upload, submit for review in the store consoles.

## Store review and phased rollout

- {{MOBILE_OS_1}}: submit for review immediately. Once approved, start a phased rollout at 10% on the first working day after approval, then 25%, 50%, and 100% on successive working days. You can accelerate if the metrics look clean, but do not skip steps.
- {{MOBILE_OS_2}}: use staged rollout in the Play Console: 10% → 25% → 50% → 100% on the same cadence.
- If a phased rollout is paused or rolled back, the release captain notes it in the release channel and opens a ticket with the outcome.

## Release captain

- The release captain is rotated each cycle. The roster lives in the Mobile apps team calendar; Otto maintains it.
- The captain is responsible for:
  - announcing the cutoff in #mobile
  - cutting the branch and triggering the build
  - watching the build and store submissions
  - moving the phased rollout along
  - posting updates to #releases when the build is submitted and when it reaches 100%

## Hotfixes

- For a critical issue in a shipped version, cut `release/hotfix/<platform>/<version>` from the release branch, not from `main`.
- The hotfix goes through the same build and submission steps as a regular release, but the phased rollout can start at 25% to get it out faster.
- Hotfixes do not change the versioning scheme; bump PATCH and continue.

## If it goes wrong

- **Build fails at cutoff:** fix forward on the release branch if the fix is small and safe, otherwise slip the release to the next cycle and announce in #releases.
- **Store rejection:** read the rejection reason, address it in the release branch, and resubmit. Do not argue with the store reviewer in the first pass; if the rejection looks like a misunderstanding, escalate through the engineering manager.
- **Crash spike during rollout:** pause the rollout immediately, roll back to the previous version in the store console, and open an incident ticket. The release captain coordinates the hotfix.
- **Credentials or signing issues:** stop the release, contact #it-help for credential rotation, and resume once the password manager entries are updated. Never share secrets in chat.

For anything not covered here, ask in #mobile or #releases.
