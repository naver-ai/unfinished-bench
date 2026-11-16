# On-call guide

Owner: Site reliability  
Last edited by: Olivier Campos (Senior Site Reliability Engineer)

## Purpose

This guide covers the follow-the-sun rota for Gantline's production services, what to do when the paging tool wakes you, and how to hand off cleanly. It is written for engineers in Site reliability, but the first few sections are useful for anyone who might get paged.

## Rota and shift times

The rota runs follow-the-sun between Lisbon and Portland. Lisbon covers the EU morning and afternoon; Portland covers the US morning and the EU evening. Each shift is roughly one working day, and the handover happens at the boundary.

- Lisbon shift: starts at the beginning of the working day in Lisbon and ends in the late afternoon Lisbon time.
- Portland shift: starts at the beginning of the working day in Portland and ends in the late afternoon Portland time.

During the gap between the Portland shift ending and the Lisbon shift starting, pages go to the Portland on-call engineer unless the paging tool has been told otherwise. In practice that means the Portland engineer carries the pages that come in outside their core shift for the US timezone. The Lisbon engineer picks up anything still open at the start of their shift.

The rota itself lives in the paging tool. If you need to swap a shift, use the paging tool's handoff feature and make sure the swap is acknowledged by both sides. Do not just trade shifts in chat and forget to update the tool.

## The paging tool

We use the paging tool for all production pages. It is the single source of truth for who is on call, what they are on call for, and how to reach them. Keep your contact details current in the tool. If you change your phone number or your chat handle, update it before you are due on call.

The paging tool is configured with several routes:

- `production-critical` — pages for services that are down or degrading in a way that affects customers.
- `production-important` — pages for issues that need attention but are not customer-facing yet.
- `buildfarm` — pages for the build farm and the internal runner pools. These route to Build infrastructure, not to Site reliability.
- `lab` — pages for lab VM issues. These route to the lab infrastructure team.

If you are not sure which route a page came in on, check the paging tool's history for the alert. The alert will have a link to the relevant metric dashboard or log view.

## What to do when paged

1. **Acknowledge the page** in the paging tool. This stops the escalation timer. If you do not acknowledge within the configured window, the tool will page the next person on the route.
2. **Read the alert payload.** It will tell you the service, the metric that fired, and a link to the dashboard. Do not skip this step — most alerts include the context you need to start investigating.
3. **Join #incidents.** If the incident is not already being tracked there, create a thread with the service name and a short description. Paste the alert link into the thread.
4. **Check the status page.** If the issue is visible to customers, someone from Site reliability should update the status page early. If you are not sure, err on the side of posting a "monitoring" update. You can always remove it later.
5. **Start investigating.** Use the metrics dashboards and the service logs. For most services, the logs are in the data warehouse and you can query them with the standard SQL interface. For the hosted runners, the relevant dashboards are under the `buildfarm` folder in the metrics dashboards.
6. **If you cannot resolve it within 15 minutes, escalate.** Do not sit on an incident hoping it clears up. Escalating is the expected behaviour, not a failure.

## Escalating to the owning team

Every service in the service catalogue has a named owning team. The catalogue lists the on-call contact for each team. When you escalate, post in #incidents and mention the owning team's channel if it exists. For example, if the issue is in the artifact store, post in #dev-productivity and mention the artifact store service name.

When you escalate, include:

- The alert that fired, with the link.
- What you have tried so far.
- Any dashboards or log queries you have already run.
- Whether the status page has been updated.

The owning team may take over the incident thread. If they do, stay in the thread in case they need context. You are not released until the thread is closed.

## Handover notes

At the end of each shift, write a handover note in the paging tool. The note should be short and factual:

- What is currently open, with links to incident threads or tickets.
- What you have tried and what the current state is.
- Anything the next person should look at first.

Handover notes are visible to the next person on the rota. They are not a substitute for a proper incident report — they are just enough context so the next shift does not start from zero.

If you are handing over an active incident, try to do it in person (or in a direct message) rather than just writing the note. A two-minute chat is worth more than a paragraph of text.

## The #incidents channel

The #incidents channel is where incident threads live. Everything that happens during an incident goes in the thread: investigation notes, commands run, decisions made, and the final resolution. The thread is the record that feeds the post-incident write-up.

Posting in #incidents is not optional. If you are paged and you do not start a thread, the SRE manager (or the person who happens to be watching) will ask you to. It is easier to start it at the beginning.

When the incident is resolved, close the thread with a summary: what happened, what the impact was, what fixed it, and what follow-up is needed. The summary should be a few sentences, not a paragraph. The full detail goes in the incident report if one is warranted.

## Compensation for out-of-hours pages

We track pages in the paging tool and the data feeds into the payroll system monthly. If you are paged outside your normal working hours, you are entitled to compensation in line with the policy in the handbook. The accounting team pulls the page records from the paging tool and processes them through payroll. You do not need to file anything.

If you believe a page was missed in the records, contact the accounting team with the time and date of the page and the paging tool's alert ID. They will check the logs and correct it.

## If it goes wrong

The most common failure is not acknowledging the page within the window. The escalation timer does not wait for you to finish reading the alert. Acknowledge first, read second.

If the paging tool itself is down, check the status page and the metrics dashboards. The paging tool has its own health dashboard. If it is down, the fallback is to watch #incidents — the SRE manager will coordinate manually and page people via chat or phone. This is rare, but it has happened.

If you are paged for something you do not recognise, do not guess. Escalate to the owning team from the service catalogue. The owning team would rather get a page for something that is not theirs than have you spend an hour investigating a service you have never seen.

If you make a change that makes things worse, say so in the incident thread immediately. Do not try to hide it. The incident process works because we have an accurate record of what was tried and what the effect was. A wrong change that is documented is useful. A wrong change that is hidden is a problem.

Finally, if you are the on-call engineer and you are unwell or otherwise unable to respond, tell the SRE manager as early as possible. They will arrange a swap in the paging tool. The rota is built so that there is always someone who can pick up a shift at short notice.
