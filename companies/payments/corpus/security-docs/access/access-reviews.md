# Quarterly access reviews

Owner: Governance, risk & controls testing. Last edited by Isaac Chowdhury (Head of GRC).

Quarterly, GRC coordinates access reviews across production and internal systems. Each review covers a rolling subset per the review tracker; every system is reviewed at least once per year. The tracker lives in the GRC folder in the back office, and the current quarter's assignments are pinned in #security.

## What we review

1. **Core systems** — the core ledger, treasury workstation, reconciliation tool, transaction monitoring system, KYB onboarding tool, and the case tool. Access is reviewed by the owning team (Payments platform for the ledger, Treasury & settlement for the treasury workstation, Financial crime for transaction monitoring, the case tool and the KYB onboarding tool, Finance operations for the reconciliation tool).
2. **Platform and infrastructure** — cloud accounts, deployctl, the secrets manager, and the command-line tools each team uses to run its services. Each is reviewed by the team that runs it; the tracker lists the reviewer per tool.
3. **Merchant-facing tools** — the back office and the merchant dashboard (reviewed by Merchant apps with Merchant success), and the CRM (reviewed by Revenue operations).
4. **Reporting** — the analytics warehouse (reviewed by Data platform) and the regulatory returns portal (reviewed by Regulatory reporting).

## Running a review

1. Open the review tracker and take the assignments for your system. Each row lists the system, the reviewer team, and the due date (two working days before the quarter's control testing close-out).
2. Export the current access list from the system. For the back office and merchant dashboard, use the access report in the admin menu; for deployctl, use `deployctl members list`; for the ledger and treasury workstation, use the access view in the back office.
3. Compare the export against the team's current roster in the HR system. Flag anyone who has left, changed teams, or has not signed in to the system in the last two quarters.
4. For each flagged account, send the account holder's manager a note through the helpdesk asking them to confirm whether access is still needed. Managers have five working days to respond.
5. Revoke stale access using the system's normal removal path — for most systems that is removing the user from the relevant group in the back office, and for the secrets manager it is deleting the user's account.
6. Record the outcome in the tracker: date of review, reviewer name, accounts removed, and any manager responses. Link the review row to the change ticket if a removal needed a change request (for example, removing a service account from the core ledger).

## Evidence for auditors

The review tracker is the primary evidence for PCI DSS and SOC 2 access reviews. Each quarter, GRC exports the tracker to PDF and stores it in the audit-evidence folder in security-docs. Make sure the tracker row shows the reviewer's name and the review date — auditors will ask for both.

## If it goes wrong

- If a manager disputes a removal, restore the access within one working day and note the dispute in the tracker.
- If a review is going to miss its due date, tell the GRC team in #security as early as possible so we can rebalance assignments.
- If you find an account that appears to be active but the person is unknown, do not remove it on your own. Raise it in #security and let GRC decide with the system owner.
- If the export fails or the system is down, record the outage in the tracker and retry the next working day. Do not mark the review complete without the export.
