# Analytics API runbook

**Owner:** Web app and API  
**Last edited by:** Zeynep Kruger (Frontend Engineer)

## Purpose

Operational notes for the Analytics API — the public-facing endpoint that serves monitoring data, derived products, and analytics payloads to subscription customers. This covers day-to-day operations, common alerts, and recovery steps.

## Architecture sketch

```
Customer → API gateway → /tiles/*  → tile service → cache → imagery catalogue
                        → /query/* → query service → cache → warehouse
                        → /usage/* → usage meter  → warehouse (usage schema)
```

- **API gateway** — handles auth, rate limiting per customer key, and request routing. TLS terminates here.
- **Tile service** — serves raster tiles (flood extents, soil moisture, vegetation indices) from the imagery catalogue, with a {{CACHE_DB}} cache in front.
- **Query service** — serves JSON responses for time-series and area summaries. Reads prepared tables in the `marts` schema of the warehouse.
- **Usage meter** — tracks API calls per customer key and writes usage events to the warehouse for billing. The meter lags by up to an hour; that is expected.

## Common alerts

### 5xx rate above 2% (gateway)

The gateway checks the 5xx share over a 5-minute window.

1. Open the gateway dashboard in the BI dashboards (look for "Analytics API gateway").
2. Check which endpoint is failing: /tiles or /query.
3. For /tiles: check the tile service CPU and cache hit rate. If cache hit rate dropped below 60%, check whether a new imagery layer was published recently (see data-docs/pipelines/imagery-ingest.md) — the cache may have been invalidated.
4. For /query: check the query service log for warehouse timeouts. If the warehouse itself is slow, ask in #data-platform.
5. If the gateway itself is the problem, do a rolling restart (below).

### Tile latency p95 above 3s

1. Check the tile service latency panel in the same dashboard.
2. Check cache hit rate. If low, check whether a large AOI order was recently processed (see data-docs/customers/aoi-orders.md) — those can flood the tile service with cold requests.
3. Check in #imagery-ops whether a large reprocessing run is going — those compete for disk I/O.
4. If the tile service has been up for more than a week, do a rolling restart — memory fragmentation has caused slow lookups before.

### Usage meter lag above 4h

The meter normally lags by up to an hour. If lag exceeds 4 hours:

1. Check the meter's log in the workflow scheduler for the "usage meter" job.
2. The meter reads from the gateway access logs. If the gateway was restarted recently, the log stream may need to be picked up again.
3. Restart the meter job from the scheduler. If it fails again, contact the Web app and API team in #apps.

## Rolling restart

Restart the API services without dropping in-flight requests.

1. Open the customer API console (internal admin view) and confirm there is no active incident.
2. In the cloud console, open the instance group for the service you are restarting:
   - `analytics-gateway` for the gateway
   - `analytics-tile` for the tile service
   - `analytics-query` for the query service
3. Set the max unavailable to 1 and max surge to 1.
4. Trigger a rolling restart from the instance group page.
5. Watch the gateway 5xx rate and latency panels for 10 minutes after the restart completes.

The whole process takes about 5 minutes per service. Do not restart the gateway and the query service at the same time.

## Rate limits per customer key

Rate limits are set per customer key in the customer API console.

- Standard subscription: 300 requests/minute per key.
- Enterprise subscription: 1200 requests/minute per key.
- Imagery tasking customers get a temporary limit of 3000 requests/minute for 5 working days after delivery.

To change a limit:

1. Open the customer API console.
2. Go to the customer's key settings.
3. Update the request/minute value and save.
4. The change applies within 60 seconds. No restart needed.

If a customer exceeds their limit, they receive HTTP 429. The response includes a `Retry-After` header. Requests for a higher limit go to Pricing and commercial analytics, who handle rate limit exceptions.

## Contacts

- **Web app and API team** — #apps (primary)
- **On-call** — see platform-docs/oncall/oncall-guide.md
- **FinOps** — #finops (for usage cost questions)
- **Support systems** — #support (for customer-facing incidents)

Unless it is an active incident, post in #apps first. The on-call rotation covers the hours outside the Rotterdam working day.

## If it goes wrong

1. If the API is partially down, do not restart everything at once. Restart one service, watch the metrics, then move on.
2. If a customer reports incorrect data (not just an outage), check the query service logs first — most data issues are in the warehouse tables, not the API. Point the customer to the status page and update it if needed.
3. If the gateway is returning 502s, check whether the tile or query service is accepting traffic. A 502 usually means the upstream is down.
4. For anything that looks like a security issue (unusual traffic, auth failures), follow handbook/security/incident-reporting.md and post in #security.
5. If you need to roll back a deployment, use the previous image version in the instance group — do not rebuild from source during an incident.

## Out-of-date notes

The rate limit page in the customer API console was recently moved under "Billing" — the old direct link may not resolve. If you cannot find it, navigate from the console home page. Also, Joanna Ndlovu used to own the query service; she has moved to the tasking portal work, so direct query service questions should go to the #apps channel now.
