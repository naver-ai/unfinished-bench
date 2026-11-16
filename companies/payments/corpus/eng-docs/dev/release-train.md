# Release train

**Owner:** Developer platform & releases  
**Last edited by:** Olivier Moreau (Engineering Manager, Developer Platform)

The release train carries the mobile app and the settlement-side services (payouts, reconciliation, treasury sync). Everything else deploys continuously from `main` via deployctl and is not subject to the train calendar.

## Train calendar

The train leaves once a week. The cut is at mid-afternoon Dublin time on the day before the train ships; anything merged after the cut waits for the following week.

| Working day | Activity |
|---|---|
| WD+1 | Cut for the next train. Release notes drafted from merged PRs. |
| WD+2 | Train ships to production. Rollout is staggered by region: EU first, then US. |
| WD+3 | Buffer for hotfixes. If a hotfix is needed, it ships on the same train only if the release manager approves. |

If WD+2 is a bank holiday in Ireland, the train ships on the next working day and the cut moves with it. Check the #platform calendar for the exact dates each quarter.

## What rides the train

| Service | Where it builds | Notes |
|---|---|---|
| Mobile app (merchant dashboard) | `mobile-app` pipeline | Requires sign-off from merchant success before the cut. |
| Payouts service | `payouts` pipeline | Depends on the treasury workstation cut-off for the day. |
| Reconciliation sync | `recon-sync` pipeline | Must be paired with the matching `batch-reconciler` release. |
| Treasury sync | `treasury-sync` pipeline | Coordinate with treasury ops on the #treasury-ops channel. |

## Getting a change on the train

1. Merge to `main` before the cut. The train picks up whatever is on `main` at the cut time; there is no cherry-picking onto the train after the cut.
2. Make sure CI is green on your merge. The build engineer on call (Abel or Aiko) can help if a CI step is flaky.
3. For the mobile app, confirm the merchant success review is done and the approval is recorded in tickets.

If your change misses the cut, it waits for the next train. There is no ad-hoc train for late changes; the WD+3 hotfix slot is only for defects that are actively affecting production.

## Continuous deployment

Services not listed above ship continuously through deployctl. This includes all payments-bus consumers, edge services, and internal tooling. If a service is not on the train table, do not hold it for the train calendar — deploy it when it is ready.

## Questions

Ask in #platform or #payments-platform. Release train status and the current train's contents are posted in #platform after each cut.
