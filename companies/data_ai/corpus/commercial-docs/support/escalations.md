# Support escalations

Owner: Customer support · Last edited by Olivier Bishop

This page covers when and how to escalate from Support. If you are unsure whether something counts as an escalation, ask in #support rather than sitting on it.

## When to escalate

| Situation | Escalate to | How |
|---|---|---|
| Customer is asking for a refund, contract change, or commercial concession | Team lead, who routes to Commercial | Via the helpdesk handover note, then ping the team lead in #support |
| Customer is threatening to leave or has complained about service quality | Team lead immediately | Call or direct message the team lead; do not wait for a meeting |
| Technical issue that looks like it affects more than one customer | Engineering, via #incidents | Open an incident in the helpdesk and post a summary in #incidents with the case reference |
| Bug in imagery delivery, tasking portal, or the customer API console | Engineering, via #incidents | Same as above; include the affected order IDs or API calls if known |
| Question about whether a dataset can be shared, re-licensed, or used for a customer's purpose | Data governance team | Route the case to the data governance queue in the helpdesk and mention it in #data-governance |
| Customer asks for data we do not have or that is not in the data catalogue | Data governance team | Same routing; add what the customer wants and the closest catalogue match, if any |
| Account or billing discrepancy that support cannot resolve from the customer record | Finance via the helpdesk | Tag the case with `finance-review` and add a note for the finance team |
| Security concern (unusual access, possible data exposure) | Security via #security | Follow the incident reporting process in the handbook; do not post details in #support |

## Response targets by plan tier

Targets are measured from when the case is received in the helpdesk. Working days are Rotterdam business days, except for US customers on the Americas coverage plan, where they are Denver business days.

| Plan tier | First response | Update cadence | Escalation to team lead if |
|---|---|---|---|
| Essential | End of next working day | At least every 3 working days | No response within 2 working days, or case is blocking the customer |
| Professional | Same working day | At least every working day | No meaningful progress within 2 working days |
| Enterprise | Within 4 working hours | At least twice per working day | No meaningful progress within 1 working day, or the customer asks for a manager |

Support coverage hours are in [`coverage.md`](coverage.md). If a case arrives outside coverage, its response target starts at the next coverage start.

## What is not a support escalation

Some things look like escalations but have a different home:

- **Feature requests** go to Customer success, who log them with the product teams. Support does not promise timelines.
- **Imagery tasking changes** (repointing, cancelling, or adding an area of interest) go to Imagery acquisition and processing via the tasking portal; only if the portal itself is broken do we escalate to engineering.
- **Sensor data gaps** go to the sensor network team via the helpdesk queue; they handle field visits and sensor health.

## Notes on escalation quality

- When escalating, include the case reference, what the customer expects, and what has been tried so far. A one-line "customer unhappy" is not enough.
- Keep the customer informed when you escalate; tell them you have involved the right team and roughly when they will hear back. Do not overpromise.
- If the team lead is unavailable, escalate to the Support Operations Manager or the Support Lead, Americas for cases on the Americas coverage plan.
- After an incident-driven escalation, the support specialist who opened it follows the case through to resolution unless the team lead reassigns it. Do not assume someone else picked it up.
