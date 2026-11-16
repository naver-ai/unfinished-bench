# ADR 0012: Order events on a shared bus

**Status:** Accepted  
**Owner:** Web (shop-web, orders-web)  
**Last edited by:** Nasser Lund  

## Context

Orders currently flow through shop-web and orders-web with no single, consistent record of order lifecycle events that downstream consumers can rely on. The CRM, the analytics warehouse, the disputes team, and the wholesale arm all need to know when orders are placed, paid, refunded, dispatched, or cancelled. Right now each consumer either polls the orders database or relies on webhooks that only cover a subset of events. This has caused missed refund notifications in the CRM and inconsistent order counts between the warehouse and the finance ledger.

The POS back office in stores also emits order events (in-store sales, click-and-collect orders, returns) but those go through a separate path and never reach the same consumers. Wholesale orders are handled differently again — they're raised in a separate system and only get synced to the warehouse in batches.

## Options considered

1. **Extend the existing webhooks** — cheap to start, but we'd end up with several parallel webhook systems (web, POS, wholesale) and consumers would still need to manage their own retry and deduplication logic. No single ordering guarantee.
2. **Shared order event bus** — a single topic for all order lifecycle events, with event schemas versioned and owned by the Web team. Consumers subscribe once and get a consistent stream. Adds a new piece of infrastructure but reduces point-to-point integrations.
3. **Write-through to the analytics warehouse only** — solves reporting but does nothing for CRM or disputes, and doesn't help with real-time refund checks.

We went with option 2.

## Decision

Adopt a shared event bus for order lifecycle events. The bus is managed by the Platform team, but the schemas and event definitions are owned by Web (shop-web and orders-web). All order events — from the website, the POS back office, and the wholesale order system — must be published to the bus. Consumers (CRM, analytics warehouse, credit control, disputes) subscribe to the bus instead of polling the orders database.

Initial event set:

- `order.placed`
- `order.payment_confirmed`
- `order.payment_failed`
- `order.refunded`
- `order.dispatched`
- `order.cancelled`
- `order.returned`

Events are keyed by order ID and carry a monotonically increasing sequence number per order so consumers can detect gaps or out-of-order delivery. We'll start with at-least-once delivery; consumers must deduplicate. The existing webhooks will be kept for a transition period of a couple of quarters but no new consumers should be added to them.

The POS back office and the wholesale order system will need adapters to publish to the bus. Those adapters will be owned by the respective teams (Retail operations and Supply chain & fulfilment), but the Web team will provide the client library and schema validation.

## Open questions

- Whether gift card redemptions should emit their own event or be folded into `order.payment_confirmed`. Gift cards are being looked at separately by Finance.
- Retention policy for events on the bus — we haven't decided how long consumers can replay from the beginning. Warehouse wants at least a full financial year; that may be expensive.
- Whether to include quote-to-order events from wholesale (when a quote becomes an order) or only the final order placement.

## Follow-ups

- Nasser to schedule a short session with the CRM and credit control teams to confirm the event fields they need for refunds and overdue tracking.
- Web team to publish the first version of the schemas in `data-docs/catalogue.md` once agreed.
- Platform to confirm whether the bus supports schema registry or whether we roll our own validation in the publisher library.
