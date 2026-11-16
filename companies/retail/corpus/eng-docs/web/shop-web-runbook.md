# shop-web runbook

Owner: Web (shop-web, orders-web)
Last edited by: Wei Murray

## Architecture sketch

shop-web is the storefront serving the public site (UK, IE, US). It sits behind the CDN and talks to orders-web for order placement and account-related calls. The main moving parts:

- **Edge / CDN** — terminates TLS, serves static assets, caches product pages briefly.
- **shop-web app** — the server-rendered storefront. Product listing, product detail, basket, and the checkout flow (which hands the order to orders-web).
- **orders-web** — the order service: places the order when checkout submits it (the payment call and the order write), and serves order history and the returns portal. Owns the order write path and talks to the payments platform and the analytics warehouse. More in `eng-docs/web/orders-web.md`.
- **Feature flag service** — consulted at request time for gradually rolled-out UI changes and checkout experiments.

Deploys go through deployctl. The app runs as a set of containers in the platform cluster; there is no meaningful state in shop-web itself.

## Common alerts

### 5xx rate above threshold

The alert fires when the 5xx share of shop-web traffic crosses 1% over a five-minute window.

1. Open the metrics view for shop-web (`shop-web` service dashboard).
2. Check whether the errors are concentrated on a specific route (product pages, checkout, basket) or spread across everything.
3. If it is checkout-related, look at orders-web latency — a slow downstream can surface here as timeouts. The checkout timeout is generous, but if orders-web is struggling you will see it in their metrics too.
4. If it is a single route, check the feature flag service for a recently flipped flag that might have changed behaviour on that page. The feature flags are in the feature flag service console; look at flags touched since the last deploy.
5. If a recent deploy is the likely cause, see "If it goes wrong" below for putting the previous build back.

### Checkout latency p95 above 2 seconds

A slow checkout usually means orders-web or the payments platform is slow.

1. Open the orders-web dashboard and look at p95 latency for the order placement endpoint.
2. If orders-web looks fine, check the payments platform status channel (`#payments-platform`) — if they have an incident, follow it there.
3. If nothing downstream looks wrong, check shop-web for a slow query or a bad dependency call. The app publishes its own request timings; look for a route where p95 jumped.
4. If the cause is not obvious, capture a thread dump from one of the shop-web instances and look for blocked calls. The instance IDs are in the cluster console.

## Feature flags service

shop-web consults the feature flag service at request time. Flags are grouped by app name; the shop-web group is `shop-web`.

To look up a flag:

1. Open the feature flag service console and select the `shop-web` group.
2. Find the flag by name. Flags should be named after the ticket they came from (e.g. `wc-3142-basket-promo`).
3. The flag page shows the owner team, the rollout per environment and the recent changes with who made them. How rollouts are staged is in `eng-docs/web/feature-flags.md`.
4. Changes to a flag reach the running app within a minute, so a flag changed shortly before an alert is worth a look.

Flags are not a substitute for a deploy — if a flag has been off for more than a quarter, it should be removed in the next shop-web change.

## Rolling restarts

A rolling restart is the usual first step when shop-web is misbehaving but the metrics do not point at a clear cause. A restart does not change any settings: instances come back with the live values from the config service (see `eng-docs/platform/runtime-config.md`).

1. Open the cluster console and select the `shop-web` service.
2. Choose "Rolling restart".
3. Set the batch size to 2 (the default). Confirm.
4. Watch the service dashboard — each batch should come back healthy before the next one starts. If a batch fails, the restart pauses; check the logs for that instance before continuing.

The whole restart takes about ten minutes. The app drains connections on shutdown, so in-flight requests should complete.

## Contacts

- Web team: `#platform` (there is no `#shop-web` channel)
- Platform & SRE: `#platform` / `#incidents`
- Payments platform: `#payments-platform`
- Data engineering (for warehouse/analytics questions): `#data-eng`
- On-call escalation: see eng-docs/oncall/oncall-guide.md

For incidents, follow eng-docs/oncall/incident-process.md. The Web team's primary contact is Nasser Lund; if he is away, escalate through `#incidents`.

## If it goes wrong

- If you suspect a bad deploy, put the previous good build back with deployctl: `deployctl history shop-web --env production` lists what went out, and `deployctl deploy shop-web <version> --env production --change CHG-XXXX` deploys that version again.
- If the CDN is serving stale or broken content, check with the platform team — the CDN config lives in the DNS repo (eng-docs/platform/dns.md) and is managed by SRE.
- If you need to take shop-web down for maintenance, put a maintenance page up at the CDN layer first, then stop the service. Do not stop the service first.
- For database-related issues, shop-web does not talk to the database directly — it is orders-web that owns the data. If orders-web is down, the storefront will show errors on basket and checkout but product browsing will still work. In that case, `eng-docs/web/orders-web.md` has its dependencies and known issues.

## Notes

- The old `shop-web-deploy` script in the tools repo is deprecated — use deployctl.
- The feature flag service moved to a new console last year; the old URL redirects but does not show all flags.
- Some of the product page caching is done at the CDN layer; if you change a product page template, the CDN cache may need to be purged. The purge button is in the CDN console under "Cache actions".
