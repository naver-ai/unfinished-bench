# Testing

Owner: Quality engineering. Last edited by Kasia Olsen.

## Unit and integration tests

- Every service in `eng-docs/services/service-catalogue.md` keeps its unit tests in the same repo as the service. Integration tests live under `internal/tests/` in each repo.
- The CI pipeline runs unit and integration tests on every branch push. The nightly builds run the full set against a fresh database clone.
- Services that touch billing or identity must also run the contract tests against `billing-service` and the identity service. Those tests live in the `contract-tests` repo.
- Coverage is not enforced centrally, but the quality team reviews coverage diffs on PRs that touch core paths (auth, billing, workspace creation, runner allocation).

## End-to-end suite

- The e2e suite runs against staging. It exercises the web editor, the desktop editor, the mobile apps, and the public API.
- E2E runs are triggered on every merge to the main branch of the web app, the editor, and the API gateway. They also run nightly for the mobile release train.
- The suite is split by area so a failure in one area doesn't block the rest. Results land in `#engineering` and in the metrics dashboard.
- If the e2e suite is red at the end of the working day, the owning team is expected to triage before the next morning. If it's still red after two consecutive runs, the paging tool pages the on-call engineer for that area.

## Flaky test quarantine

- Any test that fails intermittently gets quarantined. Move it to the `flaky` build tag and add a comment with the ticket number and the suspected cause.
- Quarantined tests do not run in CI or nightly builds. They run once a week in a dedicated job.
- Each week, the quality team publishes the flaky-test report to `#engineering`. The report lists quarantined tests, how many times each one failed, and who owns the fix.
- A quarantined test stays quarantined until the fix is merged and the test has passed in three consecutive weekly runs.
- The weekly report is also used to spot patterns — e.g. tests that only fail on the Portland build hosts or only in the EU region.

## Soak runs for desktop editor

- The desktop editor build gets a long soak run on the lab hypervisors before each release candidate is cut.
- The soak run keeps the editor open with a realistic workspace loaded, and exercises autocomplete, search, and the git panel on a loop.
- Soak runs last at least 36 hours. The lab team holds the VM leases for the duration; see `infra-docs/lab/vm-leases.md`.
- Memory, CPU, and disk usage are recorded to the metrics dashboards. If the editor leaks or degrades during the soak, the release is blocked and the editor team gets the failure report.
- The soak run uses release builds only, not debug builds.
