# Merchant invoices and fees

**Owner:** Merchant billing  
**Last edited by:** Camille Ozturk (Billing Specialist)

**How processing fees, plan fees, invoices, and credit notes work — questions we get from merchant success and support.**

---

### How are processing fees charged?

Processing fees are netted from settlement. When we settle a merchant's transactions, we deduct the agreed processing fees before the payout is sent to their settlement bank account. Merchants see the fee breakdown per payout in the merchant dashboard under **Payouts → Fee details**.

### How are platform plan fees charged?

Platform plan fees (monthly, annual, or per the contract term) are charged to the card or bank account the merchant has on file. The charge runs through chargectl on the first working day of the month. If the card or account fails, we retry twice more at three-working-day intervals before the plan is flagged for review. Merchant success can check the charge status in the back office under **Billing → Plan charges**. Mid-cycle plan changes (seat top-ups, upgrades, add-ons) are billed separately as they happen — see `merchant-docs/billing/plan-change-billing.md`.

### Where do merchants find their invoices?

In the merchant dashboard under **Billing → Invoices**. Invoices are generated monthly for plan fees and any other non-processing charges. Processing fee invoices are not generated separately — the fee detail per payout serves as the record, and merchants can export a summary for any date range.

### When are invoices issued?

Plan fee invoices are issued on the same day the charge runs. If a merchant needs an invoice outside that cycle (for example, for a one-off setup fee), billing creates it manually and posts it to the dashboard.

### What about credit notes?

Credit notes are issued when we owe the merchant money — for example, a fee correction, a waived charge, or an overpayment. They appear in the same **Billing → Invoices** section with a **CN-** prefix. Credit notes are applied to the next invoice automatically unless the merchant asks for a direct refund instead.

### A merchant says their invoice looks wrong. What do we do?

Start by checking the charge in the back office — the invoice should match the charge exactly. If the amounts differ, or the merchant disputes the fee, raise a ticket to the billing queue with the merchant ID, invoice number, and what the merchant says is wrong. Billing responds within two working days. Do not promise a credit note or refund before billing has reviewed it.

### Can a merchant change their billing card or bank account?

Yes — in the dashboard under **Billing → Payment method**. Changes take effect for the next charge. If a charge fails because of an outdated card, the merchant can update the card and we retry on the next scheduled retry date.

### Do merchants get invoices for processing fees?

No. Processing fees are netted from settlement and shown per payout. If a merchant needs a consolidated statement of processing fees for accounting, they can export one from the dashboard. The export includes the fee rate, the gross and net amounts, and the payout reference.

### Can merchants pay invoices by bank transfer instead of card?

For plan fees, the default is the card or bank account on file. If a merchant needs to pay by transfer, that is handled case by case by billing — the merchant should contact merchant success, who will open a ticket. We do not advertise this as an option.

### A merchant asks for a fee breakdown by transaction. Who can help?

The dashboard shows per-payout fee summaries but not per-transaction fees. If a merchant needs transaction-level fee detail, merchant success can request it from billing. We only provide this for the current and previous month unless there is a dispute or audit need.

### How do we handle fee questions during onboarding?

The merchant's fee schedule is part of their contract and is visible in the dashboard under **Billing → Fee schedule**. If a merchant asks whether a fee can be negotiated, that is not something billing can change — refer the question to the merchant's account owner in merchant success.

### What happens to invoices when a merchant closes their account?

When an account is closed, any outstanding plan fees are charged and invoiced as part of the final reconciliation. Credit notes for any overpayment are issued within ten working days of closure. The merchant keeps dashboard access for 90 days to download documents.
