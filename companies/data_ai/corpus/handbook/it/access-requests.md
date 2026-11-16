# Getting access to systems (people accounts)

**Owner:** IT and workplace  
**Last edited by:** Mehmet Dahl (IT Manager)

This page covers how to get a people account created, changed, or removed for Brakwater systems. It only covers accounts for people — staff and contractors. System accounts and service identities are a separate process — see `platform-docs/security/service-accounts.md`.

## Requesting a new account or access change

1. Go to the IT service desk and open a request using the **"People access"** form.
2. Fill in:
   - the person's full name and email address (for a new starter, use their @brakwatergeo.com address; for a contractor, use their company address if they don't have a Brakwater one yet)
   - the systems they need (see the system list in the form)
   - their start date (or the date access should become active)
   - their line manager's name
3. The form routes the request to the line manager for approval. Once the line manager approves, the request goes to the system owner for each system on the list. The system owners are:
   - **Catalogue, tasking portal, customer API console** — Imagery acquisition and processing
   - **Warehouse** — Analytics warehouse (Owen Gallagher is the current owner)
   - **BI dashboards** — BI and reporting
   - **Notebook server, workflow scheduler** — Data engineering
   - **Model serving, modelhub** — ML platform (Bo Vasquez is the current owner)
   - **Field app** — Sensor network
   - **CRM** — Customer success and delivery
   - **Helpdesk** — Support systems
   - **Everything else** (chat, email, docs, office tools) — IT and workplace
4. The IT team creates the account once all approvals are in. You'll get a confirmation in the ticket when it's done. New starters normally get their accounts before their first day; if the request is approved late, the IT team will prioritise the essentials (email, chat, docs) and do the rest within a working day.

## Temporary access for contractors

Contractors get the same process as staff, with two differences:

- The request must include an **end date**. Access is set to expire automatically on that date.
- The line manager is the person at Brakwater who is responsible for the contractor's work. They approve the request the same way.

If a contractor needs access beyond the original end date, open a new request (or reply to the original ticket) with the updated end date. Do not wait until the day access expires — the IT team needs at least a couple of working days to process an extension.

## Changes to access

- **Role changes** — when someone moves teams, the new line manager opens a "People access" request for the systems they need. The old manager is responsible for removing access to systems the person no longer needs. The IT team sends a reminder to both managers when a role change is recorded in the HR system.
- **Transfers between offices** — access carries over. The workplace coordinator (Jakob Molina) arranges the local bits (badge, desk, equipment).
- **Lost or forgotten passwords** — use the password manager or the self-service reset on the sign-in page. If that fails, contact the IT service desk.

## Leavers

When someone leaves, the IT team runs the leavers checklist automatically once the HR system flags the end date. The checklist covers:

1. Disable the main account (email, chat, docs) on the last working day.
2. Revoke access to all systems where the person was a direct user (catalogue, warehouse, notebook server, CRM, helpdesk, field app, and so on).
3. Remove the person from distribution lists and shared mailboxes.
4. Forward their email to their manager (the manager should set this up in advance via the IT service desk).
5. Hand over any company devices — the IT team contacts the leaver's manager to arrange the return.

If a leaver has been a system owner or has a role on a service account, the IT team notifies the team that owns the system so they can reassign ownership before the account is disabled.

## If it goes wrong

- **Access is missing on day one** — check the ticket first. If the approvals are all in and the account was created, open a chat message to #it-help with the ticket number. The IT team will sort it same day.
- **Access is still active after someone has left** — tell the IT team immediately via #it-help or the IT service desk. The leaver's manager should also check their team's access lists after a departure.
- **Someone has access they shouldn't** — report it to the IT team and your manager. The IT team will review and remove it, and if it looks like a security issue, they'll follow the incident reporting process in `handbook/security/incident-reporting.md`.
