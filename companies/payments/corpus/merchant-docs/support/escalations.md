# Escalations

**Owner:** Merchant support  
**Last edited by:** Petra Bishop (Senior Support Specialist)

This page covers when and how to escalate issues from merchant support to other teams, and what to include so the receiving team can act without chasing for detail. If you are unsure whether something needs escalation, escalate — it is easier to stand an escalation down than to recover a missed one.

## When to escalate

| Situation | Escalate to | Channel / tool | Notes |
|---|---|---|---|
| Merchant cannot take payments and it looks platform-wide (multiple merchants, or our systems clearly degraded) | Incident channel | #incidents, then the paging tool if asked | Follow the incident process in `eng-docs/incidents/incident-process.md`. Do not wait for a second report. |
| Possible fraud, money laundering, sanctions match, or unusual transaction pattern on a merchant account | Financial crime | Case tool, then #risk-controls | Include the merchant ID and what you saw. Do not discuss the suspicion with the merchant. |
| Merchant risk rating looks wrong, or a merchant's activity is outside what their risk profile supports | Risk | #risk-controls | Reference the merchant risk rating in `risk-docs/risk/merchant-risk-ratings.md` if relevant. |
| Billing dispute, fee query, or invoice question you cannot resolve from `merchant-docs/billing/` | Billing | #billing | Attach the merchant's message and what you have already checked. |
| Account is otherwise healthy but the merchant needs proactive help, or a relationship is at risk | Merchant success | #merchant-success | Include the merchant segment from `merchant-docs/success/merchant-segments.md` and any recent review notes. |
| Something is degrading but not yet an incident (latency, intermittent webhook failures, delayed payouts) | SRE / Payments | #sre or #payments-platform | Use #incidents only if it meets the incident criteria. Otherwise raise in the team channel and link the ticket. |
| Partner feed or partner API key problem | Partner support | #partner-integrations | Adrian's team owns partner support; loop them in before escalating further. |

## What to include

Every escalation should have at minimum:

- Merchant or partner name and ID
- A one-line summary of the issue
- What you have already tried (tickets, KB articles, dashboard checks)
- Impact: is the merchant actively unable to process, or is this preventive?
- Any time pressure, e.g. a payout deadline or a bank file cut-off
- Links to the relevant ticket, merchant record in the back office, and any chat threads

For financial crime and risk escalations, do not include the merchant's transaction history in the chat message — put it in the case tool and link the case.

## After you escalate

- Stay in the thread until someone from the receiving team acknowledges, or hand over explicitly in the ticket.
- If the issue becomes an incident, hand the incident channel the full context and let the incident process take over.
- If you escalated to financial crime, do not update the merchant until the case tool says you may.
- For billing escalations, check `merchant-docs/comms/writing-to-merchants.md` before drafting anything to the merchant — billing wording has its own conventions.

## Common mistakes

- Escalating to #incidents for a single-merchant issue. Single-merchant issues go to the relevant team channel unless the merchant is a platform partner or the issue is spreading.
- Escalating without a ticket. Every escalation should trace back to a ticket in `tickets`.
- Over-escalating routine chargebacks — those go through the chargeback workflow in `risk-docs/risk/chargeback-monitoring.md`, not to #risk-controls.

## Out of hours

The on-call engineer is reachable through the paging tool — use it for platform-wide outages and for any issue where a merchant's funds or ability to process are at immediate risk. For anything else, log the ticket and escalate at the start of the next working day. The on-call guide (`eng-docs/oncall/oncall-guide.md`) has the full criteria.
