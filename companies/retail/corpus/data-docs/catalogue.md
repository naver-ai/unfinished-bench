# Data catalogue (short)

Owner: Data engineering · Last edited by Karim Obi

This catalogue lists the main datasets held in the analytics warehouse and the systems that feed them. It is not exhaustive — if you are looking for something not listed here, ask in #data-eng.

## Core datasets

| Dataset | Source system(s) | Owner | Classification | Notes |
|---|---|---|---|---|
| Orders | checkout, orders-web, POS back office, wholesale | Checkout / Retail ops / Wholesale (by channel) | Internal | Order lines carry channel, store ID where applicable, and promo codes. Wholesale orders arrive via the wholesale portal and are flagged as such. |
| Customers | CRM, checkout (guest orders) | CRM team | Confidential | Includes marketing consent flags synced from the CRM. Guest orders are matched post-purchase where possible; unmatched guests stay as order-only records. |
| Loyalty | Membership & billing (loyalty service) | Membership & billing | Confidential | Points balances, tiers, and redemptions. Store staff view this through the POS back office; data lands in the warehouse on a batch. |
| Stock | POS back office, warehouse management, wholesale | Retail ops / Wholesale | Internal | Stock on hand per SKU per location, plus inbound/outbound movements. The warehouse feed is the authoritative source for DC stock. |
| Web events | shop-web, orders-web (via the event bus) | Data engineering | Internal | Page views, product interactions, basket actions, checkout steps. Sessionised in the warehouse; raw events are kept in the log tiers per the retention schedule. |

## Supporting datasets

| Dataset | Source system(s) | Owner | Classification | Notes |
|---|---|---|---|---|
| Gift cards | Gift card platform (via billing-api) | Payments platform | Internal | Balances and redemptions. The finance team reconciles against the gift card liability account each month. |
| Refunds & chargebacks | checkout, payments platform, disputes | Payments platform / Finance ops | Internal | Refund events and chargeback disputes are joined on the payment reference. Dispute outcomes are updated by the disputes team. |
| Wholesale credit | Credit control (the ledger) | Credit control (wholesale) | Internal | Credit limits, ageing buckets, and payment allocations. Shared with the wholesale team through sharectl for the quarterly review. |
| Marketing campaigns | Marketing platforms, mailer | Marketing / Data engineering | Internal | Campaign sends, opens, clicks, and unsubscribe events. Consent state is pulled from the CRM at send time. |

## Notes on access

- Confidential datasets require a business justification and are reviewed at the quarterly access review. Requests go through the helpdesk.
- Web events are pseudonymised at the edge where the raw event contains personal data (for example, account email on checkout steps).
- The warehouse is the place to query anything listed above. Do not connect directly to source systems for reporting — see `data-docs/sharing.md` for the rules on moving data out of the warehouse.
- For questions about a specific dataset, the team named as owner is the first point of contact. Data engineering can help with joins and lineage.

## Maintenance

This catalogue is updated when a new dataset is added to the warehouse or when ownership/classification changes. If you spot something stale, raise it in #data-eng and one of us will fix it. Full field-level documentation lives in the warehouse metadata; this page is intended as a quick reference.
