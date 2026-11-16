# Incident process

**Owner:** Platform & SRE  
**Last edited by:** Laszlo Ikeda (Platform Engineer)  
**Status:** Current

---

## Purpose

This document describes how we respond to incidents affecting Mossgrove systems, who does what, and what we expect from teams when something breaks. It applies to production systems that serve customers, stores, wholesale partners, or internal finance operations.

If you are unsure whether something is an incident, treat it as one and raise it in #incidents.

---

## Severity levels

| Severity | Definition | Examples | Response expectation |
|----------|------------|----------|----------------------|
| **SEV-1** | Customer-facing service unavailable or data loss risk. Major financial impact. | Shop front page down across regions; checkout failing for all customers; payment capture failing; warehouse management system down during dispatch window. | Immediate. Incident commander assigns leads. Updates in #incidents every 30 minutes or less. CTO informed. |
| **SEV-2** | Significant feature degraded or partial outage. Affects a subset of customers or one channel. | Order confirmation emails not sending; US storefront slow; gift card balance lookups failing; wholesale order portal errors. | Respond within the working day. Incident commander assigned. Updates at least hourly. |
| **SEV-3** | Minor disruption, workaround exists, or internal-only impact. | Reporting dashboard lagging; search relevance noticeably worse after a release; internal tool slow for finance ops. | Normal support channels. Fix in the next few working days. No incident commander required. |

Severity can change as we learn more. Don't argue about the level while the thing is still broken — pick the higher level, fix it, then downgrade if appropriate.

---

## Roles

**Incident commander (IC):** The single person coordinating an incident response. Usually the first Platform & SRE person on the call or in #incidents takes this on, and can hand over to someone else. The IC:

- Confirms the severity and announces it in #incidents
- Assigns a lead for each affected area (checkout, orders, payments, store systems)
- Decides when we need to involve other teams (Finance, Retail Operations, Wholesale)
- Keeps the timeline in the incident channel — put timestamps in the thread, don't rely on memory
- Declares the incident resolved and makes sure the post-incident review is scheduled

The IC is **not** expected to fix the problem themselves. Their job is coordination.

**Subject matter expert (SME):** The person who knows the affected system. They investigate, propose fixes, and communicate progress to the IC. SMEs change as the incident evolves — that's fine, the IC tracks who is doing what.

**Comms lead:** For SEV-1 and any incident that affects stores or wholesale partners, the IC nominates someone to handle external updates. This is usually from Customer Support leadership or Retail Operations. That person:

- Posts updates to #support-leads and #stores-ops
- Drafts the customer-facing message if one is needed (see `handbook/comms/writing-to-customers.md`)
- Keeps the IC informed of what has been said externally

---

## Communication

### In the moment

All incident discussion happens in the **#incidents** channel or a dedicated incident thread off it. Do not use #general or team channels for active incident coordination — people filter by channel and will miss updates.

| Audience | Channel | What they need |
|----------|---------|----------------|
| Engineering and platform staff | #incidents | Technical status, affected services, who is working on what |
| Support leads | #support-leads | What to tell customers, expected resolution time if known |
| Stores operations | #stores-ops | Whether stores can serve customers normally, whether to use fallback processes |
| Wholesale | #wholesale | Whether order portal is affected, whether wholesale dispatch is delayed |
| Finance operations | #finance-ops | Payment capture/reconciliation impact, anything affecting month-end or banking |
| Everyone | #general | Only if it affects the whole company (e.g. email down, VPN issues). Keep this to one or two posts. |

**If the incident affects customer orders or payments, the support desk must be told before customers start asking.** Post to #support-leads as soon as you know the scope, even if you don't have details yet.

**If it affects store systems** (POS back office, store networks, card readers), post to #stores-ops immediately. Stores can work offline for a while but need to know whether to keep taking payments or switch to manual processes.

### Status updates

- SEV-1: update #incidents at least every 30 minutes, even if the message is "no change, still investigating"
- SEV-2: update when something changes, but at least once per hour
- Always include: affected service, current impact, next action, who is doing it

### After resolution

Post a short summary to #incidents within a couple of hours of resolving, even before the full review is written. Include:

- What happened (one or two sentences)
- When it started and when it was resolved
- Customer impact in plain terms
- Link to the post-incident review when it's ready

---

## Working with the support desk

The outsourced desk does not need technical detail. They need to know:

- What to tell customers who call (script or key points)
- Whether refunds or goodwill gestures are being offered
- When they can expect an update

Amir Agarwal or the support leads on duty can help craft the customer-facing messaging. Do not let the desk improvise — inconsistent messages make things worse.

---

## Post-incident review

Every SEV-1 and SEV-2 incident gets a post-incident review. SEV-3 incidents can skip it unless they keep recurring or the team wants one.

The review is a short markdown document added to the folder for the owning team (e.g. `eng-docs/incidents/` or wherever the team keeps them). The IC owns writing it, with input from the SMEs.

Required sections:

| Section | What goes in it |
|---------|-----------------|
| **Summary** | What happened, when, how long, who was affected |
| **Timeline** | Key events with timestamps — detection, escalation, mitigation, resolution |
| **Root cause** | What actually caused it. It is fine to state "unknown yet" if that is true, but say what is being done to find it |
| **Impact** | Customers, stores, wholesale, finance. Include numbers if known (orders affected, refunds issued, revenue impact) |
| **Actions** | Each action must have an owner and a target date. Use `data-docs` or the team tracker to track them — the review is the record, not the tracker |
| **What went well** | Be honest. If someone caught the issue quickly, say so |
| **What went badly** | Also be honest. No blame, but if coms were slow or monitoring missed it, say that |

The review should be circulated in #incidents and to the relevant team channel. The CTO (Siobhan Keane) sees SEV-1 reviews.

Actions from reviews are followed up at the next Platform & SRE meeting. If an action has no owner or no date, it is not an action.

---

## Things that are not in this document

For change management and deployment approvals, see `eng-docs/platform/change-management.md`. For on-call expectations, see `eng-docs/oncall/oncall-guide.md`. For security incidents, follow `handbook/security/incident-reporting.md` — they take precedence over this process.
