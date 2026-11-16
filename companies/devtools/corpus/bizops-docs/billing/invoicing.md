# Invoicing

**Owner:** Billing operations  
**Last edited by:** Nadia Achebe (Billing Analyst)

## Overview

Invoicing covers monthly and annual cycles for Gantline Cloud plans, seat true-ups, VAT and sales tax handling, and invoice delivery. Billing operations owns the process end to end; the billing service in the admin console is the source of truth for what a customer is charged.

Cards are the default for all plans. Accounts on monthly billing above 100 seats, and any account on an annual plan above 1,000 seats, are invoiced instead of card-charged. The admin console marks these accounts as `invoice-billing` and hides the card fields.

## Monthly and annual cycles

1. Open the admin console and go to **Billing → Customers**.
2. Find the customer org. The plan line shows the cycle (`monthly` or `annual`), the renewal date, and the billing method (`card` or `invoice`).
3. Monthly invoice accounts are billed on the first working day of the month for the previous month's usage. Annual accounts are billed on their renewal date for the next 12 months.
4. Seat true-ups run automatically on the same cycle. The true-up line appears on the invoice as `Seat adjustments for the period`. Seats added mid-cycle are prorated to the cycle end.
5. If the customer's seat count crosses the invoice threshold mid-cycle, the next invoice switches them to invoice billing. Their card is left on file but not charged.

## Creating and sending invoices

1. In the admin console, go to **Billing → Invoices**.
2. Click **Generate** next to the open invoice period. The billing service pulls usage and seat data and produces the invoice PDF.
3. Review the PDF for the customer name, VAT ID (EU customers), and the line items. If anything looks off, raise a ticket to the billing service team rather than editing the PDF.
4. Click **Send**. The invoice goes to the billing contact(s) on the account. The email platform sends it from `billing@gantline.dev`.
5. File a copy in the customer folder in the CRM. The data warehouse picks the invoice up from there for reporting.

## Changing billing contacts

Invoice copies go to the billing contacts listed in the admin console under **Billing → Contacts**. Customers can change these themselves through the admin console. For enterprise accounts, Colette Ramirez (Sales) or the customer success team usually coordinates the change; Billing operations updates the contact list when the customer asks through a support ticket.

If a customer requests an invoice be resent, check the billing contact first — most "I didn't get it" cases are an old contact address. Update the contact, then use **Resend** on the invoice in the admin console.

## VAT and sales tax

- **EU customers:** invoices include VAT at the rate for the customer's country. The billing service looks up the rate from the VAT number the customer provided. If the customer hasn't provided a VAT number, the rate defaults to the rate for their registered address.
- **US customers:** sales tax is applied for states where Gantline Inc. has nexus. The admin console shows the tax line separately on the invoice. Billing operations does not adjust tax rates manually; changes go through Finance.

## If it goes wrong

- **Wrong amount on an invoice:** do not edit or reissue the PDF. Mark the invoice as `disputed` in the admin console and have the billing service team regenerate it after the underlying data is fixed.
- **Duplicate invoice sent:** send a note to the billing contact and mark the duplicate as `void` in the admin console. The voided invoice stays visible to the customer but shows as cancelled.
- **Missing VAT ID:** the invoice still goes out with the default rate. Flag the account to Finance so they can chase the VAT ID before the next cycle.
- **Invoice generated for the wrong customer org:** contact the billing service team and ask them to check the org mapping. Do not forward the PDF to the correct customer — the numbers likely won't match their account.

For anything else, open a ticket in the helpdesk with the `billing` tag and include the customer org ID and invoice number.
