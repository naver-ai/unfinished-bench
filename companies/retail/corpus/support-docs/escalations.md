# Escalations

Owner: Customer support · Last edited by Oskar Pereira (Customer Support Advisor)

This page covers when to escalate a ticket from the support queues, who to pull in, and how quickly we need to move. If in doubt, escalate — it's easier to step a ticket back down than to unpick a delay.

## Escalation paths

| Trigger | Escalate to | How | Response target |
|---|---|---|---|
| Customer threatens legal action, posts about us on social media, or a complaint is marked as a "serious complaint" | Team lead (Imani or Renata if Imani is away) | Tag the ticket in the CRM and message the lead directly in chat | Same working day |
| Customer is disputing a charge with their bank or card issuer | Disputes team | Move the ticket to the disputes queue in the helpdesk and note it in #disputes | By end of the working day |
| Order not arriving, tracking shows delivered but customer disputes, or a carrier says "left with neighbour" and the customer denies it | Stores team (for click-and-collect or store delivery) | Assign the ticket to the relevant store in the POS back office and ping #stores-ops | Same working day for stores; otherwise WD+1 |
| Wholesale account query about credit terms, invoices, or delivery dates | Wholesale team | Forward the ticket to #wholesale with a summary | WD+1 |
| Website or app error, checkout failure, payment declined at a store, or anything that looks like a system fault | Engineering via #incidents | Post the ticket ID and a short summary; do not wait for a customer to report it twice | Within 1 hour of the post, an engineer will pick it up |
| Data breach or suspected data breach (including a customer seeing another customer's details) | Security via the incident process in eng-docs/oncall/incident-process.md | Treat as an incident immediately — do not pass go, do not wait for a lead | Immediate |

## Notes on the common ones

**Team lead escalation** — this is for complaints that are likely to end up with the {{FIN_OMBUDSMAN_2}} or a chargeback, or where the customer has already said they're going to the press. The team lead will decide whether to involve Vera or the legal team. Do not promise the customer a resolution time beyond what we can actually commit to.

**Disputes** — the disputes team owns chargebacks and card scheme disputes. If a customer says they'll call their bank, that's a disputes ticket, not a normal refund. Include the order number, the payment method, and what the customer has told us. The disputes team works from finance-docs/chargebacks.md.

**Stores** — only escalate to a store if the issue genuinely sits with them (stock check, click-and-collect problem, a store refund that hasn't landed). Do not use this path for delivery issues that are the carrier's fault — those stay with support and we raise a claim with the carrier ourselves.

**Engineering** — the #incidents channel is for things that are affecting customers at scale, not for a one-off oddity. If a single order has a strange status, check the order in orders-web first and only escalate if you can't explain it. If a payment is stuck, check billing-api's status before pinging anyone. The platform team would rather we post too much than too little, but a "this order shows as dispatched but the customer says no" is usually a carrier issue, not an engineering one.

## Response targets

We aim to acknowledge every escalation within the working day it's raised. The targets above are for *someone picking it up*, not for resolution — a team lead might take a day to investigate, but you should have heard back from them within the day you escalated.

If an escalation hasn't been acknowledged by the end of the working day, chase it in the relevant channel. Do not let a ticket sit without a response past that point.

## Wholesale

Wholesale escalations go through #wholesale, not through the normal support queues. If a wholesale customer calls the support line, take their details and forward the ticket — don't try to resolve credit or delivery queries yourself. The wholesale team works to the credit terms in finance-docs/wholesale/credit-terms.md and they'll pick it up from there.

## After hours

Outside UK working hours, the only escalations that should happen are genuine incidents (site down, payment outage, data breach). For anything else, leave the ticket in the queue with a clear note and it'll be picked up at the start of the next working day. The on-call engineer for the platform team is listed in eng-docs/oncall/oncall-guide.md and is the right person to ping for a true incident.
