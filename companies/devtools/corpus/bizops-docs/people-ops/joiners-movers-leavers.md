# Joiners, movers and leavers

Owner: People operations · Last edited by Ibrahim Santos

This page describes what People ops does when someone joins, moves teams, or leaves Gantline. It covers both employees and contractors. If you are a manager, most of what you need is in [the manager onboarding checklist](/handbook/people/onboarding-for-managers.md); this page is the ops view.

## Joiners

1. The hiring manager submits the offer acceptance in the HR system. People ops gets a task automatically.
2. People ops creates the employee record in the HR system with:
   - start date, job title, team, manager, office (Lisbon or Portland, or remote),
   - salary and equity from the signed offer,
   - personal details from the onboarding form.
3. People ops sends the IT ticket for kit and accounts. The ticket asks for:
   - a laptop and any other hardware per the device policy,
   - an account in the identity provider, assigned to the right groups for the team,
   - access to chat, the company email platform, the HR system, the expense tool, the password manager, and the customer orgs in the Gantline Cloud admin console that the role needs.
4. For Lisbon hires, People ops also starts the Portuguese paperwork (contract, social security registration, benefits enrolment). For Portland hires, the US entity (Gantline Inc.) is set up through payroll.
5. The HR system sends the welcome email with the start date and office information. It also schedules the first-day tasks in the manager checklist.
6. On the start date, the employee completes a few HR system forms (bank details, emergency contact, tax forms). People ops checks that the IT ticket is done and the accounts work.
7. Contractor joiners are set up the same way, but with a contractor record in the HR system instead of an employee record. The contract is uploaded to the record, and the end date is set from the contract. Contractor IT access is scoped to the engagement; the IT ticket must state the end date.

## Movers

1. The manager or the employee requests the move in the HR system. The request needs the new team, new manager, and the effective date.
2. People ops updates the HR system record: team, manager, office if relevant, and any compensation changes tied to the move.
3. People ops sends an IT ticket for access changes:
   - remove access to systems and repos the old team used (as listed in the team's service catalogue entry),
   - add access for the new team,
   - update the Gantline Cloud admin console org memberships if the person changes customer-facing teams.
4. If the move is between offices (Lisbon to Portland or the reverse), People ops coordinates with IT for a new laptop and with the office team for a desk. The working-across-offices page has the practical details.
5. The HR system notifies payroll of any compensation changes. For moves that cross the employee/contractor boundary, see the contractor section below.
6. A contractor whose contract is extended gets their end date updated in the HR system. The contract amendment is uploaded to the record.

## Leavers

1. The manager tells People ops in the HR system, with the last working day. For contractors, the end date is already in the HR system; People ops confirms it with the manager about two weeks before it arrives.
2. People ops sends the IT ticket for account closure:
   - disable the identity provider account on the last working day,
   - collect the laptop and any other hardware,
   - remove access to the password manager, the HR system, the expense tool, the CRM, chat, the helpdesk, the Gantline Cloud admin console, and any customer orgs,
   - revoke the VPN certificate.
3. People ops schedules the exit interview. Exit interviews are done by People ops, not the manager.
4. On the last working day:
   - the HR system record is set to terminated with the leaver reason,
   - payroll is notified (final salary, accrued but unused leave, severance if applicable),
   - the IT ticket is marked done once the laptop is returned and the accounts are closed,
   - access to the office (badge, door codes) is revoked.
5. The manager gets a short checklist from the HR system: handover of work, transfer of code ownership, removal from on-call rotations and distribution lists.

## If it goes wrong

- HR system record was created with the wrong start date: fix the record immediately and check whether the IT ticket and welcome email were sent with the wrong date. If they were, tell IT and the manager; do not let the employee show up without a laptop.
- IT ticket is still open on the start date: escalate to #it-help with the ticket number. The employee can start with a temporary account but must get their real kit within the first working day.
- A mover keeps access to an old system: the IT ticket must list every permission to remove. If you are not sure, ask the old team lead. It is better to remove too much and add back than to leave a stale repo access.
- A leaver's account is still active after the last working day: contact IT immediately. The account must be disabled the same day.
- Contractor end date passes but the contract was extended after the fact: People ops updates the HR system with the extension date and confirms with IT that access was not interrupted. If access was interrupted, the contractor's manager must re-request it.
