# On-call guide

**Owner:** Platform & SRE  
**Last edited by:** Diego Gallagher (Site Reliability Engineer)

---

## Rota

The on-call rota lives in `#incidents` as a pinned message, and the schedule is managed by Daniel Kruger. There are two rotations:

- **Primary** – one person, five days a week, starting at the beginning of the working day UK time and ending at the start of the next working day.
- **Weekend/night** – one person covers from the end of the working day until the start of the first working day after the break.

Coverage is split between UK and US time zones; if you are in Columbus, your shift starts at the beginning of the working day ET instead. The rota is published two weeks ahead. If you need a swap, find a volunteer in `#platform` and update the rota spreadsheet, then ping Daniel.

First time on call? Read this guide fully, then read `eng-docs/platform/environments.md` and `eng-docs/oncall/incident-process.md` before your first shift.

---

## Paging tool

Pages come from the alerting stack through the paging tool. You will receive:

- A push notification on your phone (install the app from the device portal)
- An email to your Mossgrove address

The paging tool is configured with the on-call rota, so you do not need to do anything per-shift. If you do not get pages but believe you should be on call, check the rota in `#incidents` and raise it in `#platform`.

---

## What to do when you are paged

1. **Acknowledge the page** – open the paging app and tap acknowledge. Do this even if you are unsure – it stops the alert from escalating to Daniel.
2. **Read the alert message.** Most alerts include a link to a dashboard or a log query. Open the link first – it often tells you what is happening faster than investigating from scratch.
3. **Check the incident channel** – join `#incidents` if you are not already in it. Look at the last few messages to see whether someone is already working the issue.
4. **Assess severity.**
   - If the site is down, checkout is failing, or wholesale order files are not generating: this is a **major incident** – follow the steps in `eng-docs/oncall/incident-process.md` immediately.
   - If it is a single store till, a single customer unable to pay, or a slow batch job: this is **minor** – you can work it during your shift without declaring an incident.
5. **Investigate.** Start with the relevant runbook:
   - Shop pages or checkout: `eng-docs/web/shop-web-runbook.md`
   - Order webhooks or order events: `eng-docs/web/orders-web.md`
   - Data pipelines: `eng-docs/data/pipelines-oncall.md`
   - Backups or snapshots: `eng-docs/platform/backups.md` or `eng-docs/platform/snapshots.md`
6. **If you cannot fix it within 30 minutes**, escalate to the team lead for the area. Daniel Kruger is the escalation for Platform & SRE. For anything involving payments, escalate to the payments team via `#payments-platform`.
7. **If you make a change to fix something, record it.** Add a comment on the alert in the paging tool and post a short summary to `#incidents`. Even if it was a one-line config fix, write it down – the next person will thank you.
8. **Close the incident.** Only close it once monitoring looks stable for at least 15 minutes. If it is a major incident, leave it open until the incident lead says otherwise.

---

## Escalation to team leads

| Area | Escalation |
|------|-----------|
| Platform & SRE | Daniel Kruger |
| Data engineering | Karim Obi |
| Customer support | Vera Barros |
| Wholesale / fulfilment | Rebecca Singh |

If the person above is unavailable, escalate to the next person in the team (noted in the rota spreadsheet). If you cannot reach anyone and the issue is critical, page again – the paging tool will escalate after 15 minutes automatically.

Do **not** escalate to Siobhan Keane unless the incident is company-wide or has been going for more than two hours without progress.

---

## Handover notes

At the end of your shift:

1. Post a message to `#incidents` with the subject `Handover: <your name>`.
2. Include:
   - Any open incidents and their current status
   - Anything you investigated but did not resolve
   - Any changes you made that are still settling (e.g. a restarted job, a scaled-up service)
   - Anything the next person should keep an eye on
3. If you are handing over mid-incident, call the next person on the phone – do not rely on chat.

The handover message does not need to be long – three or four bullet points is fine.

---

## The incident channel

`#incidents` is the single channel for all incident communication. Rules:

- Post the initial alert link when you start working something.
- Post updates every 30 minutes if the incident is still open.
- Do not use `#random` or `#general` for incident chat – keep it in `#incidents`.
- If you are not involved, do not post in `#incidents` while an incident is active – the thread is for the people working it.

After a major incident, the incident lead posts a summary in `#incidents` and the post-mortem is filed in the incident tracker.

---

## If it goes wrong

- **Your phone dies / you miss a page.** Log in to the paging tool from a browser and acknowledge there. If you know you will be away from your phone, set your on-call status in the rota or ask someone to cover.
- **You are unsure what to do.** Ask in `#platform` – someone is almost always around. The on-call shift does not mean you are alone.
- **The paging tool itself is down.** Check status from the internal status page. If pages are not sending, post a message to `#incidents` saying you are on call, and watch the alerts dashboard manually.
- **You make a mistake and break something.** Do not hide it. Revert the change, post in `#incidents`, and tell Daniel. Honest mistakes are fine – unrecorded changes are not.
- **The incident is beyond your skills.** That is fine. Escalate early. The team would rather you page Daniel in the middle of the night than sit on a problem until the morning.
