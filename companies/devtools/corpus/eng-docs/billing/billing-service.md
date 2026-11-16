# billing-service

**Owner:** Billing engineering  
**Last edited by:** Malik Iyer  

## What it does

`billing-service` is the core of how Gantline charges customers. It:

- Pulls seat counts from the platform (via the seat snapshot feed) on a fixed cadence, once an hour on working days.
- Computes invoice line items from those seat counts plus any add-ons (extra storage, hosted runner minutes over the plan allowance).
- Generates invoices through the payment provider. Invoices are produced on the first working day of the month and again mid-month for mid-cycle changes (seat increases, plan upgrades).
- Calculates tax per invoice based on the customer's billing country and, where applicable, state or province. EU VAT is handled by the payment provider's tax engine; US sales tax uses the tax rate tables we maintain in the `tax-rates` config.
- Produces reconciliation exports for finance. These land in the finance bucket each morning and are picked up by the month-end process (see `bizops-docs/finance/month-end.md`).

## Dependencies

- **Platform seat API** — the source of truth for seat counts. If the seat feed is delayed, billing-service will use the last successful snapshot and note the staleness on the invoice.
- **Payment provider** — all charge capture and refunds go through the provider's API. The provider webhooks update invoice status; we do not poll.
- **Tax rate service** — internal service that serves the rate tables. It is updated by Billing engineering when rate changes are published.
- **Credit batches** — billing operations issues account credits from the credit queue; issued credits arrive in batches and billing-service applies them to the customer's next invoice. (See `bizops-docs/billing/credits.md` for the credit process.)
- **Data warehouse** — the reconciliation exports are loaded into the warehouse on a nightly schedule. Finance runs their checks against the warehouse, not against billing-service directly.

## Known issues

- **Seat counts for suspended orgs** — when an org is suspended for non-payment, the seat feed keeps reporting their seats until the org is fully closed. This means a suspended org can appear to accrue charges. The dunning flow (see `bizops-docs/billing/dunning.md`) handles this, but the invoice line item for suspended orgs can be misleading if someone looks at the raw data.
- **Currency rounding for multi-line invoices** — there is a known rounding difference when an invoice has both seat charges and usage-based add-ons in a non-USD currency. The total is correct, but the per-line amounts may not sum exactly to the total. This has been logged with the payment provider; we are tracking it on our side.
- **Tax re-calculation on credit notes** — when a credit note is issued for a partial refund, the tax is re-calculated at the current rate, not the rate on the original invoice. This matters if a rate changed between invoicing and the refund. Finance is aware; the reconciliation export includes both tax amounts so they can reconcile.
- **Webhook retries** — the payment provider retries webhooks for up to three days. If billing-service is down for longer than that, we need to manually trigger a reconciliation pull. There is no written runbook for that yet — ask in #billing-ops.

## Loose ends

- We still have a hardcoded list of beta customers who get invoiced manually. This list lives in the `manual-invoice` config and should be moved to the platform's feature flag service. It has not been migrated yet.
- The tax rate tables are updated by hand. There is an open RFC to move this to an automated feed; it has not been picked up.
- The reconciliation export filename includes the old `billing-svc` prefix. Finance's ingestion handles it, but we should rename it to `billing-service` for consistency with the repo name.
