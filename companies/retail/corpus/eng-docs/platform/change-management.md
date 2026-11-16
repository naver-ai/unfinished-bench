# Change management

**Owner:** Release management  
**Last edited by:** Ivan Salazar (Release Coordinator)

## Purpose

This document defines how changes to Mossgrove production systems and services are raised, reviewed, scheduled and recorded. It applies to all production systems operated by the Platform, Checkout, Web, Data, Membership & Billing, and Security engineering teams, and to any change made to the POS back office, the analytics warehouse, or the wholesale order systems.

The goal is to keep a clear record of what changed, who approved it, and when it happened, so that incidents, audits and finance queries can be traced back to a change ticket.

## Scope

In scope: application code releases, infrastructure changes, database migrations, configuration changes that affect production behaviour, feature flag rollouts beyond the initial canary, and changes to standing data that affect more than one store or customer account.

Out of scope: routine operational tasks that are already covered by a runbook (see the on-call guide), code changes that are merged to the main branch but not yet deployed, and changes that are entirely within a development environment.

## 1. Change types

1.1 Every change to production falls into one of three types: **standard**, **normal**, or **emergency**.

1.2 **Standard changes** are low-risk, repeatable actions with a pre-approved procedure. They do not need a CAB review, but they must have a change ticket and must follow the documented runbook. Examples:

- Routine certificate rotation covered by the DNS and platform runbooks.
- Adding a new store to the POS back office using the standard onboarding steps.
- Applying a monthly patch set to the warehouse cluster that has already been validated in the staging environment.
- Enabling a feature flag for a small percentage of users where the rollout plan in the ticket has been approved in advance.

1.3 The list of standard changes is maintained by Release management. If a team believes a procedure should be added, raise a ticket and the Release Coordinators will review it with the owning team and the CAB chair.

1.4 **Normal changes** are everything else. They need a change ticket raised before the change window and, depending on risk, may need CAB approval. Risk assessment is done by the team raising the change using the template in the tickets system.

1.5 **Emergency changes** are raised with the `emergency` change type. Section 5 covers how they are recorded, announced and reviewed.

## 2. Change tickets

2.1 All changes — standard, normal, and emergency — are recorded in the tickets system with the `change` type. The ticket must include:

- What is changing and why.
- The systems affected (using the cost-tag codes where relevant).
- The risk level (low, medium, high) and the rollback plan.
- When the change is planned to start and finish, in UK time.
- Who is making the change and who is the named reviewer.

2.2 Tickets must be raised by the engineer or team lead who will make the change, not by someone else on their behalf, unless that person is on leave and the change has already been agreed.

2.3 A change ticket is considered approved when it has the required approvals (see 3.3) and the scheduled window has been confirmed by the Release Coordinator on duty. The ticket status then shows `Approved`, and the change appears on the change calendar (see 6.4).

2.4 If the planned window moves, update the ticket and tell the Release Coordinator on duty, so the change calendar and the store and support teams have the right time.

2.5 While the change is in progress, add short notes to the ticket as you go: what was done, anything that behaved differently from the plan, and the time you finished. Link any related tickets (the incident, the follow-up change, the request that started it).

## 3. The CAB

3.1 The Change Advisory Board (CAB) meets twice a week, mid-morning UK time. The chair is the Release Manager (currently Dana Whitfield). The Release Coordinators (Ivan Salazar, Bianca Lehmann) maintain the agenda and the minutes. The agenda for each meeting closes at the end of the previous working day; tickets raised after that go on the agenda for the following meeting.

3.2 The CAB reviews normal changes that are flagged as medium or high risk, changes that touch more than one team, and any change that affects store systems during peak trading preparation. Teams are expected to attend the CAB for their own changes; if they cannot, they should send a note via the Release Coordinator before the meeting.

3.3 Approvals:

- Low-risk normal changes: approved by the owning team lead and the Release Coordinator on duty.
- Medium-risk normal changes: approved by the CAB.
- High-risk normal changes: approved by the CAB and, where the change affects customer payments or personal data, by the Head of the owning team (or their deputy).

3.4 CAB minutes are stored in the tickets system against each change. Decisions and conditions are written into the ticket before the change is marked approved.

3.5 If a change is rejected, the ticket is updated with the reason. The team can revise and re-raise it for the next CAB.

## 4. Freeze periods

4.1 There is a change freeze during the peak trading period. The freeze starts at the beginning of the first working day in the week that contains the last working day of November and runs through until the second working day after the New Year bank holiday.

4.2 Release management keeps a freeze-safe list of standard changes for the period. The list is reviewed each quarter before the freeze begins, and the final version is posted in `#releases` a month ahead.

4.3 The freeze applies to:

- Storefront and checkout code changes.
- Order processing and warehouse systems, including the Wakefield DC systems.
- Payment platform changes.
- Membership and billing systems.
- The analytics warehouse if a change would affect order reporting used by finance during the period.

4.4 The freeze does not apply to the GPU lab cluster, the internal product catalogue tooling, or marketing email templates, unless the change would affect order data or customer account data.

4.5 Teams planning work in the freeze period should raise the change ticket at least three working days before the proposed window and bring it to the CAB, so stores and support can be told in good time.

## 5. Emergency changes

5.1 An emergency change is recorded in the tickets system with the `emergency` type and the same details as any other change (see 2.1). Add a line on what makes it urgent and link the incident ticket if there is one.

5.2 Post the ticket number in `#releases` so the Release Coordinators can put it on the change calendar, and in `#incidents` if it belongs to an open incident. Support and store operations take their updates from those two channels.

5.3 Emergency changes are reviewed at the next CAB. The team who made the change presents what happened and whether any follow-up is needed.

5.4 An emergency change does not make the underlying fix permanent. A follow-up normal change must be raised within five working days to make the fix permanent and to update the relevant runbook or configuration documentation.

## 6. Scheduling and windows

6.1 Normal changes should be scheduled in the agreed change windows:

- Storefront and checkout: early morning on the middle three working days of the week, UK time.
- Order processing, back-office and warehouse: evening on any working day.
- Wholesale and finance systems: late afternoon on any working day.

6.2 Changes that affect the POS back office should not be scheduled during store opening hours on a bank holiday period.

6.3 If a change runs past its planned window, note in the ticket where it got to and post an update in `#releases`.

6.4 The Release Coordinators keep a change calendar of the approved and scheduled changes for the next two weeks, built from the tickets system, and post it in `#releases` at the start of each week. They flag anything that touches stores in `#stores-ops` and anything customer-facing in `#support-leads`. Storefront build dates are announced in `#releases` as well.

## 7. Records and retention

7.1 Change tickets are kept for six years after the change is closed, in line with the records retention policy.

7.2 The Release Coordinators produce a monthly summary of changes for the engineering leadership team, including the number of emergency changes and any changes that overran their window.

7.3 Any change that caused an incident must link to the incident ticket, even if the incident was minor and resolved quickly.
