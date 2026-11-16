# IT on-call guide

**Owner:** Infrastructure & SRE  
**Last edited by:** Jin Olsen (Site Reliability Engineer)

---

## Purpose

This guide covers the on-call rota for the Infrastructure & SRE team, the hand-off between South Bend and Cork, and what to do when the pager fires. It applies to all SREs and Systems Engineers on the rota.

## Rota

- The rota lives in the paging system under **Infrastructure & SRE On-call**. There are two shifts: **primary** and **secondary**.
- Primary handles pages. Secondary covers for primary if they are unreachable or need a second pair of hands.
- The rota runs for seven days at a time, changing over at a fixed time on the first working day of the week. Check the paging system for your exact rotation — it is visible to the whole team.
- If you cannot cover a shift, swap with another engineer in the paging system at least two working days before the shift starts. Post in #infrastructure so everyone knows who is carrying the pager.
- Vacation or sick days: update the rota and swap shifts before the changeover, not after.

## Follow-the-sun

- South Bend covers the US daytime shift. Cork covers the portion of the US shift that falls outside South Bend working hours.
- Hand-off happens twice a day at fixed times Irish time. The outgoing engineer posts a short handover note in #infrastructure and makes sure the handover log is current.
- The handover note must include: open pages, anything that was escalated, anything that is still being worked, and anything the incoming engineer should look at first.
- If the incoming engineer does not see a handover note within 30 minutes of the shift start, they should page the outgoing engineer and ask for one.

## When you are paged

1. Acknowledge the page in the paging system as soon as you see it. Do not wait to read the full alert before acknowledging.
2. Check the alert details. Most pages include the system name and a link to the relevant dashboard or log view.
3. Post in #infrastructure with the alert ID, the system, and a one-line summary. Use the **on-call** tag if the channel allows it.
4. Assess severity. If a clinical system is down or the claims feed is stopped, treat it as a major incident and follow the major incident process in `it-docs/oncall/major-incidents.md`.
5. If you need to make a change to fix something, follow the change management process in `it-docs/change/change-management.md`. Emergency changes are allowed for outages, but you must log the change after the fact.
6. If you cannot resolve within 30 minutes of acknowledgment, escalate to the secondary. If the secondary cannot help, escalate to Sebastian Marchetti (Infrastructure Manager) via the paging system or phone.
7. Keep the #infrastructure channel updated as you work. A short update every 15–20 minutes is expected for anything that takes more than a few minutes.

## Escalation

- **Tier 1:** Primary on-call
- **Tier 2:** Secondary on-call
- **Tier 3:** Sebastian Marchetti (Infrastructure Manager)
- **Tier 4:** Raymond Pellegrino (CIO) — only for a major incident that is not resolving or where the health system's operations are significantly affected.

Escalate early rather than late. If you are not making progress, that is a reason to escalate, not a reason to keep trying alone.

## Handover notes

- The handover log lives in the infrastructure channel's pinned items. Each entry has: date, shift, engineer, open pages, notes.
- Write the handover note at the end of your shift, even if nothing happened. "No pages, no open issues" is a valid note.
- Include anything that is half-finished, even if it is not urgent. The next engineer may need the context.
- If you made a change that is still settling, say so. Do not leave the next engineer to discover it.

## Infrastructure channel

- #infrastructure is the working channel for on-call activity. All pages, alerts, and incident updates go here.
- Keep it readable. Use threads for discussion on a specific alert. Post the summary in the main channel and put the detail in a thread.
- Do not use #infrastructure for non-urgent chat. Use #general or #random for that.
- The channel is visible to the whole IT department, so write for that audience. Avoid assuming readers know the context of a particular alert.
- If you post a link to a dashboard or log view, make sure the link works for people outside the SRE team.

## If it goes wrong

- If you acknowledge a page but then cannot work on it, tell the secondary immediately and hand over what you have so far.
- If you miss a page, the paging system will escalate to the secondary automatically. When you see the missed page, post in #infrastructure and own it. Everyone misses a page occasionally; ignoring it is the problem.
- If a fix makes things worse, say so in the channel. Do not try to hide it. Roll back the change if that is possible, and log what happened.
- If you are on-call and your pager is not receiving pages, test it at the start of your shift. The paging system has a self-test option. If it fails, contact the team lead and arrange for the secondary to cover while the pager issue is sorted.
- For any page that is a false alarm or a repeat of a known non-issue, note it in the handover log. The team reviews recurring alerts and works on reducing noise, but only if the data is recorded.

---

## Quick reference

| Item | Where |
|------|-------|
| Major incident process | `it-docs/oncall/major-incidents.md` |
| Change management | `it-docs/change/change-management.md` |
| Backups and restores | `it-docs/infra/backups.md` |
| Remote access VPN | `it-docs/network/remote-access-vpn.md` |
| EHR downtime | `it-docs/clinical-systems/ehr-downtime.md` |
| Interface engine / HL7 | `it-docs/clinical-systems/interfaces.md` |

---

*Last reviewed: rota and hand-off times confirmed with the Cork team. Contact Jin Olsen with corrections.*
