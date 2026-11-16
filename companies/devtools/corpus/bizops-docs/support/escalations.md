# Escalations

**Owner:** Developer support  
**Last edited by:** Owen Tadesse (Support Specialist)

This page covers when and how Developer support escalates to engineering, billing operations, security, or the account's CSM. It complements the flow in `../support/support-overview.md`; that page covers how we triage and respond, this one covers what we do when we need someone else.

## Before escalating

- Confirm the issue is not already tracked on the status page or a known incident in `#incidents`. If it is, follow the incident thread instead of raising a separate escalation.
- Make sure you have the account slug, org ID, any relevant request IDs, and the earliest affected time you can find. If you are missing any of these, gather them first — an escalation without them just causes a round trip.
- If the customer is a Gantline Inc. account, check the CRM for the account's CSM before going further.

## Escalation targets

| Target | When | Where to escalate | What to include |
|---|---|---|---|
| Engineering (owning team) | Product defect, service error, or behaviour that looks like a bug in a specific service | The owning team's channel (see service catalogue in `eng-docs/services/service-catalogue.md`); for build or CI issues use `#buildfarm` or `#dev-productivity` as appropriate | Account slug, org ID, request IDs, affected endpoint or service, timestamps, what we saw vs what the customer reported, whether it reproduces on a fresh workspace |
| Engineering (incident) | Service down, data loss, security concern, or anything with broad customer impact | `#incidents` immediately; do not wait for a team channel | Same as above plus current severity, customer count if known, and whether the status page has been updated |
| Billing operations | Plan, seat, invoice, or payment questions that support cannot resolve from the billing service or the admin console | `#billing-ops` | Account slug, plan name, seat count, invoice or payment reference if one exists, what the customer is asking for |
| Security | Credential exposure, suspicious access, abuse, or anything that might be a breach | `#security` (or follow `handbook/security/reporting-an-incident.md` if it is an active incident) | Account slug, what happened, when it happened, what access we have already revoked, customer contact if they reported it |
| CSM | Strategic accounts, renewal risk, or anything the customer success team should know about before support does more work | Tag the CSM in the ticket; use the CRM to find them | Ticket link, account slug, summary of the issue, what we already tried, any customer sentiment worth noting |

## Escalation process

1. Post to the target channel with the details from the table above. Keep it concise — the channel is the record, not a chat.
2. If no one acknowledges within a reasonable window (about two hours during Lisbon or Portland business hours), ping the team lead for that area. For engineering teams, that is usually the engineering manager listed in the service catalogue.
3. Once someone picks it up, keep the ticket updated with what the owning team says, and mirror anything customer-visible back to the customer in the ticket.
4. If the issue turns into an incident, hand over to the incident process in `eng-docs/oncall/incident-process.md` and follow that from then on.

## Notes

- Escalations are not a way to skip the queue. Use them when the customer is blocked or when the issue is beyond what support can act on, not because a ticket has been open for a while.
- For billing escalations, do not speculate about credits or refunds in the channel. The billing team handles that; support relays what the customer asked and what we already told them.
- If you are unsure which team owns a service, check the service catalogue or ask in `#engineering` before escalating to a random channel.
- After the issue is resolved, add a short note to the ticket with the outcome. That history is what lets the next person escalate faster.
