# Passwords and sign-in

Owner: Security engineering · Last edited by Emma Arslan

## Password manager

- Every Mossgrove account must have a unique password, stored in the company password manager. If you're not on it yet, request access via the helpdesk.
- Never type a work password into a personal device unless the password manager or the sign-in page directs you to.
- Shared mailboxes and service accounts: credentials live in the password manager, not in chat or in a doc. If you see one in the open, move it and ping #security.

## MFA

- MFA is required on every system that supports it. That includes ledgerctl, sharectl, the CRM, the analytics warehouse, the POS back office, the feature flag service, and the admin side of mailer.
- Use the authenticator app, not SMS, wherever the option exists. SMS is only for systems that don't offer anything else.
- If you get a push or a code you didn't trigger, do not approve it. Report it via the incident process in `eng-docs/oncall/incident-process.md` and mention it in #security so the team can check for a token replay.
- Lost or replaced phone? Sort new MFA before wiping the old device. If you're locked out, the helpdesk can do a recovery only after you've spoken to a member of Security engineering.

## Stores and shared accounts

- Store tills and the POS back office do not use personal logins. Each store has a shared account per shift; the PIN is rotated at the start of every quarter and whenever someone with access leaves.
- Wholesale account managers share the same rule for the wholesale order portal — one shared login per team, credentials in the password manager, rotated each quarter.
- Never put a shared store or wholesale password in a ticket, in chat, or on a sticky note near the till. If you see one, change it and tell the store manager or the relevant team lead.

## Other

- Password expiry is managed centrally — you'll see a reminder from the password manager, not from an email. Treat any email asking you to "verify" or "renew" your password as phishing and report it.
- New joiners get their initial password from the onboarding checklist in the handbook; it must be changed at first sign-in.
