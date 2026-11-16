# Joiners, movers and leavers

**Owner:** Identity & access  
**Last edited by:** Chloe Schmidt (Identity Engineer)

## Joiners

1. The HR system creates the base account record the night before the start date. The joiner appears in the identity source with their legal name, personal email, start date, cost centre and manager.
2. Identity & access runs the nightly provisioning job. It creates the network account, mailbox, home drive and entries in the ERP, MES, CMMS and the rest of the connected systems.
3. The line manager requests role-based access via the service desk portal using the ticket type "Joiner – role access". The ticket must reference the HR system employee ID. The manager selects from the standard role bundles:
   - **Manufacturing (Reutlingen/Telford/Greenville):** MES shop-floor terminal login, CMMS view, time-recording terminal PIN.
   - **Engineering:** PLM read/write, firmware repo access via the monorepo group, test lab calendar.
   - **Office/finance/purchasing:** ERP, expenses app, supplier portal (read), document shares.
4. Access bundles are granted automatically by the identity provisioning workflow. Anything outside the bundles (e.g. a buyer needing ERP purchase-order approval rights) goes through the normal access request in the service desk portal and is approved by the relevant team lead.
5. The joiner collects their badge from reception on the first day. Factory staff also get their time-recording terminal card from the shift lead.

## Movers

1. When a team change is entered in the HR system, the provisioning job removes the old team's role bundles and adds the new ones. This runs on the effective date.
2. The employee keeps their primary account, mailbox and employee ID. Their home drive is not moved.
3. Shared drives are handled by the manager: the losing team lead raises a ticket to remove access, the gaining team lead requests the new access. Both happen via "Mover – access change" in the service desk portal.
4. If the move is between sites (Reutlingen ↔ Telford ↔ Greenville), the badge is reissued at the destination. The time-recording terminal assignment follows the site change.
5. The factory IT team in the destination site should be copied on the ticket so the MES terminal profile follows the person.

## Leavers

1. The HR system flags the leaving date. On the last working day, the nightly job disables the account at the end of the day.
2. The following items happen automatically:
   - Network login disabled, mailbox converted to shared and assigned to the line manager.
   - Access to ERP, MES, CMMS, PLM, expenses app and supplier portal revoked.
   - Badge deactivated.
3. The line manager is responsible for collecting the laptop, phone and any site keys, and for raising a "Leaver – equipment return" ticket in the service desk portal.
4. The manager can request a mail redirect for customer-facing roles for up to 30 days. This is done via the ticket "Leaver – mail redirect".
5. The mailbox is archived via mailarchctl after the redirect period and kept per the retention schedule.

## Contractors

1. Contractor accounts are created the same way as joiner accounts, but the HR system record includes an end date.
2. The account is automatically disabled on the end date. There is no grace period.
3. Extensions must be entered in the HR system before the end date. If the extension is entered after the account is disabled, the account is re-enabled the next night and the contractor is told to re-authenticate.
4. Contractor access bundles are the same as for employees in the same role. The hiring manager is the sponsor and approves access changes via the service desk portal.

## If it goes wrong

- Account not created on the start date: check the HR system record first (employee ID present? cost centre set?). If the record is fine, check the provisioning job log in the identity source. Raise an "Identity – joiner issue" ticket if the job failed.
- Account disabled but the leaver is still on site: contact Identity & access. The leaver's badge may still work for door access even after the account is disabled — this is expected and is handled by the site security team.
- Contractor account disabled early: verify the end date in the HR system. If correct, the account stays disabled. If incorrect, the HR system record must be corrected, then Identity & access can re-enable the account manually.
- Access not removed after a mover: check whether the losing team lead raised the removal ticket. The automatic part only covers the role bundles; anything added manually stays until it is removed manually.
