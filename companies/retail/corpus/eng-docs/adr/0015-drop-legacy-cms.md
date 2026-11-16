# ADR 0015: Retire the legacy CMS

> Needs updating after the move — ping #platform if something here looks wrong.

## Status
Accepted, partly done.

## Context
The legacy CMS still hosts the product pages for the remaining non-transactional content (store locator, wholesale catalogue PDFs, garden centre lookbooks) and the old blog. The Web team has been gradually moving content into the current shop-web platform since the beginning of the financial year, but a long tail of pages was left behind because they didn't fit the standard page template or were owned by other teams.

## Decision
Retire the legacy CMS. Content moves as follows:

- Store locator and opening hours → shop-web, using the existing store data feed that the POS back office already publishes.
- Wholesale catalogue PDFs and garden centre lookbooks → moved to the wholesale section of the public site, with the old URLs redirecting permanently.
- The blog → consolidated into the marketing site; old posts that are more than two years old are not being migrated, and the marketing team has confirmed they don't need the archives.
- Remaining pages that have no equivalent on shop-web (e.g. the old store-specific landing pages, the "about our fabrics" section) will be reviewed case by case by the Web team and either rewritten or decommissioned.

## Loose ends
- Redirect map is in sharectl but hasn't been fully tested against the live store routes. Tariq to co-ordinate with #releases before switch-off.
- The legacy CMS still receives writes from the wholesale team for the PDF library; that workflow needs to move to the shared drive first.
- A handful of pages are still only linked from the legacy sitemap and have no external inbound links — those will be dropped without redirects.
- The old CMS database will be kept read-only for one more quarter after the switch-off, then the snapshots will be deleted per records retention.

## Owner
Web (shop-web, orders-web). Last edited by Tariq Mahlaba.
