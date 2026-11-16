# Deploying with deployctl

Owner: Developer platform & releases | Last edited by: Theo Bishop

## Overview

`deployctl` is the tool for pushing builds through our environments. All deploys to production start with a canary and progress automatically unless you pause them. This page covers the basics; for the full command reference run `deployctl --help` or see the man page on any build host.

## Environments

Deploys go through `dev`, `staging`, then `prod`. Each environment has its own namespace in deployctl. You can see what is currently running with:

```
deployctl status
```

This shows the deployed build IDs per service per environment, plus whether a rollout is in progress.

## Starting a deploy

1. Make sure the build you want is available in the artifact store. Builds are tagged with the branch name and the commit SHA. If you just merged to `main`, the tag is `main-<sha>`.
2. Start the deploy:

   ```
   deployctl deploy <service> --env prod --build main-<sha>
   ```

3. deployctl will promote the build through each environment. By default it waits for health checks to pass in `dev` before moving to `staging`, and then to `prod`.
4. In `prod`, the rollout starts at the canary percentage configured for the service group (see below). If the canary is healthy for the observation window, deployctl automatically scales up to 100%.

## Canary percentage

Canary percentages are set per service group in the `deployctl.yaml` file at the root of the service repo. Most services default to 5%. Higher-risk services (anything touching the core ledger or the payments bus) default to 2%. You can override the canary for a single deploy:

```
deployctl deploy <service> --env prod --build main-<sha> --canary 10
```

Do not raise the canary above 25% without talking to the SRE team first.

## Watching a rollout

Use:

```
deployctl watch <service> --env prod
```

This shows a progress bar with the percentage of instances on the new build. It exits when the rollout completes. If you need to leave the terminal, the rollout continues in the background — you can always attach again with `deployctl watch`.

## Rolling back

If a deploy is misbehaving:

1. Roll back to the previous build:

   ```
   deployctl rollback <service> --env prod
   ```

2. deployctl will immediately route traffic back to the previous build ID and then revert the remaining instances.

Rollback is nearly always faster than fixing forward. If you are unsure whether to roll back, roll back. You can always redeploy once the fix is in.

## Deploy windows

Deploy windows are applied per service group and enforced by deployctl. The main groups:

- **Payments-core** (core ledger, payments bus, treasury workstation): deploys are limited to working days, between the start of the Dublin business day and mid-afternoon Dublin time. No deploys during the daily reconciliation window.
- **Edge** (edge gateways): any time.
- **Everything else**: any time.

If you need to deploy outside the window for a service group, ask on #sre; the SRE on call can agree it, and you then pass `--override-window`.

## Where deploy logs go

Each deploy writes a log entry to the `deployctl` log stream, which lands in the analytics warehouse under `deploy.events`. The log includes the operator, the service, the build IDs before and after, the canary percentage, and the outcome. If you need to investigate a failed rollout, query that table or ask in #dev-platform and someone can pull the relevant events for you.

## If it goes wrong

- If the canary fails health checks, deployctl pauses the rollout automatically. You will see a red banner in `deployctl status`. Fix the issue or roll back — the rollout will not resume on its own.
- If a rollback also fails, stop the rollout with `deployctl abort <service> --env prod` and page the SRE team via the paging tool.
- For anything that looks like a bad build rather than a bad config, check the build logs in the artifact store before redeploying. A build that fails in `prod` but passed in `staging` usually means a config difference between environments — check the feature flag service first.
