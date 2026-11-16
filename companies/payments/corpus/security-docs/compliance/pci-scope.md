# PCI DSS scope

**Owner:** Governance, risk & controls testing  
**Last edited by:** Ben Abara

## Context

We hold cardholder data in a small number of places and we want the scope statement to reflect that. The QSA has seen the network diagrams from eng-docs/architecture/overview.md and agrees with the boundary we've drawn around the card vault and the payments gateway. This note records what is in scope, what is out, and the evidence folders we keep for the annual assessment.

## In scope

- **Card vault** — the service that stores PANs and the database behind it. This is the only place we store card numbers at rest.
- **Payments gateway** — the service that accepts card transactions from the merchant dashboard and the API, and the network segments that carry traffic between the gateway and the vault.
- **The network segments** that connect the gateway, the vault, and the core ledger where authorisation responses are logged. The segment boundaries are the ones marked on the diagram in the architecture overview; the QSA signed off on those boundaries last year and we've not changed them since.
- **Administrative access paths** to the above — jump hosts and the service accounts used to deploy or configure the gateway and vault. The list of accounts is in the access review pack.

## Out of scope

- **The core ledger** — it stores transaction metadata but no PANs. Token references only.
- **The treasury workstation**, **reconciliation tool**, and **settlement and payouts** flows — they consume tokens, not card numbers.
- **The analytics warehouse** — no PANs are loaded there. The data classification policy says cardholder data stays out of the warehouse and the pipeline checks enforce it.
- **Partner platforms** — platform partners never see card numbers; the gateway tokenises before anything leaves our network.
- **Merchant devices and browsers** — card entry happens on our hosted fields, so the merchant never has to touch PCI scope themselves.

## Annual assessment

- The assessment runs yearly, timed so the report is ready for the renewal of our sponsor bank arrangement. The QSA lead is the same firm we've used for the last two years.
- **Nadia Petrov** coordinates the evidence collection. The controls testing team pulls the evidence folders together.
- **Isaac Chowdhury** reviews the draft before it goes to **Dovile Kazlauskaite** for sign-off.
- The QSA visits the Dublin office for the walkthrough; Vilnius and Austin join remotely. There's no on-site requirement at the other sites because the in-scope systems run in the Dublin data centre.

## Quarterly external scans

- Scans run on a quarterly cadence against the external-facing IPs that terminate traffic to the gateway. The scan vendor is the same one the QSA recommended.
- Results go to the controls testing team. **Imani Ahmadi** triages the findings and tracks remediation in the tickets system.
- A clean scan report needs to be on file before the annual assessment starts; if a scan comes back with findings, the owning team fixes them and the scan is re-run.

## Evidence folders

The controls testing team keeps the following in the `security-docs/compliance` area:

- **Network diagrams** — current versions, updated whenever a change touches the in-scope segments. The change management process in eng-docs/platform/change-management.md requires a note in the ticket when a change affects scope.
- **Configuration baselines** — the gateway and vault configs as deployed, pulled from the config repo at each assessment.
- **Access reviews** — the quarterly access review output for the service accounts and jump host access, as per security-docs/access/access-reviews.md.
- **Scan reports** — the last four external scan reports plus any remediations.
- **Training records** — completion records for the PCI training module for the teams who touch the in-scope systems. This lives in the learning platform and the controls team exports it for the assessment.

## Loose ends

- The QSA asked us to confirm that the card vault's backup media is encrypted at rest. The backups team has confirmed it is, but we need to add the backup job details to the evidence folder before the next assessment.
- We need to update the network diagram to show the vault's read replicas. They were added last year and the diagram still shows a single vault node.
- The merchant dashboard shows the last four digits of the card on the payment methods page. That's fine, but we should note in the evidence that truncated PANs are displayed and not stored in the dashboard's own database.
