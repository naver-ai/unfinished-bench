# Failed payments

Owner: Billing operations · Last edited by Nadia Achebe

When a customer's card payment fails, the billing service runs a retry sequence and sends emails at defined points. This page covers the retry cadence, the emails, and what happens when an org is put into read-only mode.

## Card retries

The billing service retries the card three times after the initial failure. The retries happen on a fixed schedule relative to the original attempt. If the card is updated before the final retry, the remaining attempts are skipped and the payment is retried immediately with the new card details.

| Attempt | Timing | Notes |
|---|---|---|
| Initial | On the invoice due date | Card declined or network error |
| Retry 1 | Two days after initial failure | |
| Retry 2 | Five days after initial failure | |
| Retry 3 | Eight days after initial failure | Final automatic attempt |

After the third retry fails, the payment is marked as failed and the org is moved to read-only. No further automatic attempts are made. The customer must update their card or contact support to have the payment reprocessed manually.

## Emails

The billing service sends the following emails through the email platform. All emails come from billing@gantline.dev and are sent to the org's billing contact (the last user who updated the payment method, or the org owner if no payment method has ever been set).

| Email | Trigger | Content |
|---|---|---|
| Payment failed | Initial failure | Invoice number, amount, link to update card |
| Payment retry scheduled | Before retry 1 | Reminder that the card will be retried, link to update card |
| Payment retry failed | After retry 2 fails | Notice that the second retry failed, one retry remains |
| Read-only notice | After retry 3 fails | Org is read-only, steps to restore access |
| Payment received | Manual reprocess or new card succeeds | Confirmation, org is reinstated |

## Read-only mode

An org enters read-only mode after the final retry fails. In read-only mode:

- Existing workspaces keep running but cannot be started once stopped.
- Builds and CI runs are paused; queued jobs are held.
- The web editor and desktop editor open in read-only view.
- The API returns 402 for mutating endpoints but continues to serve read endpoints.
- Code search and code hosting remain fully available.

The org is reinstated as soon as a payment succeeds. Reinstatement is automatic — the billing service picks up the successful payment and removes the read-only flag within a few minutes. No manual step is needed from Billing operations unless the payment was made outside the normal flow (for example, a bank transfer or a credit applied by billing operations).

## Support guidance

When a customer asks about a failed payment:

- Confirm the invoice number and the amount from the billing service admin console.
- Check whether the org is currently read-only and when the retries ran.
- If the customer says they updated their card but the retry still failed, check whether the card was updated before the final retry. If it was updated after the final retry, no further automatic attempt is made — the payment needs to be reprocessed manually. Raise a request to Billing operations via the billing-ops channel with the org name and invoice number.
- If the customer asks why their org is read-only while the card looks valid, point them to the payment history in the admin console. The most common cause is a card that was replaced by the bank (new number) but not updated in the billing settings.

For anything beyond that, follow the escalation path in `bizops-docs/support/escalations.md`.

## Notes

- The retry schedule is configured in the billing service; do not adjust it per customer. If a customer asks for a different retry timing, offer the standard reprocess path instead.
- The read-only notice email includes a link to the billing settings page and the support contact. The reinstatement email is sent automatically when the payment succeeds.
- If a customer pays by invoice (not card), this page does not apply — see `bizops-docs/billing/invoicing.md`.
