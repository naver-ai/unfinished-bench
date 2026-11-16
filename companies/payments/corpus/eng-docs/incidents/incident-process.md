# Incident process

**Owner:** Site reliability  
**Last edited by:** Selin Zhang (Site Reliability Engineer)  
**Status:** Current

## Purpose

This page describes how Kilbarra handles incidents affecting production services, merchant-facing functionality, or internal systems that support them. It covers severity levels, roles, bridge etiquette, and what happens after an incident is closed. If you are on call, read this alongside the on-call guide.

## Severity levels

| Severity | Label | Definition | Payments examples | Who is notified |
|---|---|---|---|---|
| SEV-1 | Critical | A core payments service is unavailable or severely degraded for a material share of merchants or transactions. Financial loss, regulatory exposure, or a safeguarding risk is possible. | Authorisation success rate drops below the SLO threshold for more than a few minutes; a payout file is late to a bank and the next available slot is the following day; the core ledger cannot process settlement | Incident commander (IC), SRE lead, VP Engineering, treasury ops, #incidents, paging on-call SRE |
| SEV-2 | High | A significant feature or internal system is down or badly degraded, but merchants can still process and settle. Workarounds may exist. | Merchant dashboard is down for a sustained period; payment links are not generating; the reconciliation tool cannot pull the day's file | IC, #incidents, on-call SRE |
| SEV-3 | Medium | An internal tool or non-critical function is impaired. No merchant-facing impact. | The analytics warehouse is behind on ingestion; the case tool is slow; a status page component is stale | On-call SRE, team owning the system |
| SEV-4 | Low | A cosmetic or minor issue that does not affect operations. Tracked and fixed in the normal queue. | A typo on an internal dashboard; a non-production report is showing the wrong date | Team owning the system |

The IC can raise or lower the severity at any point. When in doubt, raise it. It is always easier to step down than to page people after the fact.

## Roles

Every incident gets an **incident commander (IC)** and a **scribe**. The IC comes from the incident commander rota (SREs and engineering managers) and is paged when the incident channel is opened. The IC stays in the role for the whole incident, or hands over explicitly to another IC if the incident runs long.

The IC owns the bridge, the timeline, and the decision to close the incident. They do not debug. If the IC finds themselves deep in a console, they should hand the troubleshooting to someone else and step back.

The **scribe** posts a running timeline to the #incidents channel, noting what was tried, what changed, and when. The timeline is the raw material for the review, so it should include timestamps, names, and the outcome of each action. The scribe does not need to be technical, but they do need to be on the bridge and able to type.

For SEV-1 and SEV-2 incidents where merchants can see the problem, someone from Incident & merchant communications joins the bridge to keep support and merchant success up to date. The status page guide and the customer notices page cover the mechanics of each.

## Running the bridge

The incident bridge is the primary channel in #incidents. If you are on the bridge, you are expected to keep it usable:

- Post one message per update. Do not reply to older messages to add a new data point; post a fresh message.
- Use threads for side conversations. If it is not relevant to everyone on the bridge, it goes in a thread.
- Do not ask "any update?" on the bridge. The scribe posts a timeline update at regular intervals; if there is no update, there is nothing new to report.
- The IC is the only person who declares an incident closed. If you believe the incident should be closed, say so on the bridge and let the IC make the call.
- Avoid speculation about root cause. State what is observed, not what is suspected to have happened.
- If you need to step away, say so. If you are the IC and you step away, hand over to another IC first.

The IC may use a separate troubleshooting channel for deep technical work, so the main bridge stays readable. If they do, the scribe's timeline should still capture the highlights from that channel.

## Closing the incident

An incident is closed when the immediate impact is over and the system is back within normal operation. Closure does not mean root cause is understood; it means the bridge is no longer needed. The IC makes that call and posts a short closure summary to #incidents with:

- Severity and duration
- What happened, in two or three sentences
- What restored service
- Whether a post-incident review is needed

The IC books the **post-incident review** before closing. The review happens within a few working days of the incident, unless the incident is still being investigated and the review needs to wait. The review owner is the team that owns the affected system, not necessarily the SRE team. The review should cover:

- The timeline, with the scribe's notes as the starting point
- What worked and what did not in the response
- The root cause, if known, and what will stop it recurring
- Follow-up actions, each with an owner and a target date

The review notes go into the change tracker as a single item, with the follow-up actions linked. The incident is not fully done until the follow-up actions have owners. If a follow-up cannot be scheduled, that is a decision for the team's lead, not something the review leaves open.

## During the review

The review is a blame-free conversation. The point is to improve the next response, not to assign fault. If someone made a call that looked reasonable at the time, that gets noted as a decision, not a mistake. The review notes should record what happened and what changes are coming, so the next team to hit the same problem has something to read.

After the review, the IC or the review owner posts a short summary to #incidents with a link to the review notes. If any action changes a runbook or an on-call guide, that change should be raised in the normal change process and completed before the next on-call rotation starts.
