# Wholesale credit terms

**Owner:** Credit control (wholesale)  
**Last edited by:** Delphine Marchetti (Credit Controller)

## Purpose

This document sets out how credit limits and payment terms are assigned to wholesale accounts, and how holds are applied and released. It applies to all wholesale customers supplied by Mossgrove, including independent outdoor shops, garden centres, and any account opened through the wholesale arm.

## Scope

Credit control (wholesale) manages all credit applications, limit reviews, and holds. The POS back office and the wholesale sales team do not set or change terms.

## Credit application

1. A new wholesale account must complete a credit application before the first order is processed. The application is submitted through the CRM and lands in the credit control queue in the tickets system.
2. The application must include: two trade references, the customer's company registration number, and the registered address. Applications missing any of these are returned to the sales contact for the account.
3. Credit control (wholesale) checks trade references and runs a credit check through the usual bureau. The check is valid for 30 days from the date it is run; if the account has not placed an order within that window, the application is reopened and the check is rerun.
4. Applications for accounts with a registered address outside the UK or Ireland are reviewed by Graham Pike before a limit is set.

## Credit limits by account tier

5. Accounts are assigned to one of three tiers:

   5.1. **Tier 1** – new accounts or accounts with less than 12 months trading history. Standard limit is £2,500.

   5.2. **Tier 2** – accounts with 12+ months of trading history and no more than two late payments in the last 12 months. Standard limit is £10,000.

   5.3. **Tier 3** – accounts with 24+ months of trading history, no late payments in the last 12 months, and a consistent order pattern. Standard limit is £25,000, or higher at the discretion of the Credit Control Manager.

6. Limits are reviewed every six months. Reviews are driven from the CRM and are queued to credit control automatically. Nadia Farouk runs the Tier 1 and Tier 2 reviews; Magnus Nunez runs Tier 3 reviews.
7. A customer can request a temporary limit increase for a single order. The request must come through the wholesale sales contact and is approved only if the account is not on hold and has no outstanding invoices beyond the payment terms. Temporary increases are capped at 50% above the account's standard limit and last for 60 days.

## Payment terms

8. Standard terms are **net 30** from the date of the invoice.
9. Net 60 terms may be granted to accounts that have held a Tier 3 limit for at least 12 months and have paid on time for the last 6 months. Net 60 requests are approved by the Credit Control Manager only.
10. Terms are set on the account in the CRM and flow to the ledger when the invoice is raised. Any change to terms must be made in the CRM before the invoice run; changes made directly in the ledger will be overwritten at the next sync.

## Credit holds

11. A hold is placed on an account when:

    11.1. An invoice is more than 14 days past its due date.

    11.2. The account exceeds its credit limit, even if the invoices are not yet due.

    11.3. The account has had a cheque or card payment returned unpaid twice within a rolling 3-month period.

12. Holds are applied by credit control through the CRM and take effect on the next order the customer places. The wholesale sales team is notified through the CRM so they can contact the customer before the order is blocked.
13. While an account is on hold, no new orders are processed and no further credit is offered. Existing open orders that have already been picked are still shipped unless the hold is marked as urgent by credit control.
14. A hold is released when the account has either paid the outstanding balance in full or agreed a repayment plan that is logged in the CRM. Repayment plans must be approved by Graham Pike or Nadia Farouk.

## Overrides

15. Only the Credit Control Manager can override a hold. Overrides are recorded in the CRM with a reason and a review date.
16. The Chief Financial Officer can override a hold on a Tier 3 account, but this is rare and the override is logged the same way.
17. No other role, including the wholesale sales team or regional operations, can release or override a hold. If an account is on hold and an order is urgent, the request goes through credit control in the tickets system.

## Related documents

- `finance-docs/ar-reminders.md` – overdue invoice reminders and escalation
- `finance-docs/ap/payment-runs.md` – how payments are applied to accounts
- `data-docs/sharing.md` – what customer data can be shared outside Mossgrove
