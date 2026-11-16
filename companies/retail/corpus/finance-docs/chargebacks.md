# Chargebacks

**Owner:** Disputes & chargebacks  
**Last edited by:** Isaac Gashi  

---

## How chargebacks arrive

Chargebacks come from the acquirer as a daily file. The Payments platform team (billing-api) imports it automatically into the dispute tracker and books each one to the chargebacks ledger, but the feed can lag by a day or two. If you need to check whether a specific chargeback has landed, Isaac or anyone in Disputes can query the acquirer portal directly.

1. New ones sit at the top of the dispute tracker's open queue.
2. Each entry shows the order number, amount, reason code, and the acquirer's deadline for representment.
3. The deadline is **not** negotiable. The acquirer applies their own clock; if our response misses it, the customer keeps the money and the case is closed.

## Who owns what

- **Disputes & chargebacks** owns the whole lifecycle: evidence gathering, representment, and any follow-up with the customer.
- **Checkout / billing-api** only owns the technical import and any feed fixes. If a chargeback is missing from the dispute tracker, raise a ticket in `tickets` on the payments platform project, not in the disputes project.
- **Credit control** gets involved only when a wholesale invoice is disputed through the bank rather than through our normal credit terms process. That is rare; when it happens the disputes team adds credit control to the case so the account manager hears about it.

## Evidence packs

For retail orders (online or in store), the standard pack is:

1. Order confirmation from the CRM (copy the order ID from the chargeback entry).
2. Delivery confirmation. For online orders, use the tracking event from the carrier. For store orders, use the POS receipt showing the item was collected or delivered — export from the POS back office and save as PDF.
3. Any communication with the customer from `mailer` or `chat` (only if relevant to the reason code). For example, for a "goods not received" dispute, include the dispatch email. For a "not as described" dispute, include any photos the customer sent via support.
4. A short summary note (one or two sentences) explaining why the charge is valid. Write it like you would to a bank, not to a customer.

Save everything into the chargeback folder in the shared drive. Name it `CB-<order number>-<acquirer reference>.pdf`. One PDF per chargeback, merged in that order.

**Stores:** if the store needs to help with a receipt or a signature, ask the store manager directly via `#stores-ops`. Do not ask the helpdesk — they do not have access to the POS back office.

**Wholesale:** chargebacks on wholesale payments are handled by the same process, but the evidence pack is different. Include the purchase order, the delivery note, and the invoice from the ledger. If the customer has already paid a partial amount, note that in the summary — the acquirer sometimes only disputes the outstanding balance.

## Representment

Representment is submitted through the acquirer portal by Disputes & chargebacks. Aurelio and Freya alternate on submissions; Malik picks up anything that arrives outside the usual working pattern. If all three are out, Isaac handles it.

1. Log in to the acquirer portal (credentials in the shared password manager under "Acquirer disputes").
2. Find the chargeback by reference.
3. Attach the merged evidence PDF.
4. Pick the response code that matches the reason code; the acquirer portal lists them per card scheme. Isaac has seen most of the older codes if one is unfamiliar.
5. Submit and note the confirmation reference on the case in the dispute tracker.

## If it goes wrong

- **Missed deadline:** mark the case as `lost` in the dispute tracker and post a note in `#disputes`. The amount is written off. Do not call the acquirer to ask for an extension — they do not give them. If it keeps happening on the same reason code, raise it in the next fortnightly review with the payments platform team.
- **Acquirer rejects the representment:** the rejection notice comes through the same feed. Check whether the rejection is because of evidence (missing or unreadable) or because the reason code does not match. For evidence issues, we can resubmit once. For reason code mismatches, we cannot — log it as `lost` and move on.
- **Customer disputes the same order twice:** the second chargeback usually arrives under a different reason code. Treat it as a new chargeback; do not assume the first representment covers it.
- **A store or wholesale customer calls about a chargeback before we see it:** ask them for the acquirer reference and check the dispute tracker. If it is not there, tell them the bank feed can take a couple of days and ask them to follow up with their bank. Do not promise anything about the outcome.

## Review cadence

Aurelio runs a weekly report of all open chargebacks and posts it to `#disputes` on the first working day of the week. Isaac reviews the lost ones each fortnight and makes sure the write-offs are reflected in the ledger before the month-end close. If you notice a reason code we have not seen before, flag it in `#disputes` — we track new patterns in the shared spreadsheet.
