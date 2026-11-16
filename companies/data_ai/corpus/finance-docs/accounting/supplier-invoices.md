# Supplier invoices

**Owner:** Accounting, AP and payroll  
**Last edited by:** Ebony Schmidt (Payroll Administrator)

## How invoices arrive

1. All supplier invoices go to the AP mailbox (`ap@brakwatergeo.com`). The mailbox is checked twice a day by Accounting, AP and payroll — first thing in the morning and mid-afternoon.
2. When an invoice arrives, save the PDF to the `Invoices/Received` folder in the shared drive and rename it using the pattern `YYYYMMDD_SupplierName_InvoiceNumber.pdf`. If the file is a scan or photo, still save it as PDF.
3. Register the invoice in the expenses tool with the following details:
   - Supplier name (match to the approved supplier list in the CRM)
   - Invoice number and date
   - Net amount, VAT amount and total
   - Currency (convert to EUR at the rate on the invoice date; note the rate used in the comments)
   - Purchase order number if one exists (see "Matching to the PO" below)
   - Cost centre code (see "Coding to cost centres" below)
4. If the invoice has no PO and no cost centre code, flag it as `Needs coding` and leave it in the `Invoices/Received` folder. The requestor is responsible for picking it up within five working days.

## Matching to the PO

5. For invoices against a purchase order, open the PO in the procurement module (the same one used for new suppliers — see `finance-docs/procurement/new-suppliers.md`).
6. Check the PO number on the invoice matches the PO line item. If the invoice total differs from the PO by more than 10%, do not proceed — send it back to the requestor with a note on the discrepancy.
7. If the invoice matches, mark the PO as `Invoice received` in the procurement module and attach the invoice PDF to the PO record.

## Imagery provider invoices

8. Imagery provider invoices often list per-scene lines with a scene ID, acquisition window, and price per scene. Match each line to the corresponding entry in the imagery catalogue.
9. If a line references a scene ID you cannot find in the imagery catalogue, check the tasking portal order number on the invoice. If the order exists, note the catalogue ID in the invoice comments. If the order does not exist, flag the line for review by the Imagery ops team via `#imagery-ops`.
10. Some imagery providers invoice in bundles (e.g. "50 scenes, medium resolution, region A"). For these, create one line per scene in the expenses tool using the catalogue IDs from the imagery catalogue, and allocate the invoice amount proportionally across the lines.

## Cloud provider invoices

11. Cloud provider invoices come as a single PDF with a summary and usage details. Save the PDF as usual and register the invoice in the expenses tool.
12. The cost centres for cloud invoices follow the cloud account naming in `platform-docs/cloud/accounts-and-projects.md`. For each cloud account that appears on the invoice, create a separate line in the expenses tool with the account's cost centre code.
13. If the cloud invoice total is more than 5% above the previous month's total, notify `#finops` before processing. Do not hold the payment — just flag it in the channel.
14. Cloud credits or adjustments appear as negative amounts on the invoice. Register those as a separate line with the same cost centre as the account they apply to, and add a comment noting the credit reference.

## Coding to cost centres

15. Use the cost centre codes from the chart of accounts (available in the finance drive under `Cost centres`). The main ones you will see are:
    - `CC-100` — Rotterdam office overhead
    - `CC-200` — Denver office overhead
    - `CC-310` — Imagery operations (satellite tasking, imagery ingest)
    - `CC-320` — Ground sensor network
    - `CC-410` — Data platform (warehouse, pipelines)
    - `CC-420` — ML platform (training cluster, model serving)
    - `CC-510` — Customer success and delivery
    - `CC-610` — Sales and marketing
16. If a cost centre code on the invoice does not exist in the chart of accounts, do not guess. Leave the coding field blank and flag the invoice to the requestor.
17. Costs that span multiple cost centres (e.g. a training run that uses both imagery and compute) should be split into separate lines with a note in each line's comments.

## Payment runs

18. Payments run twice a month, with the second run on the final working day of the month. Invoices must be fully registered, coded and matched by midday on the working day before a payment run to be included.
19. To prepare a payment run, open the expenses tool and select `Payment runs` → `Create new run`. The tool lists all invoices marked `Ready to pay`. Review the list, then export it to {{SPREADSHEET_APP}} and check the totals against the general ledger.
20. If everything balances, approve the run in the expenses tool and send the export to `#finance` with a short note listing the total amount and number of invoices. The bank file is generated from the expenses tool and uploaded to the bank portal by the Financial Controller or the Senior Accountant.
21. After the run, mark each invoice as `Paid` in the expenses tool and move the PDF from `Invoices/Received` to `Invoices/Paid` in the shared drive.

## If it goes wrong

22. **Duplicate invoice.** If the same invoice number appears twice, keep the first registration and mark the second as `Duplicate` with a comment pointing to the original.
23. **Wrong amount.** If a supplier sends a corrected invoice (e.g. credit note plus new invoice), register both, mark the original as `Superseded`, and add the credit note number in the comments.
24. **Invoice without a PO.** Send it back to the requestor via the expenses tool with a note. Do not create a PO retroactively unless the requestor confirms the goods or services were already delivered.
25. **Suppliers chasing payment.** Check the payment run schedule above and reply with the next run date. If the invoice was submitted after the cut-off for a run, explain it will go in the following run.
26. **Bank details changed.** If a supplier notifies us of new bank details, do not update the supplier record in the CRM. Forward the request to the Financial Controller — bank detail changes need a separate verification step.
27. **Unclear invoice lines.** Flag in `#finance` with the invoice number and a screenshot of the line. Someone from the relevant team will respond — do not wait more than two working days before escalating to the Financial Controller.
