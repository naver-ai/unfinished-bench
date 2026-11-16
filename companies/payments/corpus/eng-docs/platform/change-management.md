# Change management

**Owner:** Developer platform & releases  
**Last edited by:** Abel Larsen (Build Engineer)  
**Applies to:** All production and production-adjacent systems, including the core ledger, the payments bus, the merchant dashboard, the back office, partner-facing services, and internal tooling that handles merchant or financial data.

## Purpose and scope

This page defines the change types used at Kilbarra, what a change ticket must contain, and the approval path for each type. It also covers the change advisory board (CAB) and the peak-season freeze.

Emergency changes are described in the runbook of the service concerned. This page covers only the paperwork that follows one.

## Change types

1. **Standard change** — a pre-approved, low-risk change that follows a documented procedure. No CAB review needed per instance.
   1.1. Standard changes must have a runbook or checklist in the owning team's repository, and must have been through at least two successful executions before they can be registered as standard.
   1.2. The list of registered standard changes is maintained by Developer platform & releases. To add or retire one, raise a ticket in tickets with the category `standard-change` and attach the procedure.
   1.3. Examples of current standard changes: routine patching of non-financial internal services, onboarding a new log source to the SIEM, renewing certificates for services already on automated renewal, adding a DNS record for a merchant's custom checkout domain.

2. **Normal change** — a change that is not standard and not emergency. Requires a change ticket approved in tickets by the approver set in the ticket's approver field for the affected system.
   2.1. Low and Medium risk normal changes are approved in the ticket. High risk normal changes also go to the next CAB meeting before their window.
   2.2. Normal changes should be submitted at least three working days before the intended window so the CAB has time to review.

3. **Emergency change** — a change made through a service's own emergency path, as described in that service's runbook.
   3.1. The person making the change opens a change ticket in tickets with category `emergency` and completes the retrospective fields described in section 7.

## Change ticket contents

4. Every change ticket in tickets (standard, normal, or emergency) must contain:

   4.1. **Description** — what is changing, which service or system, which environment, and the expected effect. Include the relevant ticket or incident number if the change is linked to one.
   4.2. **Risk level** — Low, Medium, or High. If the change touches the core ledger, the payments bus message store, settlement or payouts, the risk level is at least Medium.
   4.3. **Rollback plan** — the specific steps to undo the change, or a statement of why rollback is not possible and what mitigation is in place instead. A rollback plan that says "restore from backup" must name the backup set and the restore procedure (see eng-docs/platform/backups.md).
   4.4. **Window** — the proposed start and end time, and the business justification for that window. For normal changes, the window should avoid the bank file cut-off and the end-of-day settlement window unless the change is about those systems and has been coordinated with Treasury Operations.

4.5. Normal and emergency change tickets must also name:
   4.5.1. The change owner (the person accountable for the change).
   4.5.2. The implementer (who will press the button), if different.
   4.5.3. The systems affected, using the system names from the inventory in eng-docs/architecture/overview.md.
   4.5.4. Whether merchant-facing communication is needed (see merchant-docs/comms/writing-to-merchants.md).

## Change advisory board

5. The CAB meets twice a week, on a fixed schedule published in the team calendar. Meetings are open to anyone at Kilbarra; attendance is expected for anyone with a High risk change on the agenda.

   5.1. Standing members:
   - Developer platform & releases (Engineering Manager or a nominated Build Engineer) — chair
   - A representative from Merchant payments
   - A representative from Infrastructure
   - A representative from Security (the security team nominates who attends)
   - A representative from Merchant operations desk
   - A representative from Treasury operations when the change touches settlement, payouts, safeguarding, or anything that moves money or affects the bank file cut-off

   5.2. The CAB may co-opt additional members for a specific change (for example, someone from the data lake team for a change to lake pipelines, or someone from Regulatory reporting for a change that touches return data).

   5.3. CAB decisions are recorded in the change ticket. A normal change is approved only when the ticket shows an explicit approval decision. Silence is not approval.

## Peak-season freeze

6. The peak-season freeze covers the late-November shopping peak through the year-end merchant peak. The exact start and end dates are published each year by Developer platform & releases at least two weeks before the freeze starts.

   6.1. During the freeze, normal changes to the following are not approved unless the CAB grants an explicit exception:
   - The core ledger and the payments bus message store
   - Settlement and payouts, including anything that touches the treasury workstation or the bank file cut-off
   - The merchant dashboard and the back office
   - The payments gateway and hosted checkout
   - The transaction monitoring system

   6.2. Standard changes continue during the freeze if they are on the registered list and do not touch the systems listed in 6.1. If a standard change touches one of those systems, it is treated as a normal change during the freeze.

   6.3. The paperwork for emergency changes in section 7 is the same during the freeze.

   6.4. The freeze does not apply to changes that are purely additive monitoring, read-only reporting, or documentation.

## Emergency change paperwork

7. Any emergency change must have a retrospective ticket in tickets within two working days of the change being executed.

   7.1. The retrospective ticket must contain:
   - The change ticket number from the emergency action
   - What happened, in plain language
   - What the emergency path was (which runbook or tool was used)
   - Whether the rollback plan was executed, and if not, why not
   - What the CAB should know when it reviews the change

   7.2. The retrospective is reviewed at the next CAB meeting. The CAB will decide whether the emergency classification was appropriate and whether any follow-up work is needed (for example, turning the emergency change into a standard change if it happens often, or adding a control to prevent recurrence).

   7.3. If the emergency change touched the core ledger, settlement, payouts, or the transaction monitoring system, a representative from the relevant team must attend the CAB review in person. A comment in the ticket is not sufficient.
