# Incident process

**Owner:** Site reliability  
**Last edited by:** Priya Ozturk (Site Reliability Engineer)

## Severity levels

| Severity | Definition | Examples |
|---|---|---|
| **SEV-1** | Customer-facing service is down or severely degraded for a large population. Ongoing data loss or security exposure. | Hosted runners unavailable across all pools; git push failing for a broad set of customers; code search returning 5xx at high rates. |
| **SEV-2** | Significant degradation or outage for a subset of customers, or a core internal system is down. | API error rate above threshold for one region; cloud workspaces failing to start for a segment; the admin console unreachable for staff. |
| **SEV-3** | Minor degradation, single customer affected, or an issue that has a workaround. | One customer's builds failing due to a cache miss; a mobile push batch failing for a small list of installs. |
| **SEV-4** | No active impact; a bug or anomaly that needs tracking. | A dashboard showing stale metrics; a flaky internal tool. |

A SEV-1 or SEV-2 is declared by whoever is on call. If you are unsure, declare SEV-2 — it is easier to downgrade later than to have missed the escalation window.

## Roles

Every incident above SEV-4 gets an **incident commander (IC)**. The IC is the single decision-maker for the response. They are not expected to debug — they coordinate, set the timeline, and make the call on mitigations.

| Role | Responsibility | Who fills it |
|---|---|---|
| Incident commander | Owns the response, declares severity, coordinates actions, decides on mitigations, calls the all-clear. | The first SRE on call, unless they are already deep in another incident. |
| Comms lead | Drafts status page updates, posts in #incidents, keeps #support and #customer-success informed. | The IC can hand this to another SRE, or to someone from the relevant product team if the incident touches their area. |
| Subject matter expert | Debugs the specific component (buildfarm, API, editor, mobile, etc.). | The person most familiar with the affected service; pulled in by the IC via #engineering or the relevant channel. |
| Scribe | Tracks actions and decisions; helps assemble the post-incident review. | Any volunteer; often a newer SRE or an engineer from the affected team. |

For SEV-1 incidents, the IC should hand off comms to someone else early so they can focus on the technical response. Ava Fleming or Olivier Campos can help pull in additional SREs if the response needs more hands.

## Running the incident

- All coordination happens in #incidents. Create a thread per incident; post the severity, the affected component, and the incident channel name.
- The IC posts a short summary at the start and updates the thread as the picture changes. No one else should post top-level messages in #incidents during an active incident — use the thread.
- The status page is updated by the comms lead. Every update goes through the IC first. If the incident affects a customer-facing feature, update the status page within 30 minutes of declaring SEV-1 or SEV-2.
- Keep #support in the loop. Sofia Marek or another support specialist will be watching the thread; the comms lead should post a one-line summary of what customers are seeing and what the team is doing. Support handles individual customer replies; they do not need technical detail.
- For SEV-1 incidents, the comms lead also posts a short update in #general so the rest of the company can answer customer questions without guessing.
- Do not close the incident until the fix is verified in production and the monitoring dashboards look stable. The IC calls the all-clear and posts a summary in #incidents.

## Post-incident review

Every SEV-1 and SEV-2 gets a post-incident review (PIR). SEV-3 incidents get a PIR if the IC or the affected team wants one.

The PIR is filed as a new document in the eng-docs/oncall folder. Use the template below. The IC is responsible for getting it written and circulated; the scribe usually drafts it. Target is to circulate the draft within five working days of the all-clear.

### PIR template

```markdown
# PIR: <short title>

**Date:** <date of incident>
**Severity:** SEV-<level>
**IC:** <name>
**Duration:** <start to all-clear>

## Timeline

| Time (UTC) | Event |
|---|---|
|  | First report or alert |
|  | Severity declared |
|  | Status page updated |
|  | Mitigation started |
|  | Mitigation verified |
|  | All-clear |

## Impact

What customers or internal users experienced, how many were affected, how long it lasted.

## Root cause

What actually went wrong. Include the full chain — the trigger, the contributing factors, and why it wasn't caught earlier.

## What went well

## What went wrong

## Action items

| Action | Owner | Target |
|---|---|---|
|  |  |  |

## Follow-ups

Any links to related issues, tracking tickets, or follow-up PIRs.
```

The PIR is posted in #incidents and #engineering. If the incident revealed a systemic gap, the relevant team owns the follow-up items; the SRE team tracks them until they are closed.

## Escalation

If the incident is not resolving or the IC needs more authority, escalate to Ava Fleming or Joaquim Serrano. For incidents touching customer accounts or billing, loop in #billing-ops early — they can check account state without waiting for a support handoff.

## Notes

- The on-call rota is in the paging tool. If you are IC and need to hand over, find your relief in #sre before stepping away.
- Severity levels are guidance, not a checklist. A single customer running thousands of builds may feel like a SEV-2 even if the definition says SEV-3. Use judgment and write down the reasoning in the thread.
