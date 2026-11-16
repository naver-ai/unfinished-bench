# Intercompany

**Owner:** Group controlling  
**Last edited by:** Daisuke Castillo (Senior Controller)

## Scope

This note covers what the three Kessendorf entities invoice each other for, the transfer pricing mark-ups, and how we match and settle intercompany balances each month.

## What we invoice

- **Telford (Kessendorf UK Ltd)** invoices Reutlingen and Greenville for DU-series drives and drive sub-assemblies built on the Telford drives line. Standard mark-up: cost plus 6%.
- **Reutlingen (Kessendorf GmbH)** invoices Telford and Greenville for finished MC-series motion controllers and for engineering services (application engineering, firmware support, retrofit design). Mark-up on controllers: cost plus 8%. Engineering services: cost plus 5%, applied to direct labour and material only.
- **Greenville (Kessendorf Inc.)** invoices Reutlingen and Telford for field service work performed in the Americas, and for warranty service on behalf of the group. Mark-up: cost plus 5%.

Mark-ups were set by group tax and have not been revisited since. If a new product line or service type starts crossing entities, raise it with group controlling before quoting a price to the receiving entity.

## Monthly matching

Intercompany positions are matched in the consolidation tool at month-end close. The AP side in the receiving entity must match the AR side in the invoicing entity within a tolerance of EUR 500 (or local equivalent, converted at the month-end rate used by treasury).

Matching is run by group controlling on the second working day after close. Open items are chased with the entity controllers; anything still open after the third working day gets escalated to the CFO.

## Settlement

Net positions are settled monthly via the payment runs in the treasury module. Only the net balance per entity pair is settled. Settlement currency is EUR; Telford and Greenville positions are converted using the rate published in the cash forecasting note for that month.

Treasury is copied on the settlement run. Sanne Visser handles the intercompany settlement entries in the ERP.

## Mismatches

Common causes and how they are resolved:

- **Timing differences** — goods in transit, service not yet booked. Recheck against the goods-in record and the RMA portal. If the goods arrived in the receiving entity's warehouse before the invoice was posted, the receiving entity books the invoice in the same period.
- **Price differences** — check against the CPQ tool if the item was quoted, otherwise against the item master. If the price on the invoice differs from the agreed mark-up, the invoicing entity issues a credit note; the receiving entity does not adjust the invoice.
- **Quantity differences** — check against the MES production record and the outbound release at the dock. Shortages are handled via the normal RMA process; the intercompany invoice is matched only after the RMA is logged.
- **Currency rounding** — differences under EUR 50 are written off by group controlling. Above that, the invoicing entity re-issues.

If an entity pair has more than two mismatches in a quarter, group controlling sets up a call with the affected controllers to look at the root cause.

## Loose ends

- Telford has been invoicing Reutlingen for packaging materials under the engineering services line. This should be a goods line, not a service line. The UK controller was going to fix the item master — not done yet.
- The old intercompany reconciliation spreadsheet (the one Shreya used to run before we moved to the consolidation tool) is still referenced in the month-end close checklist. The checklist should point to the consolidation tool instead.
- Margreet asked for a quarterly summary of intercompany balances by entity and currency. Group controlling provides this in the finance review deck, but the format is still the one from the pre-consolidation-tool days; a cleaner layout is pending.

Questions on this note go to group controlling.
