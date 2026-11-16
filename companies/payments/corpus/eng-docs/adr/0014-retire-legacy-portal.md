# ADR 0014: Retire the legacy merchant portal

*Needs updating after the move — ping #platform if something here looks wrong.*

**Status:** Accepted, partly done  
**Owner:** Merchant apps (dashboard & mobile)  
**Last edited by:** Noor Rahman

## Context

The legacy merchant portal (the dashboard before the current one) still serves a handful of pages that were not moved when we consolidated onto the current merchant dashboard. Most merchants were migrated in phases, but a small cohort of long-standing accounts still default to the old portal on login. The portal runs on infrastructure that is no longer patched on the same cadence as the main dashboard, and it holds a separate session store.

## Decision

Retire the legacy portal. All remaining pages have been re-implemented in the merchant dashboard. The old portal will be decommissioned once the last cohort is switched over via the feature flag service. No new development or bug fixes will be done on the legacy codebase, aside from urgent security fixes.

## What was moved

- Statement downloads and transaction exports → dashboard (billing section)
- Payment link creation and management → dashboard (payments section)
- Payout history and settlement details → dashboard (treasury section, read-only)
- VAT invoice downloads → dashboard (billing section)

## Still left

- The "old invoices" page for a small set of merchants whose invoice numbering predates the current billing system. These are rendered from a static export and will not be rebuilt in the dashboard; affected merchants have been written to.

## Loose ends

- The legacy portal's DNS entries and the redirect from the old hostname are handled by the platform team; ticket in #platform tracks the cutover.
- Session store retirement is pending confirmation that no merchant has an open session older than the 30-day idle timeout.
- The mobile apps still reference two legacy portal URLs in their support flow; Dalia has a PR up to point those at the dashboard equivalents.
- Final decommission date is not yet set — depends on the last merchant confirmation.
