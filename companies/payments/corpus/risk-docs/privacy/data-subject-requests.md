# Data subject requests

**Owner:** Privacy & data governance  
**Last edited by:** Yusuf Demir (Senior Counsel, Privacy)

This covers requests from merchants' staff and e-money customers exercising their rights under the GDPR — primarily access, erasure and correction. It does not cover requests from merchants acting as data controllers (e.g. a merchant asking for a copy of their own transaction data); route those through the back office and the merchant support handbook.

## Before you start

1. Confirm who is asking. For an e-money customer, verify identity via the KYB onboarding tool or the merchant dashboard, whichever holds the relationship. For merchant staff, ask them to confirm through their work email or via the helpdesk.
2. If the requester is acting on behalf of someone else (e.g. a solicitor), get a signed authority from the data subject before proceeding. Pass this to Privacy & data governance with the request.
3. Log the request in the case tool under the `DSR` category. Include the date received, the channel, and what was asked for. This timestamp starts the one-month clock.

## Access requests

4. Search the systems that hold personal data for the requester's identity. The usual places are:
   - the core ledger (search by customer ID or IBAN)
   - the treasury workstation (payout records)
   - the transaction monitoring system (screening hits, alerts)
   - the back office (merchant account records, staff user accounts)
   - custnotify (any notices we sent them)
   - the CRM (support tickets, account notes)
5. Pull the relevant records into a single folder on the case in the case tool, named with the case reference. Do not include records that relate to other people; redact those before sharing.
6. Send the response through the same channel the request came in, unless the requester asked for a different channel. The merchant dashboard supports a secure message attachment; the back office does not, so use the case tool's secure link for those.
7. If we need more time (e.g. the request is complex), tell the requester within the first month and log the extension in the case tool. A further month is the maximum.

## Erasure requests

8. Find the records as for an access request, but do not delete anything yet. Check whether we are obliged to keep any of them:
   - AML records (screening hits, KYC documents, transaction monitoring alerts) are kept per the records retention schedule — do not delete those.
   - Ledger entries are part of the event-sourced ledger; erasure means anonymising the personal identifiers on the events, not removing the events themselves. See ADR 0004 in eng-docs for the mechanics.
   - Settlement and payout records fall under safeguarding; coordinate with Treasury ops before touching anything.
9. For records that can be erased, delete them in the source system and note the deletion in the case tool. For the core ledger, raise a ticket to `#payments-platform` with the customer ID — the ledger team will run the anonymisation.
10. Confirm to the requester what was erased and what was kept and why (e.g. statutory retention). Keep the wording brief; the privacy team can review if it is a sensitive case.

## Correction requests

11. Verify the correction against the source of truth. For merchant staff details, that is the back office; for e-money customer details, the merchant dashboard or the KYB onboarding tool.
12. Make the change in the source system. Corrections do not propagate automatically, so check whether other systems hold the same field (e.g. an address held in both the CRM and the core ledger) and update each.
13. Where a correction affects a record we are required to keep (e.g. a name on a transaction monitoring alert), add a correction note to the record rather than overwriting it.

## If it goes wrong

- **Missed the deadline:** tell the Privacy & data governance lead immediately. Do not send the response late without checking with them first; they may prefer a partial response and an explanation.
- **Can't find the person:** search the analytics warehouse for the customer ID, and ask the merchant success team whether the account has been renamed or transferred. If still nothing, tell the requester we have no records and log the search steps in the case tool.
- **Request is abusive or manifestly unfounded:** do not refuse on your own. Refer to Katrin Solberg's team with the evidence; they will decide whether to refuse and how to word it.

Templates for acknowledgement, extension and response letters are pinned in #data-governance. Use those rather than drafting from scratch.
