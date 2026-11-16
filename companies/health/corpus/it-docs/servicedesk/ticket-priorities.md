# Service desk priorities and response targets

**Owner:** IT service desk  
**Last edited by:** Bilal Graham

The service desk triages every ticket into one of four priority levels. Priority determines how quickly we respond, who works the ticket, and when we escalate. If you are not sure which priority to assign, pick the higher one and let the on-call lead reclassify it. Reclassifying down is easier than sitting on something urgent.

| Priority | What it means | Examples | First response target | Resolution or workaround target |
|---|---|---|---|---|
| P1 | A whole unit, clinic, or business function cannot work. Patient care or revenue is actively affected. | EHR down in an ED; pharmacy system offline; claims adjudication system not processing; VPN gateway down for a whole site | 10 minutes, 24/7 | Continuous work until resolved |
| P2 | A significant group is impaired, or a single critical function is unavailable with no workaround. | One clinic cannot chart; provider portal down for all users; prior authorization queue not loading; interface engine feed failing | 30 minutes during coverage hours | 4 working hours |
| P3 | One person or a small group is impaired, but a reasonable workaround exists. | A single workstation will not boot; one user cannot print; badge tap not working for one person; password reset after hours | 4 working hours | 2 working days |
| P4 | Routine, cosmetic, or planned work. No one is blocked. | New monitor request; software install for a new hire; screen flicker that is intermittent; documentation update | 2 working days | 10 working days |

## Coverage and after-hours

The service desk is staffed during normal US working hours from South Bend and Valparaiso on US working days. The Cork office covers the early part of the day, before the US offices open. Cork also covers US holidays that fall on Irish working days, and South Bend covers Irish public holidays.

P1 tickets are worked immediately by whoever is on call, regardless of site. The on-call rotation is published in the on-call guide. If a P1 comes in during Cork hours, Cork owns it until the next US working day handover, then the South Bend lead takes it over. Handover includes a written summary in the ticket plus a verbal handoff to the incoming lead.

P2 tickets that come in after the US offices close are triaged by Cork and worked if they can be; otherwise they are queued for the next working day and the requester is told when to expect contact. P3 and P4 tickets are not worked after hours.

## Escalation

- **P1:** The ticket is automatically paged to the on-call engineer and the service desk lead. If it is not acknowledged within 10 minutes, page the on-call manager. If the on-call manager does not respond within 10 more minutes, page the CIO office.
- **P2:** Escalate to the service desk lead if the resolution target will be missed. The lead can pull in the relevant platform team (EHR, interface engine, claims, etc.) through the #it-help channel.
- **P3/P4:** Escalate to the service desk lead if the ticket has not had an update in 5 working days, or if the requester has asked twice for an update without getting one.

Any ticket that is blocked by another team for more than 2 working days gets flagged in the weekly service desk review. Beatriz reviews the P1 and P2 list each morning with the on-call lead from the previous night.

## Notes

- A P1 is not only about downtime. A safety event reported through the safety event reporting system that involves IT (for example, a chart not displaying in the EHR) is treated as P2 at minimum and escalated to Quality & patient safety through the on-call chain.
- If a ticket arrives with no priority assigned, default to P3 unless the requester has said otherwise.
- Do not close a P1 or P2 ticket until the requester confirms the workaround or fix is acceptable to them. Confirmation can be a reply in the ticket or a message in chat; a screenshot is better.
- For after-hours password resets, see the on-call guide — those go to the Cork desk directly, not through the ticket queue.
