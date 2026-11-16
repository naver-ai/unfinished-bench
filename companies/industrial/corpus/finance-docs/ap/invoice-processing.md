# Invoice processing

**Owner:** Accounts payable  
**Last edited by:** Daan Peeters

---

## Scope

This covers supplier invoices received by Accounts payable for goods and services purchased against a PO. It does not cover employee expenses, intercompany recharges, or credit notes raised by us.

---

## 1. Scanning and capture

1. All supplier invoices arrive either by email to `ap@kessendorf.com` or as paper mail to the Reutlingen reception. Paper mail is routed to Accounts payable on the second floor.
2. Scan paper invoices at the multifunction printer in the finance corridor using the profile **AP-Capture**. The scan lands in the capture inbox in {{DOC_CAPTURE}} (the old ScanFlow profile is retired — do not use it).
3. In {{DOC_CAPTURE}}, open the **AP Inbox** queue. Each document must be assigned a document type: `Invoice`, `Credit note`, or `Statement`.
4. The OCR fields are usually populated. Check the supplier name, invoice number, invoice date, and total amount. Correct anything the OCR got wrong before saving.

## 2. Matching

5. Match the invoice to the PO in the ERP. Use transaction **{{ERP_INVOICE_TRANSACTION|code}}** (invoice receipt) for goods invoices or **MR8M** for credit notes.
6. For a goods invoice, the PO must be fully goods-receipted before posting. Check the GR quantity in **MIGO** — if the GR is missing or short, hold the invoice and contact the buyer named on the PO.
7. For a service invoice, check that the service entry sheet has been approved in the ERP. Service entry sheets are approved by the requester's manager; if approval is missing, return the invoice to the requester via the supplier portal.
8. Three-way match: PO line, GR line, and invoice line must agree on item number, quantity, and price. If the invoice line does not map to a PO line, do not post — send it back through the supplier portal with a note.

## 3. Tolerances

9. Price tolerance: the invoice line may not exceed the PO price by more than 3%. Above that, the invoice goes to the buyer for a price change or a credit note request.
10. Quantity tolerance: invoiced quantity may not exceed the GR quantity by more than 2% or one unit, whichever is larger. Anything above that is held pending a GR correction.
11. Small differences in the total (up to EUR 2.00) can be posted to the tolerance account **DIF01** without contacting the supplier.

## 4. Posting and payment

12. Post the invoice in the ERP. The GL account is taken from the PO; do not override it unless the buyer confirms the change in the supplier portal.
13. Invoices are paid on the next payment run after the due date printed on the invoice. Payment runs happen twice a month; see the payment runs page in the finance docs.
14. After posting, file the PDF in {{DOC_CAPTURE}} under the supplier's folder and set the workflow status to `Posted`.

## 5. Credit notes

15. Credit notes are matched against the original invoice. If the credit note references a specific invoice, match it in **MR8M**.
16. If a credit note has no reference, post it as a standalone credit and raise a query to the supplier through the supplier portal asking for the reference.
17. Credit notes that exceed the original invoice amount are held and escalated to Daan before posting.

## 6. Supplier statements

18. At month-end, compare the supplier statement against the ERP account balance in **FBL1N**. Do this for the top 40 suppliers by volume; the list is in the AP shared folder.
19. Differences go to the supplier via the supplier portal with a copy of the statement and the open items from the ERP. Chase for a reply after two working days.
20. If a supplier statement shows an invoice we do not have, request a copy of the invoice from the supplier and process it as a new invoice.

## 7. Supplier queries

21. All supplier queries go through the supplier portal. Log in with the shared AP account, assign the query to the right clerk (Rebecca for German suppliers, Gaurav for UK and US suppliers, Julia for the rest).
22. If a supplier calls by phone, direct them to the portal. We do not discuss invoice status over the phone.

---

## If it goes wrong

- Invoice posted to the wrong cost centre: reverse with **MR8M** and re-post with the correct assignment. Tell the buyer so they can correct their records.
- Duplicate invoice: do not delete. Post a credit note for the duplicate amount and note both document numbers in {{DOC_CAPTURE}}.
- OCR capture failed and the document is in the wrong queue: move it to the correct queue in {{DOC_CAPTURE}} and re-run the OCR profile.
- Supplier portal is down: process the query by email to the supplier and note the ticket number in the AP log. Do not create a manual invoice outside the ERP.

---

## Related

- `finance-docs/ap/supplier-master-data.md`
- `finance-docs/procurement/po-release.md`
- `finance-docs/treasury/payment-runs.md`
