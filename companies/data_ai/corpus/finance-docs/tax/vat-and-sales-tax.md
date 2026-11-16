# VAT and US sales tax notes

Needs updating after the move — ping #finance if something here looks wrong.

**Owner:** Accounting, AP and payroll · Last edited by Ebony Schmidt

## EU / UK VAT

- Subscriptions to EU customers are B2B reverse charge when the customer provides a valid EU VAT number. We keep the number on file in the CRM and note it on the invoice.
- If no valid VAT number, we charge Dutch VAT at the standard rate on the subscription. This came up with a couple of agricultural co-ops in France during the last renewal push.
- Imagery tasking orders follow the same rule; the analytics API is treated as a subscription for VAT purposes.
- UK customers: reverse charge still applies post-Brexit, but we need the customer's UK VAT number and should mark the invoice "reverse charge" per {{TAX_AUTHORITY_1|code}} wording. Some UK port accounts were set up before the change and may still have Dutch VAT on file — the support team knows to route those via #support to Accounting.

## Dutch domestic customers

- Domestic (NL) customers are charged Dutch VAT at the standard rate. This includes water boards unless they are acting under a public law arrangement — the public-sector tenders doc has the criteria, but in practice we default to charging VAT and adjust on request.

## US sales tax

- US SaaS sales tax varies by state. We currently collect where we have nexus: Colorado (Denver office) and any state where we exceed economic nexus thresholds. The customer API console shows whether tax is added at checkout.
- States handled by the tax engine in the billing system; no manual calculation. If a US customer says they are tax-exempt (many port authorities are), the exemption certificate goes to Accounting via the CRM and we flag the account before the next invoice run.

## Public sector

- Some public-sector customers (water boards, municipalities) send us a self-billing or reverse charge arrangement. Those are handled case by case and the arrangement is noted in the CRM. Ask before assuming.

## Where to ask

- VAT questions: #finance or the Accounting team. US sales tax: Jin knows the state rules. General invoicing queries: #support routes via the helpdesk and the customer API console notes.

**Loose ends:** the payroll calendar references a VAT return date that moved; the CRM field for the reverse charge marker is not always filled in, so invoices can go out with Dutch VAT by mistake. Chasing the sales team to update it before each invoicing run.
