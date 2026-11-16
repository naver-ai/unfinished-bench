# DNS

> Needs updating after the move — ping #platform if something here looks wrong.

Public zones for mossgroveoutdoor.co.uk and the store/wholesale subdomains live in Route 53. The legacy registrar still holds the root zone for the old .ie domain used by the Dublin office intranet — that's the half-done bit. Migration is tracked in tickets, most of the work is waiting on the Irish legal entity to confirm the transfer auth code.

To request a record, open a ticket in `tickets` with the hostname, record type, TTL, and the owning team. Platform & SRE reviews and applies. Changes to the root zone or anything that affects outbound mail (SPF/DKIM) need a second pair of eyes from the team — usually Dalia or Owen.

TTLs: default 300s for anything fronted by the CDN, 600s for internal services, 3600s for MX and TXT. The old registrar's zone still uses 86400s on everything; we'll drop those when the zone moves.

The shared `mailer` hostname is still pointing at the old registrar's nameservers on the .ie zone — the UK zone is fine. Wholesale partners using the legacy FTP endpoint for order files are unaffected, but the DNS for that endpoint is also still on the old registrar.

Loose ends: finish the .ie zone transfer, update the runbook reference in `eng-docs/oncall/oncall-guide.md` (it points to the old registrar's console), and sweep the access review list for anyone who still has credentials to the old registrar console.
