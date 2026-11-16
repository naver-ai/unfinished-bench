# orders-web

> Needs a tidy-up after the returns portal work — ping #platform if something here looks off.

## What it does

orders-web is the order service behind the storefront, served from the shop-web domain. When checkout in shop-web submits an order, orders-web places it (the payment call and the order write); it also runs the customer-facing order history and returns portal. It handles:

- Order placement for online checkout (called by shop-web — see `eng-docs/web/shop-web-runbook.md`)
- Order history for customer accounts (both online and store purchases where the customer gave an email at the till)
- Returns initiation and label generation for UK, IE and US orders
- Wholesale order status lookup for trade customers (read-only — they don't initiate returns here, that still goes through the wholesale account manager)
- Gift card balance checks for orders placed against a gift card (see `finance-docs/gift-cards.md` for the balance reconciliation rules)

## Dependencies

- Payments platform — the payment call when an order is placed (`#payments-platform` if it is slow or failing)
- `orders-api` (owned by the Web team) — the order history and returns pages read from here, and it is fed from the order event bus (`eng-docs/adr/0012-event-bus.md`)
- `mailer` — return labels and confirmation emails
- The finance ledger — refund amounts are checked against the ledger before a return is accepted

The orders-web VMs (`orders-web-01`, `orders-web-02`) are on the weekly snapshot schedule only, see `eng-docs/platform/snapshots.md`.

## Known issues

- Return labels for US orders sometimes show the UK return address if the customer's order was fulfilled from Wakefield DC. The label is still valid but it confuses customers. We're tracking this with the fulfilment team.
- The order history page for wholesale trade customers occasionally fails to show line items for orders placed more than 13 months ago. The data is there, it's a query pagination issue. Workaround is to export the order from the wholesale portal.
- Irish customers sometimes see VAT amounts in GBP on the order detail page instead of EUR. The amounts are converted correctly at checkout, this is purely a display issue. It's been on the backlog for a while — needs the pricing service to pass the currency at the line-item level.
- After the returns portal launch, some customers reported being able to start a return on an item that was already returned. The API now checks the return status before allowing a new return, but the error message the customer sees is the generic "something went wrong" page rather than something helpful. Cosmetic but annoying.

## Config

All configuration lives in the config service (same as shop-web). Feature flags for orders-web are in the feature flag service under the `orders-web` prefix — see `eng-docs/web/feature-flags.md` for how those are named and rolled out.

Deploys are handled by `deployctl` — the orders-web deploy job is separate from shop-web, so you can deploy one without the other. Worth remembering if you're coordinating a change that touches both.

There is no separate runbook for orders-web — the shop-web runbook (`eng-docs/web/shop-web-runbook.md`) covers the shared infrastructure; if you're on call and something orders-web specific breaks, it's usually the returns API or the mailer queue backing up.

Last edited by Amara Molina.
