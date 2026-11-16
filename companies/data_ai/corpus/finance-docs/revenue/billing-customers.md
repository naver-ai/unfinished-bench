# How customers are billed

**Owner:** FP&A and finance analytics  
**Last edited by:** Caleb Laurent

## How are monitoring subscriptions billed?

Monitoring subscriptions (flood, water, crop, soil) are billed annually in advance. The invoice is raised on the subscription start date and covers the following twelve months. Renewals are raised automatically from the CRM contract end date; if a renewal needs a different price or term, the account manager updates the CRM before the renewal run.

## When do we bill tasking orders?

Tasking orders are billed per km² on delivery. The tasking portal records the delivered area (after cloud screening and any reshoots) and that figure drives the invoice. We bill the delivered km², not the ordered km² — if we delivered less because of cloud cover, the customer pays for what they actually got. The imagery operations team confirms delivery in the portal before the invoice is generated.

## And API usage?

API usage is billed monthly in arrears from the usage meter. The meter is read at the end of the billing month, usage is priced according to the customer's plan (see `commercial-docs/sales/pricing-and-packaging.md`), and invoices go out with the next billing run. If a customer disputes a usage figure, we pull the meter detail from the customer API console and walk through it with them.

## What about credit notes?

Credit notes are issued for billing errors, for partial deliveries on tasking orders, and for service credits agreed through support. They need the FP&A team to check the original invoice before the credit is raised. Credit notes reference the original invoice number — we don't issue standalone credits without that link.

## How does the CRM talk to the ledger?

The hand-off is a nightly batch: the CRM pushes contracts and invoices to the ledger via the workflow scheduler. The sync is idempotent, so re-running it after a failure doesn't duplicate anything. If a contract is amended in the CRM after the sync, the next run picks up the change and posts a correction. The finance team reviews the sync log each morning — anything that failed to post lands in the exception report in the BI dashboards.

## What happens if a customer wants to upgrade mid-year?

Upgrades are handled as a pro-rata adjustment on the next renewal, not as a mid-term invoice. The exception is when the upgrade adds a new site or sensor cluster — those are billed from the go-live date as a separate line. We don't split an existing subscription invoice mid-term unless the customer specifically asks for it.

## Do we bill in advance for API usage?

No — API usage is always in arrears. The only prepaid element for API customers is the platform fee, if their plan has one, which is billed annually in advance like a monitoring subscription.

## Which currency do we invoice in?

Rotterdam contracts are invoiced in EUR, Denver contracts in USD. The billing run uses the exchange rate published by the bank on the invoice date. We don't do multi-currency invoices — if a customer wants to pay in a different currency, that goes through the accounts team before we raise anything.

## Where do billing questions go?

Start with `#finance` — the FP&A team picks up billing queries there. For contract or pricing questions, the sales team owns those conversations. For anything about the meter or usage data, the data engineering team can help trace the source.
