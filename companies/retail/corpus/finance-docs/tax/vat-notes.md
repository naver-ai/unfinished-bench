# VAT notes for ops

Owner: FP&A. Last edited by Zeynep Amsel.

Context: we had recurring questions from the support team and the stores about VAT treatment on online orders, gift cards, and wholesale. Bruno Ibarra pulled together a short session with FP&A and the payments platform team to write down what we operate with day to day. These notes are for the ops side, not the filing position — if in doubt, raise it in #finance-ops.

## Online orders — UK vs Ireland

- UK delivery address: VAT at UK rate. Ireland delivery address: VAT at Irish rate. The rate is set at checkout based on the delivery address, not the billing address or the card.
- US orders: no VAT, but the checkout still shows a tax line for US sales tax where the fulfilment state requires it. That is handled by the tax engine in the checkout service, not by us manually.
- If the customer later changes the delivery address before dispatch, the order is re-priced and VAT is recalculated. The warehouse system picks this up automatically. Refunds of the difference go through the standard refund process (see finance-docs/refunds.md).

## Gift cards

- Sale of a gift card: no VAT at the point of sale. VAT is accounted for when the card is redeemed against goods.
- This applies to gift cards sold in store and online. The POS back office and the web checkout both treat gift card sales as a receipt, not a sale of goods. Do not override this in the ledger when coding the daily takings.
- Redeemed gift cards against an order: the order is VATable in the normal way. The gift card redemption is not a discount for VAT purposes; VAT is on the full value of the goods supplied.
- Expired or partially redeemed cards: no VAT adjustment either way.

## Wholesale

- Reverse charge questions for wholesale customers (mainly garden centres and independent shops) are not something we handle in FP&A day-to-day. Anything on reverse charge — whether it applies for a given customer, the wording on the invoice, or the customer querying the VAT on their statement — goes to the tax team. Delphine can point the customer to the right contact, but the credit control team does not give VAT advice on the phone.
- The wholesale arm invoices via the ERP; the VAT treatment is set per customer by the tax team. If a customer is set up without a reverse charge flag and you believe it should be there, raise it via tickets to Finance ops, not directly to the tax team.

## Loose ends

- The Irish online rate is currently set from a config file in the checkout service. We asked payments platform to move that into the feature flag service so FP&A can update it without a code deploy. Not done yet.
- Gift card VAT on partially redeemed cards issued before the February change — there is a small population where the unredeemed balance was cancelled. The tax team said it is fine as filed, but we have not done a formal review. On the list for the next quarter-end.
- The old "vat-calc" spreadsheet that support used to check rates is out of date; point anyone who asks to the checkout config instead.
