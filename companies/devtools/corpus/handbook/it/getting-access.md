# Getting access to systems

**Owner:** IT & workplace tech  
**Last edited by:** Alana Rahman (IT Manager)

This covers how to get access to Gantline's internal systems, who approves what, and what happens to access when your role changes.

## Requesting access

1. Open the service desk form from the IT help channel bookmark or at `go/access-request`.
2. Pick the system you need from the app catalogue. The catalogue lists every internal system with its owner team and the access level each role normally gets.
3. Add your line manager as the approver. The form sends the request to them first.
4. Once your line manager approves, the system owner's team gets a ticket. They grant access or reply with a reason it can't be granted. Most requests are done within one working day.
5. You'll get a confirmation in chat from the IT helpdesk when access is live. If the system uses SSO, it's usually immediate after the owner team acts.

Some systems need a second approval from a specific team, not just the owner — for example, production cloud console access also goes to Site reliability, and the restricted schemas in the data warehouse also go to Data platform. The form shows these extra approvers when they apply.

## Temporary access for a project

If you need access for a short-lived piece of work (an incident, a migration, a trial of a tool):

1. Request through the same form and choose "temporary" as the duration.
2. Set an end date. The system owner grants access with that expiry; it's revoked automatically.
3. If you need an extension, open a new request before the current one lapses — don't ask IT to move the date on the old ticket.

Temporary access is for a named piece of work. Don't use it to get around the normal approval flow, and don't share credentials with anyone else. If a colleague needs the same access, they file their own request.

## Moving teams or leaving

When you change teams, your line manager or the new manager opens a movers ticket in the HR system. That triggers the access review:

- **Moving teams:** your old team's system access is revoked on the effective date. Your new team's access is granted when their onboarding checklist is done. If you need overlapping access for a handover, your old and new managers agree on it and note it in the movers ticket — the default is no overlap.
- **Leaving:** all access is revoked on your last working day. The IT helpdesk runs the offboarding list from the HR system; the admin console, the CRM, the helpdesk, the paging tool, the cloud consoles and the rest are all covered. If you're a US customer-facing role, Gantline Inc. access is revoked the same day.

## If it goes wrong

- **Approval stuck:** ping the approver in chat. If they're out, the system owner team can step in for a single working day's delay.
- **Access not working after approval:** check the app catalogue for any note about VPN or IP allow-listing, then ask in `#it-help`.
- **Wrong access level:** reply on the ticket and the system owner adjusts it. Don't try to escalate through the system itself.
- **Urgent access during an incident:** the on-call engineer can request temporary access via the incident channel and the system owner team grants it immediately, but the normal form request still has to be filed afterwards.

For anything not covered here, ask in `#it-help` and someone from IT & workplace tech will pick it up.
