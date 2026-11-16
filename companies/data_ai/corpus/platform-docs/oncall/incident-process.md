# Incident process

**Owner:** Cloud platform  
**Last edited by:** Tomas Fleming  

This page describes how we classify incidents, who runs the response, how we keep support and customers informed, and what a post-incident review should contain. It applies to the services and pipelines we operate across the platform, imagery, sensor and application teams. If you are unsure whether something counts as an incident, raise it in #incidents and let the on-call engineer decide.

## Severity levels

| Level | Meaning | Examples | Response expectation |
|---|---|---|---|
| SEV-1 | Customer-facing service unavailable or core data pipeline stopped; revenue impact or safety-relevant monitoring degraded | Analytics API returns errors for all requests; imagery ingest has not advanced for several hours and the backlog is growing; sensor telemetry gap covering a flood-prone area during a rainfall event | Continuous effort until resolved; incident commander named within 30 minutes; update #incidents and the status page within the same window |
| SEV-2 | Significant degradation or partial outage; a subset of customers or a single region affected; internal tooling blocked for a whole team | A customer delivery is late past the agreed window and the partner is waiting; one water board cannot see recent gauge data; the tasking portal fails for one region | Work during office hours unless the on-call engineer judges otherwise; status page update within one hour; named owner for the response |
| SEV-3 | Minor degradation, cosmetic issue or operational annoyance; workaround exists | A dashboard is slow to load for one team; a sensor station reports intermittent gaps but data is within the SLA; a non-critical export job fails once and retries | Fix in the normal queue; no status page entry unless it drags on for more than a working day |
| SEV-4 | No immediate impact; proactive fix or hygiene issue | A certificate expires next month; a {{IAC_TOOL}} plan shows a drift that is harmless; a log source stops sending and we did not notice | Handle through the backlog; mention in #incidents only if it explains something someone is asking about |

The on-call engineer on duty sets the initial severity. Anyone can challenge it, but the incident commander (once named) owns the final call. Downgrading a severity is fine when the situation is clearly better than first thought; upgrading is fine when the impact grows. There is no penalty for getting the initial level wrong, only for not revisiting it.

## Incident commander

For SEV-1 and any SEV-2 that spans more than one team, the first on-call engineer to respond names an incident commander (IC). The IC does not need to be the person fixing the problem. Their job is to:

- keep the timeline in #incidents (or a dedicated thread) up to date
- decide who is working on what and pull in extra people when needed
- talk to support and the status page when the comms step says so
- call the end of the incident and confirm the severity for the review

For a single-team SEV-2, the engineer handling it can act as their own IC and does not need to hand over. For SEV-1, if the response looks like it will last more than a couple of hours, the IC should hand over to someone else after the first hour so the response does not stall. The Cloud platform team keeps a small rota of people who can take IC duty; anyone who has done the on-call module can volunteer.

## Comms

Keep the noise low until the picture is clear, but do not go silent. The minimum expectations:

| Audience | SEV-1 | SEV-2 | SEV-3/4 |
|---|---|---|---|
| #incidents | First update within 15 minutes of the call, then at least every 30 minutes until resolved | First update within 30 minutes, then when something changes | One message if it explains an anomaly, otherwise nothing |
| Support team | Tell the support on-call via the helpdesk channel; they triage customer questions and can open a case in the helpdesk if needed | Same as SEV-1 but only if customers are likely to notice | No direct contact |
| Status page | Page entry within 30 minutes. Include affected product area, start time, and a short description. Update at least hourly | Page entry within one hour if customers can see the effect; otherwise wait and see | No entry |
| Customer notifications | The IC drafts a customer-facing summary and hands it to the support team; they send it via the customer API console or by email depending on the customer's preference | Support decides whether a notification is needed; the IC helps with wording | No notification |

The status page is where customers follow incident updates. Keep incident details out of #random. For anything that looks like a security issue, follow the security incident reporting flow in the handbook and let the security team lead the external messaging.

The support coverage doc has more on how the support rota overlaps with on-call; for a SEV-1 outside Rotterdam office hours, the Denver office support person is the first contact for customer questions.

## Running the response

Some practical notes that have come up more than once:

- Use a dedicated thread in #incidents for the timeline. The IC starts it with the initial detection message and posts updates there. The main channel keeps the summary.
- Do not open multiple threads for the same incident. If someone does, the IC closes the duplicates with a pointer to the main one.
- When you hand over between shifts, the IC posts a handover message with the state, what has been tried, and what the next person should try. The on-call guide has the handover format.
- The imagery operations team and the sensor network team each have their own escalation paths; the IC pulls them in when the incident touches their areas rather than trying to fix it alone.

## Post-incident review

Every SEV-1 gets a post-incident review (PIR). SEV-2 incidents get a PIR when the IC or the affected team asks for one, or when the same failure has happened twice in a quarter. The IC schedules the PIR within five working days of the incident being closed. The review is a meeting, not just a document; the doc is the output.

The PIR document lives in the platform-docs repository under `oncall/pirs/` with the file name matching the incident. The template:

```markdown
# PIR: <short title>

- Incident: <link to the #incidents thread and any status page entry>
- Severity: <initial and final>
- Dates: <start and end, working days>
- IC: <name>
- Responders: <names and teams>

## Summary
<two or three sentences on what happened and what customers saw>

## Timeline
| When | What |
|---|---|
|  |  |

## Root cause
<what actually caused it, not the symptom>

## What went well
<bullet list>

## What went poorly
<bullet list>

## Actions
| Action | Owner | Due |
|---|---|---|
|  |  |  |

## Follow-up
<whether the actions were done and what the review team learned>
```

The IC (or a delegate if the IC is unavailable) drafts the PIR and circulates it in the team channel before the meeting. The meeting should cover the timeline, the root cause, and agree the actions. The IC assigns owners and due dates; the platform team checks follow-up at the monthly platform review. If an action is not done by its due date, the owner says so in #incidents and proposes a new date — it is not a failure, but we do not let PIR actions disappear.

For SEV-2 reviews, the same template works; keep the timeline shorter and do not over-invest in the write-up. The point is to capture the learning, not to produce a long report.
