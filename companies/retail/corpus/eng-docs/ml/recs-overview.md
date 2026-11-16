# Recommendations overview

**Owner:** Machine learning (recommendations)  
**Last edited by:** Aleksander Becker (Data Scientist)

## What we do

The recommendations team builds and maintains the models that power product suggestions across the Mossgrove shop. We serve three main surfaces: the product detail page, the basket page, and the transactional emails sent by mailer after order dispatch. Each surface has its own model, trained on different signals and optimised for slightly different behaviour.

This document is a high-level map of what exists, how it is trained, and how we judge whether a change is an improvement. If you are new to the team or need to understand what "the recs" actually are, start here.

## Models

### Similar items

Serves the "You might also like" block on product detail pages. Inputs are the current product, the customer's session context (category browsing, search terms, items already viewed), and a lightweight customer profile built from order history where available.

The model is a two-tower architecture trained on view-and-buy co-occurrence from the analytics warehouse. We refresh training data nightly from warehouse tables that the data engineering team maintains. The embedding tables are rebuilt on the GPU cluster (see `eng-docs/ml/gpu-lab.md` for capacity and scheduling notes).

Serving happens in-process in orders-web. Latency budget is 50ms p95, which we have been holding comfortably. The feature store used for customer context is the same one used by the checkout team's fraud checks, so we share ownership of that pipeline with them.

### Basket completion

This is the "Customers also bought" panel on the basket page. It is a smaller model, a gradient-boosted tree over basket-level features: item categories, price bands, whether the basket contains a tent or other large item, promo code usage, and a few store-level features (e.g. whether the customer has a store within 15 miles, which we know affects basket composition for bulky items).

We retrain this model on a rolling schedule rather than a fixed cadence. Data comes in continuously from the order event bus (see `eng-docs/adr/0012-event-bus.md`), and we trigger a retrain when the cumulative signal volume since the last retrain crosses a threshold. In practice that has been somewhere between every two and three weeks. The model card on the warehouse catalog has the exact thresholds.

### Email recs

Transactional emails sent by mailer include a "You might also need" section. This uses a rules-based fallback with a light model layer on top. The model scores candidate items from the same category or complementary categories (tent + footprint, stove + gas canister, etc). It is trained on historical email click-through from the warehouse, but because mailer sends are batched and the click stream is delayed, we train this one on a fixed monthly cadence. It is the least critical of the three, and we have occasionally skipped a monthly retrain during busy periods without noticeable impact.

## Training cadence

Summarising the above:

- Similar items: nightly data refresh, embedding rebuild weekly on the GPU cluster, model release via the standard process in `eng-docs/ml/model-release.md`.
- Basket completion: rolling retrain based on signal volume, typically every two to three weeks.
- Email recs: monthly retrain, can slip by a week or two if the team is busy.

All model releases go through the same release checklist and require sign-off from the ML engineering manager (currently Henrik Costa). Releases are scheduled between major trading events and we avoid releasing on the last working day of the week where possible.

## Offline evaluation

We maintain a set of offline evaluation datasets in the warehouse, one per surface. These are held-out windows of historical interaction data, refreshed each quarter. The team uses these to check that a candidate model does not regress on:

- Click-through rate on the surface where it will serve
- Add-to-basket rate after a recommendation is clicked
- Conversion rate for sessions where a recommendation was seen (this one is noisy at the session level, so we look at it over a trailing window)
- Revenue per session, bucketed by whether the session included a recommendation impression

We also run a category-level breakdown so we can catch a model that improves overall metrics but does badly on, say, cookware or garden furniture. That has caught real issues twice in the past year.

The eval harness is a set of jobs run on the GPU cluster; the results are written back to the warehouse and surfaced in the team's dashboard. We do not publish a single "score" anywhere — the dashboard shows the breakdown and the team discusses.

## A/B testing

All three surfaces are behind the feature flag service, and we run A/B tests in production for any change that passes offline eval. Tests are run in partnership with the checkout team, because most of our metrics (add-to-basket, conversion, revenue) are owned by them and they need to schedule their own experiments around ours.

Tests are allocated to a random sample of customers at the browser-session level for the web surfaces. For email recs, the test unit is the individual customer, because mailer sends are per customer and we do not want the same customer seeing different content in the same send. We generally run tests for two full weeks of traffic to reach significance, though busy periods can shorten that because volume is higher.

The checkout team maintains a shared calendar of live tests and we coordinate through #checkout and #ml-recs. We do not launch a test without confirming with Lucia Ahmadi's team that the metrics we care about are not already being moved by one of their experiments. There have been a couple of incidents where two tests were both looking at conversion and neither was conclusive; the shared calendar exists to stop that happening again.

## Wholesale and stores

The recommendations models only serve the online shop (UK, IE, US). We do not serve recommendations in the POS back office or to wholesale customers. That said, the basket completion model does use store proximity as a feature, and the data engineering team has confirmed that the store postcode table in the warehouse is kept current by the stores operations team. We have a standing request with them to be told when they open or close a store, because that changes the feature for customers in that area.

## Known limitations

- The similar items model does poorly on new products with no interaction history. We have a cold-start fallback that uses category-level embeddings, but it is noticeably weaker. The merchandising team knows about this and flags new ranges in #marketing when they need us to look at cold-start behaviour.
- Basket completion tends to recommend high-margin items over high-fit items when both are available. We have not prioritised fixing this, but the checkout team has raised it and we track it.
- Email recs do not account for whether the customer has already purchased the recommended item in a separate order. We filter on order history at the customer level, but the filter has a two-day lag because of warehouse refresh timing. In practice this rarely surfaces because the email goes out within a day of dispatch, but it does happen.

## Related documents

- `eng-docs/ml/model-release.md` — release process for all models
- `eng-docs/ml/gpu-lab.md` — training infrastructure
- `eng-docs/adr/0012-event-bus.md` — order events used for basket completion training data
- `data-docs/catalogue.md` — where to find the evaluation datasets and feature tables
- `eng-docs/web/feature-flags.md` — how tests are rolled out

If something in here is out of date, the right place to flag it is #ml-recs.
