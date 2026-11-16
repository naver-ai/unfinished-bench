# Major incident process

**Owner:** Infrastructure & SRE  
**Last edited by:** Tomas Fonseca  

This document covers how we run a major incident from declaration through review. It applies to all Kellsbrook Health systems, including the EHR, patient portal, claims adjudication, the interface engine, and anything else that affects patient care, member services, or revenue cycle.

---

## Severity levels

| Level | Definition | Examples | Initial response |
|-------|-----------|----------|------------------|
| **SEV-1** | System unavailable or data integrity at risk; clinical or member safety affected; regulatory reporting required | EHR down across a campus; interface engine stopped so lab and pharmacy orders queue for more than one hour; claims adjudication halted past the payment run cut-off | Page Infrastructure & SRE immediately; declare incident in #it-help; incident commander takes over |
| **SEV-2** | Significant degradation or partial outage; workarounds exist but manual effort is high | Patient portal read-only; provider portal slow for registration checks; prior authorization queue delayed more than two hours; one campus loses chart access in chartarc | Page Infrastructure & SRE; declare incident in #it-help; incident commander assigned within 30 minutes |
| **SEV-3** | Minor impairment; no clinical impact; workaround is straightforward | Single clinic's badge readers offline; claims ingest backlog under an hour; VPN slow for remote users | Log ticket, assign to the owning team, monitor |

Anyone can declare a major incident by posting in #it-help with the system name and the perceived level. If you are unsure whether it is SEV-1 or SEV-2, call it SEV-1; we can downgrade later.

---

## Incident commander

The first Infrastructure & SRE person to respond takes the incident commander role and keeps it until the incident is closed or explicitly handed off. The commander:

- Opens a channel (usually `#incident-<shortname>`) and pins the incident ticket link.
- Assigns a **scribe** to keep the timeline. The scribe does not troubleshoot.
- Confirms the severity level and posts it in #it-help, #southbend-campus, #valpo-office, #kalamazoo-campus, and #cork-office as appropriate.
- Coordinates with the service desk so they have a script to acknowledge the outage.
- Watches the clock: for SEV-1, every 30 minutes we post a status update in the incident channel. For SEV-2, every 60 minutes.
- Declares the incident resolved when the fix is confirmed and the affected service has been stable for at least 15 minutes.

The commander does not need to be the most senior person. If Sebastian or a manager is present, they can advise, but the commander owns decisions.

---

## Keeping the right people informed

### Nursing and clinics

For any incident involving the EHR, the patient app, or the interface engine, the incident commander (or their delegate) calls the **nursing supervisor on duty** for each affected campus. The nursing supervisor decides whether to invoke the downtime procedures in `it-docs/clinical-systems/ehr-downtime.md`.

- South Bend: call the nursing supervisor via the hospital paging system.
- Valparaiso: call the nursing supervisor via the hospital paging system.
- Kalamazoo: call the nursing supervisor via the hospital paging system; also alert the Research Institute if the issue affects the EDC or the CTMS.
- Cork: call the GP-led medical centre directly; Siobhán Kiely (practice manager) is the daytime contact. The centre runs its own practice system, so an EHR outage mostly affects the care summaries it gets for US patients.

Do not wait for the nursing supervisor to call us. We call them.

### Health Plan

For claims adjudication, the member portal, the provider portal, or prior authorization, the incident commander posts in #claims-ops and #member-services and asks the team leads to spread the word. Chiara Sorensen (Claims Operations Lead) and the member services supervisor decide whether to adjust phone scripts or extend deadlines. The commander also copies #provider-services when the provider portal is affected.

### Executives

For SEV-1 incidents, the incident commander notifies Raymond Pellegrino through the on-call process. Raymond's office decides whether the executive team needs a briefing. Do not skip this step even if the incident looks minor at first; it is easier to cancel a briefing than to explain why we did not call.

---

## EHR downtime hand-off

When the nursing supervisor declares downtime:

1. The incident commander posts the declared downtime start time in the incident channel and in #southbend-campus, #valpo-office, #kalamazoo-campus, or #cork-office as applicable.
2. The service desk posts the downtime script in #it-help.
3. The records office activates the chartarc pull queue for any requested records. The records team posts in #records-office when they are ready.
4. The incident commander tracks the downtime duration. If it exceeds four hours, the chief medical informatics officer is notified through the hospital paging system.
5. When the EHR is back, the incident commander confirms with the nursing supervisor that the downtime period has ended and the EHR is accepting orders. The nursing supervisor coordinates the back-entry of orders and notes.

The downtime hand-off is not complete until the nursing supervisor confirms the EHR is usable on at least one workstation per unit. Do not close the incident before that confirmation.

---

## Post-incident review

Every SEV-1 and SEV-2 incident gets a post-incident review within five working days. The incident commander schedules it, invites the teams involved, and posts the draft in #infrastructure.

### Template

Use the following template for the review document:

```
# Post-incident review: <short title>

**Incident ticket:** <link>
**Date and time range:** <start> – <end>
**Severity:** SEV-<level>
**Systems affected:** <list>
**Incident commander:** <name>
**Scribe:** <name>

## Summary
<two to five sentences for a non-technical reader>

## Timeline
| Time (UTC) | Event |
|------------|-------|
|            | First report |
|            | Declared incident |
|            | Nursing supervisor notified (EHR incidents only) |
|            | Downtime declared (if applicable) |
|            | Fix deployed |
|            | Service confirmed stable |
|            | Incident closed |

## Impact
- <patients / members / providers affected>
- <manual workarounds used>
- <missed SLAs or deadlines>

## Root cause
<what happened, in plain terms>

## What went well
<bullet list>

## What went poorly
<bullet list>

## Action items
| Action | Owner | Due |
|--------|-------|-----|
|        |       |     |

## Follow-up
<open questions, if any>
```

The completed review is stored alongside the incident ticket. Action items are tracked in tickets and reviewed at the next Infrastructure & SRE team meeting. If a review identifies a change to this document or to runbooks, the change is submitted through the normal change management process in `it-docs/change/change-management.md`.

---

## Related documents

- `it-docs/clinical-systems/ehr-downtime.md` — EHR downtime procedures
- `it-docs/oncall/oncall-guide.md` — IT on-call guide
- `it-docs/servicedesk/ticket-priorities.md` — Service desk priorities and response targets
- `it-docs/change/change-management.md` — Change management
