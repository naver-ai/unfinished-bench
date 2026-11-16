# DNS and domains

*Needs updating after the registrar move — ping #platform if something here looks wrong.*

Owner: Infrastructure · Last edited by Tariq Beaumont.

## Where zones live

All public and internal zones are in our primary DNS provider, except `kilbarrapay.com` itself, which still sits with the old registrar from before the move. The move was meant to bring everything under one roof; the domain remains with the previous registrar because the transfer request stalled on the administrative contact. Lena Voss has asked #platform to chase it, but it keeps dropping off the queue. The zone is managed in the same tool and updates propagate fine — only the registration itself is still split.

## Requesting a record

Open a ticket in tickets with the `dns` tag and name the owning team. Infrastructure reviews and applies changes within one working day for normal requests. For anything urgent, page the Infrastructure on-call through the paging tool. Records that point to partner systems should be requested through the partner integrations team so they can confirm the destination is current.

## TTLs

Standard TTL for most records is 300 seconds. For failover and health-check records, use 60 seconds. For the few records that genuinely never change — like the root `kilbarrapay.com` NS set — 86400 is acceptable, though the split registration makes us keep the root TTL at 300 until the move completes.

## Merchant custom domains

Merchants can use their own domain for hosted checkout. They add a CNAME to `checkout.kilbarrapay.com`, and the edge provisions a public certificate for it automatically. The edge team confirms the domain resolves before enabling it. Merchant success has the checklist for what the merchant needs to do on their side; the actual record lives in the merchant's own DNS, not ours, so we cannot create or edit it for them.
