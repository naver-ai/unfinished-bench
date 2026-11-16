# Quarterly access reviews

Owner: Security engineering · Last edited: Kai Silva (GRC Analyst)

Scope: all Mossgrove systems listed in the access request handbook, plus the POS back office and the wholesale CRM portal.

## Review cycle

1. Each quarter, Security engineering publishes a tickets ticket titled `Access review — Q<n> <year>` and assigns it to the system owner named in the access request handbook. Owners confirm or revoke access for their system.
2. Owners run the review using the system's own user list export (ask the system owner for the export if you don't have admin access; for the POS back office and CRM, the admin export in the back office).
3. For each user, confirm:
   - still in their current role (check the HR system if unsure);
   - their access matches the role's baseline in the access request handbook;
   - no accounts are shared between staff, stores, or the wholesale team.
4. Revoke anything stale. For deprovisioning use the standard offboarding flow in the HR system — do not delete the account in the target system first, or the HR system will error.
5. Leave a comment on the tickets ticket with the export filename, the date the export was taken, and anything you revoked. This is the audit evidence.
6. Security engineering spot-checks a sample of system exports against the HR system list of leavers and internal movers. The sample size is 10% of active named accounts, rounded up.

## Removing stale access outside the quarterly cycle

If you notice a user who has left or moved roles mid-quarter (e.g. from a store to the wholesale team), raise an `Access` ticket in tickets and deprovision through the HR system the same working day. Do not wait for the next quarterly review.

## If it goes wrong

- If you revoke the wrong user: re-grant via the HR system immediately, then flag to the system owner in the tickets ticket so they can confirm nothing else was affected.
- If a user reports they cannot log in after a review: check the HR system first for a pending role change, then check the system's audit log. Most cases are a role move that the manager forgot to submit.
- If the export from a system is empty or incomplete: do not proceed. Raise a `Platform` ticket for the system owner and note it on the quarterly tickets ticket.

Questions about scope go to #security. Store and wholesale access questions go to #stores-ops or #wholesale respectively.
