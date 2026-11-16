# Webhooks

**Owner:** Integrations & partners  
**Last edited by:** Malik Lund (Solutions Engineer)

## Event types

Webhooks cover the main lifecycle events merchants care about: payment succeeded, payment failed, payout completed, payout failed, and balance threshold alerts. Each event carries the standard payload envelope (event ID, type, occurred-at, data object). Event types are versioned; merchants pin the version in the dashboard when they set up the endpoint.

New event types are additive. We do not change the shape of an existing event type without a deprecation window of at least three working days on the public changelog and a merchant notice.

## Delivery and retries

Delivery is at-least-once. We send an HTTP POST to the registered URL with the signature header (see below). If the endpoint returns anything other than 2xx, we retry on this schedule:

1. 30 seconds after the first attempt
2. 5 minutes after that
3. 30 minutes after that
4. 2 hours after that
5. 6 hours after that
6. 24 hours after that

After the last attempt, the event is marked failed and appears in the merchant dashboard under **Webhooks → Failed events**. Merchants can manually replay from there, or you can do it from the back office (below).

We time out after 10 seconds and do not follow redirects. Endpoints must be HTTPS with a valid public certificate.

## Signatures and rotating the secret

Each webhook endpoint has a signing secret. We sign the raw body with HMAC-SHA256 using that secret, and send the result in the `Kilbarra-Signature` header as `t=<timestamp>,v1=<hex digest>`. Merchants verify against the body exactly as received — any whitespace or re-encoding on their side breaks verification, so we point them at the sample verifier in the docs.

Rotation is self-serve in the merchant dashboard:

1. Go to **Developers → Webhooks → [endpoint] → Signing secret**.
2. Choose **Generate new secret**. The old secret stays valid for 24 hours from generation.
3. Update the endpoint code with the new secret.
4. Optionally, click **Revoke old secret** in the dashboard once traffic is confirmed on the new one. If they leave it, it expires automatically.

If a merchant has lost the secret and cannot verify, they can regenerate from the dashboard at any time. Support cannot read the secret, but can confirm when it was last rotated.

## Replaying events from the back office

For a merchant who needs a replay (for example, their endpoint was down for an extended window and the retries exhausted), use the back office:

1. Open the merchant in the back office and go to **Integrations → Webhook events**.
2. Filter by event type, date range, or status (failed/delivered).
3. Select the events to replay — you can select all in a filter, or pick individually.
4. Click **Replay selected**. Events go straight back into the delivery queue with the same retry schedule.
5. Confirm the merchant sees the deliveries on their side. If the endpoint is still failing, stop and check with Integrations engineering before re-replaying.

Replays are logged against your back office user, and the merchant sees a note on the event in their dashboard.

## Common merchant questions

- **Why did I get the same event twice?** At-least-once delivery means duplicates are possible. Merchants should dedupe on the event ID.
- **Can I get an event in a different format?** No. If they need a different shape, point them at the platform API — the webhook payload matches the API response objects.
- **How fast will I get the event?** For successful payments, we aim for delivery within a few seconds of the ledger write. Payouts can take a bit longer because of the batch cycle.
- **My endpoint is down for maintenance. Can I pause webhooks?** No, but they can close the endpoint and let retries run, then replay after. The 24-hour retry window usually covers short maintenance.

## If it goes wrong

- **Merchant says they are not receiving events** — check the events list in the back office first. If the events show delivered, the signature or the endpoint code is the issue. Ask the merchant to check their logs for the delivery attempt.
- **Signature verification failing after a rotation** — almost always a copy-paste issue with the new secret, or they are verifying against a re-encoded body. Get them to compare the raw body bytes.
- **Events stuck in retry with no end** — the endpoint is returning 5xx or timing out. Check the delivery log for the status code and timing, and check the endpoint is not behind a firewall that drops our IP ranges. We publish those ranges in the dashboard.
- **Replay is not delivering** — the endpoint is likely still failing. Confirm with the merchant before retrying; otherwise you are just hammering a broken URL. Escalate to Integrations & partners if the endpoint looks unreachable from our side.
