# Merchant risk ratings

**Owner:** Risk controls  
**Last edited by:** Tessa Nakamura (Risk Analyst)

## Rating factors

Merchant ratings are assigned from a combination of factors at onboarding and reviewed on a rolling basis. The core factors are:

| Factor | Notes |
|---|---|
| MCC | High-risk categories (e.g. gambling, crypto, adult) map to a higher starting rating regardless of other factors |
| Country | Jurisdiction risk tier from the KYB onboarding tool; high-risk jurisdictions cap the rating at B+ |
| Volume | Projected and actual monthly processed volume; volume bands are reviewed at each rating refresh |
| Chargeback ratio | 90-day rolling chargeback rate as reported by the card schemes |
| Refund ratio | 90-day rolling refund rate from the core ledger |
| Delivery lag | For goods and services merchants, the median time between payment and fulfilment confirmation |

Volume and ratio data are pulled from the analytics warehouse via the standard monthly rating refresh. Chargeback data comes from the transaction monitoring system.

## Ratings

| Rating | Meaning | Review frequency |
|---|---|---|
| A | Low risk; established history, stable ratios | Each quarter |
| B+ | Acceptable risk; minor watch items | Each quarter |
| B | Elevated risk; requires closer monitoring | Monthly |
| C | High risk; active management required | Monthly, plus weekly check by the assigned Risk Analyst |

C-rated merchants are also looked at by the Risk Controls Lead each month. B-rated merchants are reviewed at each monthly refresh and any material change in the factors above triggers an immediate re-rating.

## Monitoring dashboards

The Risk controls team maintains two dashboards in the analytics warehouse:

- **Rating overview** — current rating by merchant, with the underlying factor values and the last review date.
- **Rating drift** — merchants whose factor values have moved toward the next rating boundary since their last review.

Drift is checked at each monthly refresh. Merchants that cross a boundary are flagged for re-rating before the next scheduled review. The dashboards pull from the same warehouse views used for the monthly refresh, so there is no manual reconciliation.

## Re-rating during the quarter

If an event occurs that changes a factor materially — a chargeback spike, a change in the merchant's processing profile, or a new KYB finding — the assigned Risk Analyst re-rates the merchant outside the normal cadence. Re-ratings are recorded in the case tool with the reason and the factor that changed. The merchant's rating is visible in the back office.
