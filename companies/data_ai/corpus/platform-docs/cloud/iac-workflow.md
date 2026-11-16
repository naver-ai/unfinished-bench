# Infrastructure changes with {{IAC_TOOL}}

**Owner:** Cloud platform  
**Last edited by:** Ivan Herrera (Senior Platform Engineer)

This document describes how infrastructure changes move through the infra repository, from branch to production. It covers the {{IAC_TOOL}} workflow only.

## Repository layout

The `infra` repository is organised by cloud account and then by layer:

- `accounts/` — per-account configuration (production, development, shared services)
- `modules/` — reusable {{IAC_TOOL}} modules (networking, compute, storage, IAM)
- `environments/` — environment-specific state configurations and backend definitions
- `scripts/` — helper scripts for state operations and drift handling

State lives in the remote backend configured per environment. Do not initialise {{IAC_TOOL}} locally against production state; the pipeline handles that.

## Opening a PR

1. Branch from the current `main`. Name the branch after the change, e.g. `add-sensor-ingest-queue`.
2. Make your change. Run `{{IAC_TOOL|lower}} fmt` and `{{IAC_TOOL|lower}} validate` locally against the module you touched.
3. Push the branch and open a pull request against `main` in the infra repository.
4. Fill in the PR template. It asks for the change type (new resource, modification, removal), the affected account and environment, and a short description of the impact.
5. Link the corresponding ticket from tickets in the PR description. Infrastructure changes without a linked ticket will not be reviewed.

## Plan output in CI

Every PR triggers a plan job in CI. The job runs `{{IAC_TOOL|lower}} plan` against the relevant environment state and posts the output as a comment on the PR.

- **Green plan** — no changes or only expected changes. Proceed to review.
- **Unexpected changes** — if the plan shows changes to resources you did not intend to touch, stop and investigate. Do not request review until you understand every line of the diff.
- **Plan failure** — if the plan job fails, fix the configuration error and push again. Do not merge with a failing plan.

## Review

At least one reviewer from the Cloud platform team must approve the PR. For changes that touch more than one account, a second reviewer from the platform team is required.

Reviewers check:

- The plan output matches the intent of the change.
- No secrets or account identifiers are hard-coded in the configuration.
- Resource names follow the naming conventions in the repository style guide.
- The change does not conflict with any in-flight work. If two PRs touch the same state, coordinate with the other author.

## Apply

After approval, merge the PR to `main`. The pipeline runs `{{IAC_TOOL|lower}} apply` automatically for the affected environment. The apply job output is visible in the CI logs.

Do not run `{{IAC_TOOL|lower}} apply` locally for production or shared services environments. For development environments, local apply is allowed if the pipeline is unavailable, but you must confirm the state is not locked by another run.

## Drift detection

A nightly job runs `{{IAC_TOOL|lower}} plan` against all environments and posts the results to the #cloud-platform channel. The report lists any resources where the actual cloud configuration differs from what {{IAC_TOOL}} expects.

Read the report as follows:

- **Expected drift** — resources changed manually as part of an incident or a temporary fix. If the change should be permanent, open a PR to update the configuration. If temporary, revert the manual change.
- **Unexpected drift** — resources modified outside of {{IAC_TOOL}} with no record. Investigate and either import the change into configuration or revert it, depending on what the resource is and why it changed.

If the drift report is empty, there is nothing to do.

## Importing hand-made resources

If a resource was created manually in the cloud console (for example during an incident or a quick fix), bring it under {{IAC_TOOL}} management:

1. Add the resource block to the relevant module or environment configuration.
2. Run `{{IAC_TOOL|lower}} import` for that resource using the appropriate state. The command and the exact resource address are shown in the drift report.
3. Run `{{IAC_TOOL|lower}} plan` locally to confirm the imported state matches the configuration. Adjust the configuration if {{IAC_TOOL}} wants to change attributes that should stay as they are.
4. Open a PR with the configuration change and mention in the description that it includes an import.

## If it goes wrong

- **Apply fails mid-run** — the pipeline marks the run failed and leaves the state locked. Resolve the failure and re-run the pipeline job. If the lock does not clear, contact the platform team in #cloud-platform.
- **Resources deleted unintentionally** — do not recreate them manually from memory. Restore from the most recent state backup or, if that is not possible, recreate from the configuration and verify the result against the resource's original purpose.
- **Plan shows a full replacement of a resource that should be updated in place** — stop and check whether the resource has a `lifecycle` block with `create_before_destroy` or `prevent_destroy` set. If not, the configuration change may be forcing replacement; adjust the change rather than letting it proceed.
- **Drift report shows the same unexpected drift for several days** — open a PR to align configuration with reality. Do not leave drift unaddressed for more than a few working days.

For questions about this workflow, ask in #cloud-platform.
