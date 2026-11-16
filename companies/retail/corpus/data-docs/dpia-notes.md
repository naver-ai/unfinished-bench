# DPIA notes

Owner: Legal. Last edited by Grace Harper (Paralegal).

These notes track when a data protection impact assessment is needed and record the outcome of recent DPIAs. If you're unsure whether a project or change needs one, talk to Legal before you go too far down the build path.

## When we need a DPIA

We run a DPIA when a project involves:

- Large-scale processing of customer personal data, especially purchase history or behavioural data
- New ways of combining datasets that weren't designed to be joined
- Profiling or automated decision-making that affects individuals
- Processing of special category data (we don't do much of this, but it comes up occasionally in HR projects)
- New technology that processes personal data in a way we haven't done before
- Sharing personal data with a new external party

The GDPR says we should assess whether the processing is "likely to result in a high risk" — if in doubt, ask. It's much cheaper to do the assessment early than to unwind something after launch.

The DPO is contracted through our external provider. Contact Grace Harper in Legal and she'll route it to the DPO. For urgent queries, the DPO has office hours once a week — check the Legal channel for the current slot.

## Recent DPIAs

### Recs personalisation (ml-recs) — completed

The recommendations team wanted to start using order history plus browsing events from the analytics warehouse to personalise the storefront product carousels. This joined data from orders-web and the event bus that hadn't been combined at individual customer level before.

What we decided:

- Legal signed off with conditions. The main one was that we only use order history and browsing events for customers who haven't opted out of personalisation in the CRM.
- The ml-recs team had to document the retention period for the training data — they went with 13 months, aligned with the warehouse retention.
- We required a review after the first quarter of production traffic to check the opt-out rate and whether any customers were contacting support about the recommendations.

Outstanding items:

- The ml-recs team still owe us a note on whether they're using any third-party enrichment data. That was meant to land with the quarterly review but hasn't shown up yet.

### CRM sync — completed

The CRM team wanted to sync customer records from the shop databases into the CRM on a continuous basis (previously it was a nightly batch via sharectl).

What we decided:

- Fine to proceed — the data is the same as the batch sync, just more frequent. No new categories of data.
- We asked the CRM team to confirm the sync doesn't pull in any payment card data. They confirmed billing-api only exposes token references, not PANs.
- Noted that the sync includes customers from the wholesale arm (contacts at independent shops and garden centres). Those are business contacts for the most part, so lower risk, but the CRM team needs to keep the two populations distinguishable because the lawful basis is different.

Outstanding items:

- The CRM sync DPIA references the old data catalogue (data-docs/catalogue.md) which was fine at the time but the catalogue has been reorganised since. The reference may be stale.
- Zainab was the AP contact on the original supplier onboarding for the CRM vendor — she's since moved to the accounts payable team so the name on the record is outdated.

## Loose ends / things we keep meaning to tidy

- We should write up a short note on when a DPIA is needed for changes to the store loyalty programme (if it ever comes back). It's been kicked around a couple of times but never went anywhere.
- The DPIA register lives in the Legal shared drive; Grace maintains it. Ask her if you need to see what's in progress.
- A few DPIAs from the Columbus office (US e-commerce) were done under the old US entity name before the restructure. Those are still valid but could do with a re-issue under the current entity. Not urgent.
