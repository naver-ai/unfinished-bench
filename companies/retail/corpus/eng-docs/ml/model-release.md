# Releasing a recs model

**Owner:** Machine learning (recommendations)  
**Last edited by:** Aleksander Becker (Data Scientist)

This page covers the steps for taking a trained recs model from the GPU lab through to live traffic. It applies to catalogue, home page and basket recommendations.

## Offline metrics bar

- [ ] Run the offline evaluation on the candidate against the current live model using the standard eval set (last full week of orders, filtered to signed-in users).
- [ ] Check the headline metrics: recall@20, NDCG@10, and revenue lift on the holdout set.
- [ ] Candidate must beat the live model on revenue lift by at least 0.5 percentage points, and must not regress recall@20 by more than 1 point.
- [ ] If the candidate is a re-train of the same architecture with new data, a smaller bar applies — discuss with Henrik before starting.
- [ ] Log the eval outputs in the ml-recs channel and link the job ID from jobctl.

## Shadow period

- [ ] Deploy the candidate as a shadow model via the recs service config. Use the `rec-shadow` flag in the model registry entry.
- [ ] Run shadow for a minimum of two full trading days, covering at least one non-weekday for the UK store estate.
- [ ] Compare shadow output vs live on a daily basis: click-through, add-to-basket, and order conversion for users who saw both.
- [ ] Watch for any obvious skew — if the shadow model is recommending mostly clearance lines or a single category, stop and talk to Salma before proceeding.
- [ ] Export the comparison table to the warehouse and paste the link in the model release thread.

## Canary

- [ ] Open a change ticket in tickets with the model version, shadow results, and the planned canary percentage.
- [ ] Start canary at 5% of UK and IE web traffic. US traffic is handled separately — co-ordinate with the Columbus team via the #ml-recs channel.
- [ ] Monitor the canary for at least one working day before increasing.
- [ ] Increase to 25% if metrics are flat or better. Hold at 25% for another working day.
- [ ] At 25%, check the stores-facing feed too — the POS back office uses the same model output for till-side suggestions.

## Full rollout and rollback

- [ ] After the 25% hold, promote to 100% for the region. Update the model registry and mark the previous model as archived.
- [ ] If anything looks wrong at any stage, flip the model registry back to the previous version — this is a config change and does not need a new deploy.
- [ ] Rollback is instant: the recs service picks up the registry change on its next refresh (under a minute). Do not attempt to redeploy the old binary.
- [ ] After 100% rollout, close the change ticket and post a summary in #ml-recs with the canary numbers.

## Sign-off

- [ ] Get sign-off from Henrik (ML Engineering Manager) on the offline metrics and shadow comparison.
- [ ] Get sign-off from the product manager for the surface (home page, basket, or catalogue) — Harriet for membership-related surfaces, otherwise the web product team.
- [ ] Attach both sign-offs to the change ticket before the 100% step.

## Notes

- Wholesale customers do not receive model-generated recommendations — their ordering portal uses the manual catalogue ordering flow.
- The US site runs on a separate model instance; do not assume UK metrics will carry over. The shadow period for US runs on a shorter cycle — see the US release notes in the data-docs catalogue.
- For anything that goes wrong during a release, the on-call guide covers the first steps.
