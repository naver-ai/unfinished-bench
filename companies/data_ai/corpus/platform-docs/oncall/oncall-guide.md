# On-call guide

**Owner:** Cloud platform  
**Last edited by:** Jae Park (Site Reliability Engineer)

## Purpose

This guide covers the weekly on-call rota for the Cloud platform team, what to do when you get paged, and how to hand over. It is meant to get you through the first minutes of an incident and point you to the right places. It is not a substitute for the incident process — read that too.

## Rota

- The rota runs weekly, rotating through the Cloud platform team. Each shift starts on a working day morning and runs for seven days.
- The rota lives in the paging tool and is synced from the Cloud platform calendar. If you need a swap, find someone on the team who is willing and change the rota entry in the paging tool. Make sure the swap is reflected before the current shift ends.
- Handover happens on the last working day of your shift. Post a short summary in #cloud-platform before the end of your working day, even if nothing happened. Say what was quiet, what you dealt with, and anything the next person should watch. If you had an incident, reference the case number from the incident process.
- If you are on call, keep the paging app on your phone and your laptop within reach. You do not need to stay glued to your desk, but you do need to be able to respond within the paging acknowledgment window.

## The paging tool

- Pages go to the on-call person via the paging tool. It will call your mobile and send a push notification. Acknowledge the page in the app as soon as you see it. If you do not acknowledge within the window, it escalates to the next person on the rota.
- Do not silence the paging app for the week. If you are going somewhere without signal, tell the team in #cloud-platform and arrange coverage.
- The paging tool has a small set of labels for the kind of page. Use them when you acknowledge so the team can see what kind of thing is coming in.

## First minutes after a page

1. Acknowledge the page in the paging tool.
2. Read the alert details. Most pages come from the monitoring dashboards and will have a link to the relevant dashboard or log view.
3. Join #incidents and post a short line: what the page is, whether you have acknowledged it, and that you are looking. Do not wait until you know what is happening.
4. Look at the status page. If this is a known issue, it will be listed there with a note. Follow that note if it says what to do.
5. If you cannot tell from the alert what is affected, check the affected service's runbook. The analytics API runbook and the batch pool docs are the most common ones.
6. If it is a known issue with a documented fix in the runbook, apply that fix. Post in #incidents what you did and that you are closing the alert.
7. If the issue is not something you can fix in a few minutes, start the incident process and follow it. That means opening a case in tickets, assigning it to yourself, and keeping the timeline updated.
8. Keep the #incidents channel updated as you go. A short line every few minutes is enough. People from other teams will be watching and will ask if they need to.

## Escalation

- If you need a second pair of eyes, escalate in the paging tool to the Cloud platform team lead. That will page them directly. You can also ask in #cloud-platform if people are around, but do not rely on that for something urgent.
- If the incident involves the ML training cluster, the model serving infrastructure, or a model rollout that is misbehaving, escalate to the ML platform rota. You can find that rota in the paging tool. Do not try to fix model serving issues yourself — the ML platform team owns that.
- If the incident involves warehouse connections, the warehouse, or dbt runs, escalate to the Analytics warehouse team via the paging tool. Kaito Mori and Priya Raman are usually the first people to respond.
- If you are not sure who to escalate to, escalate to the Cloud platform team lead anyway. They will route it.

## Handover notes

- At the end of your shift, post in #cloud-platform:
  - Anything you were working on when the shift ended.
  - Any alerts that are still open and what you have done so far.
  - Any incidents that are still running and where they stand.
  - Any known weirdness that did not page but that the next person should keep an eye on.
- If you had an incident that is still open, make sure the case in tickets has a clear owner for the next person. Do not assume they will read your mind.
- If you made changes to infrastructure during your shift, make sure the {{IAC_TOOL}} state and the relevant docs are up to date. If you did something by hand that should be in {{IAC_TOOL}}, note it in the handover and create a follow-up ticket.

## The #incidents channel

- #incidents is for live incident coordination. Keep it tidy. One thread per incident, and put updates in the thread, not as new messages in the channel.
- If you are on call, you are expected to moderate #incidents during your shift. If someone posts a new incident as a top-level message, ask them to move it into a thread.
- Do not use #incidents for non-urgent things. That goes in #cloud-platform or #it-help depending on what it is.
- When an incident is resolved, close the case in tickets and post a short summary in the thread. The incident process has details on what the summary should contain.

## If it goes wrong

- If you get paged and you are not sure what to do, do not stay silent. Post in #incidents that you are looking and escalate to the team lead. Nobody will be annoyed at an early escalation.
- If you accidentally acknowledge the wrong page or close an alert you should not have, reopen it and say so. It is better to have a noisy channel than a missed incident.
- If the paging tool itself is down, check the status page and ask in #cloud-platform. We have a manual fallback rota in the Cloud platform calendar — the person whose shift it is should post in #incidents that they are covering.
- If you are on call during a major incident and you need rest, hand over to the next person early. The team lead can arrange cover. Do not run yourself into the ground.
