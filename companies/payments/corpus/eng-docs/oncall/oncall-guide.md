# On-call guide

**Owner:** Site reliability  
**Last edited by:** Lena Schmidt (Site Reliability Engineer)

---

## Purpose

This guide covers how on-call works across the engineering teams that carry a rota, what to do when you get paged, how to hand over, and how to escalate when something needs more than one person. It is the starting point for anyone new to a rota and the reference for anyone who has been on one for a while.

## Rotas

Each team that operates a service runs its own rota in the paging tool. The rotas are:

- **SRE** — 24x7, primary and secondary, one week at a time. Handover is on the first working day of the week.
- **Payments platform** — 24x7, primary only, one week at a time.
- **Payments dev** — daytime cover, one day at a time.
- **Data platform** — daytime cover, one day at a time.
- **Integrations & partners** — daytime cover, one day at a time.
- **Treasury ops** — daytime cover, one day at a time.

Rotas are maintained in the paging tool by the team lead or a nominated deputy. If you need to swap a shift, arrange it in the team channel and then update the rota yourself — the paging tool lets you swap shifts without needing admin help. If you cannot find a swap, tell the team lead at least two working days before the shift starts.

Check your rota at the start of each month so you know when you are on. The paging tool sends a reminder the day before each shift.

## When you are on call

You are expected to be reachable on your phone and on chat. Keep your laptop with you and charged. If you are leaving the office or going somewhere without signal, set your paging tool status to "unavailable" and make sure the secondary (if your team has one) knows.

When you are paged:

1. **Acknowledge the page** in the paging tool within five minutes. If you do not acknowledge, it escalates to the secondary and then to the team lead.
2. **Read the alert details.** Most alerts include a link to the relevant dashboard or log view. Open it.
3. **Decide if this is something you can handle alone.** Many alerts are routine — a queue backing up, a certificate nearing expiry, a feed that has not delivered. Fix it if you can.
4. **If you need help, page the secondary** (for SRE) or escalate to the team lead (for teams without a secondary). There is no shame in this — better to have two people on a problem early than one person stuck for an hour.
5. **If the issue affects merchants, partners, or internal users, open an incident channel.** See below.

## Opening an incident channel

Use the `/incident` command in the `#incidents` channel. This creates a dedicated incident channel, pages the on-call incident commander, and posts a link to the incident tracker. Name the channel after the service and a short description, for example `#incident-payouts-slow`.

Open an incident channel when:

- A production service is down or degraded for more than a few minutes.
- Merchant payouts, settlements, or card transactions are delayed or failing.
- A partner feed has stopped and the partner has noticed.
- The transaction monitoring system is not processing alerts.
- You believe a security incident may be in progress — when in doubt, open the channel and let the incident commander decide.

Once the incident channel is open, the incident commander takes over coordination. You stay on the call if you are the one who knows the system — otherwise you are free to stand down when the commander says so.

## Escalating to team leads

If you are stuck, escalate. The escalation path is:

1. Your team lead (or the duty team lead for your team).
2. The SRE lead (Ben Whitaker) for anything that spans multiple services.
3. The VP Engineering (Mateo Silva) for incidents that need a decision across engineering teams.

Do not wait for a page to escalate. If you have been working on something for 30 minutes without progress, call the team lead. If the issue is affecting merchants, you do not talk to merchants directly — merchant communication goes through the incident channel.

## Handover notes

At the end of your shift, write handover notes in the paging tool. Cover:

- Anything you worked on during the shift, even if you resolved it.
- Open issues that are still being worked.
- Things the next person should keep an eye on (queues that were backing up, feeds that were late, certificates that are close to expiry).
- Anything you changed during the shift, with the ticket number for it.

Handover notes are visible to your team and to the SRE team. They are not visible to other teams. If something needs to be known beyond your team, post it in the relevant team channel as well.

## On-call allowance

Everyone who carries a 24x7 rota (SRE and payments platform) gets an on-call allowance per week on call. The allowance is paid with the next payroll run after the shift. It is in the payroll calendar — see `finance-docs/payroll/payroll-calendar.md` for the exact dates.

Daytime rotas (payments dev, data platform, integrations & partners, treasury ops) do not attract the allowance — they are covered as part of the role.

If you think your allowance is wrong, raise it with your team lead first, then with Payroll & payables if it is not resolved.

## If it goes wrong

- **You miss a page.** The paging tool escalates to the secondary and then to the team lead. You will get a chat message from the team lead asking what happened. Be honest. Missing a page happens to everyone once — missing several is a problem.
- **You break something while fixing it.** Say so in the incident channel immediately. Do not try to hide it. The incident commander needs the full picture to decide what to do.
- **You do not know what to do.** Say that out loud. Ask for help in the incident channel or call the team lead. Nobody expects you to know everything.
- **The handover notes are missing or thin.** Do not panic. Check the incident channel history and the team channel for context. If there is genuinely nothing, start fresh and write notes for the next person.

## Related documents

- `eng-docs/incidents/incident-process.md` — the full incident process
- `eng-docs/incidents/status-page.md` — status page updates
- `eng-docs/sre/monitoring-and-slos.md` — monitoring and SLOs
- `eng-docs/platform/change-management.md` — change management
- `eng-docs/platform/deploys.md` — deploying with deployctl
