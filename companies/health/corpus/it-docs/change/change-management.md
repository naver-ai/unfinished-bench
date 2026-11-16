# Change management

**Owner:** Infrastructure & SRE  
**Last edited by:** Lucia Barros (Storage Engineer)

## Purpose

This document defines how changes to Kellsbrook Health production systems and infrastructure are planned, reviewed, approved, and recorded. It applies to all IT-operated systems, including the EHR, claims adjudication system, interface engine, data warehouse, and the platforms managed by Infrastructure & SRE. Clinical and research teams making changes to their own applications or study records should follow their departmental change processes.

## Scope

Applies to any modification, addition, or removal that could affect the availability, integrity, or security of a production service. This includes configuration changes, code deployments, infrastructure changes, and data migrations.

## Change types

1. **Standard change** — A low-risk, pre-approved, repeatable change with a documented procedure and known outcome. These do not require CAB review but must still be logged as change tickets.

   1.1 Examples: adding a storage bucket for an existing application, adding a DNS record for an internal service, adding a user to a security group, applying a routine OS patch to a non-clinical server, rotating a certificate on an internal service.

   1.2 Standard changes must have a documented procedure referenced in the change ticket. If the procedure does not exist, the change must be raised as a normal change.

2. **Normal change** — A change that carries some risk or requires coordination across teams. These are reviewed by the Change Advisory Board (CAB).

   2.1 Examples: EHR version upgrades, interface engine connection changes, claims adjudication system configuration updates, data warehouse schema changes, network firewall rule changes, storage array firmware updates, load balancer pool changes.

   2.2 Normal changes require a change ticket with a completed risk assessment, implementation plan, rollback plan, and testing summary before they can be scheduled for CAB review.

3. **Emergency change** — A change required to resolve a major incident or prevent imminent impact to patient care, member services, or revenue operations. These bypass the normal CAB timeline but still require approval and must be reviewed retrospectively.

   3.1 Examples: applying an emergency security patch to a compromised system, restarting a failed interface engine process with a configuration fix, restoring service by failing over storage that is degrading.

   3.2 Emergency changes may be approved by the Infrastructure Manager (or their deputy) and the relevant system owner. The change must be logged in tickets immediately, and the CAB reviews it at the next scheduled meeting.

   3.3 Emergency changes made outside of regular working hours are approved by the on-call lead and the duty manager. The on-call lead notifies the Infrastructure Manager before the end of the next working day.

## Change ticket fields

4. Every change must have a ticket in tickets with the following fields completed:

   4.1 **Title** — Short description of what is changing.

   4.2 **Change type** — Standard, normal, or emergency.

   4.3 **System(s) affected** — List the systems from the service catalogue. If the change touches more than one system, list all of them.

   4.4 **Planned start and end** — The maintenance window. Clinical systems have priority windows outside of regular clinic and practice hours unless otherwise agreed with the relevant operational team.

   4.5 **Risk level** — Low, medium, or high, based on the risk assessment matrix in the IT risk register.

   4.6 **Impact** — Which sites, teams, or member populations could be affected. For example, a change to the claims adjudication system should note whether it impacts the claims payment queue and which site (Valparaiso or South Bend) runs the affected process.

   4.7 **Implementation steps** — Ordered steps describing what will be done.

   4.8 **Rollback plan** — How the change will be reversed if it fails. If no rollback is possible, say so explicitly and explain why.

   4.9 **Testing completed** — What testing was done before the change. For standard changes, reference the documented procedure.

   4.10 **Communications plan** — Which channels will be used to notify affected teams. Use the relevant chat channels (for example, #his-platform for EHR changes, #claims-ops for claims system changes, #infrastructure for network or storage changes).

   4.11 **Reviewer(s)** — Required for normal and emergency changes.

## Change Advisory Board

5. The CAB meets twice a week to review normal changes. Changes should be submitted at least one working day before the meeting so they can be circulated in advance.

   5.1 CAB membership includes: Infrastructure Manager (chair), a representative from Infrastructure & SRE, a representative from the service desk, the clinical systems team lead, a representative from the affected business area (for example, Claims operations for claims system changes, Nursing informatics for EHR changes), and a representative from Security.

   5.2 CAB decisions are recorded in the change ticket. A change may be approved, approved with conditions, returned for more information, or rejected.

   5.3 If a change is approved with conditions, the conditions must be met before implementation. The CAB chair is responsible for confirming conditions are satisfied.

   5.4 The CAB may delegate approval of low-risk normal changes to the Infrastructure Manager and the relevant system owner, to be reported at the next meeting. This delegation is reviewed each quarter.

## Change freezes

6. A change freeze means no normal or standard changes may be implemented during the freeze period, except emergency changes that are required to resolve a major incident or prevent imminent patient harm.

   6.1 **EHR upgrade freezes** — A freeze is in effect from two working days before an EHR upgrade until three working days after the upgrade has been completed and verified. The clinical systems team announces the freeze dates on #his-platform and #nursing-leaders.

   6.2 **Open enrollment freeze** — A freeze on changes to the member portal, the claims adjudication system, and the prior authorization queue is in effect during the open enrollment period for individual and {{MANAGED_PLAN_PROGRAM}} plans. The freeze begins on the first working day of the enrollment period and ends after the enrollment deadline has passed and the first enrollment file has been processed successfully.

   6.3 During a freeze, standard changes that are classified as urgent maintenance (for example, security patches for known active vulnerabilities) may be submitted to the CAB chair for approval. The chair consults with the affected system owner before making a decision.

   6.4 The Infrastructure & SRE team maintains a shared calendar with all planned freezes for the current quarter. Any team planning a change that falls within a freeze should contact the Infrastructure Manager to discuss options.

## Implementation and recording

7. Changes are implemented only after the change ticket is approved and the planned start time has been reached.

   7.1 The implementer updates the change ticket with the actual start and end times, any deviations from the implementation steps, and the outcome.

   7.2 If a change fails or needs to be rolled back, the implementer updates the ticket with what happened, and a follow-up ticket is raised to investigate the cause and determine whether a new change is needed.

   7.3 Post-implementation review for medium- and high-risk changes is conducted within three working days. The review is recorded in the change ticket and identifies any follow-up actions.

## Related documents

- IT on-call guide (it-docs/oncall/oncall-guide.md)
- Major incident process (it-docs/oncall/major-incidents.md)
- Backups and restores (it-docs/infra/backups.md)
- Clinical workstations and badge tap (it-docs/servicedesk/clinical-workstations.md)
