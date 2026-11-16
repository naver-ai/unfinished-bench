# Secrets

**Owner:** Security engineering  
**Last edited by:** Ana Quinn (Security Engineer)  
**Applies to:** All staff, contractors, and third parties who handle Mossgrove systems or data.

## Purpose

Mossgrove relies on a large number of credentials — API keys, database passwords, TLS private keys, store POS tokens, wholesale partner tokens, and cloud service accounts. This document sets out how we store, rotate, and protect secrets. It also tells you what to do when a secret gets out.

## Scope

All secrets used for Mossgrove systems, including cloud infrastructure, internal tools, store systems, wholesale integrations, and customer-facing services.

---

## 1. Secrets manager

1.1 All secrets must be stored in the company secrets manager. If a system does not support the secrets manager directly, use the provided sidecar or SDK. Do not keep secrets in local files, shell profiles, or personal password managers.

1.2 The secrets manager is the only place where production credentials live. This includes database passwords, API keys for payment providers, wholesale partner credentials, and the POS back office service account.

1.3 Access to the secrets manager is granted through the access request process in `handbook/it/access-requests.md`. Requests are reviewed by the system owner and the Security engineering team.

1.4 Secrets are grouped by environment (`prod`, `staging`, `dev`) and by service. Never reuse a production secret in a lower environment.

1.5 Store-level secrets (POS tokens, store Wi-Fi credentials) are managed through the POS back office and pushed to devices centrally. Store staff must not be asked to enter or store credentials manually.

## 2. No secrets in repos

2.1 Source code, configuration files, and documentation must not contain secrets. This includes private keys, passwords, tokens, and connection strings with embedded credentials.

2.2 If you need a configuration value that differs between environments, reference it by name and set the actual value in the secrets manager. Do not commit a "default" value.

2.3 Secrets that are found in a repository are treated as leaked (see section 4) and must be rotated promptly.

2.4 The `ledgerctl`, `sharectl`, and `deployctl` tools all accept credentials via environment variables or the secrets manager. Passing credentials on the command line is not permitted.

2.5 When writing runbooks or internal guides, use a descriptive name for the credential rather than the value itself.

## 3. Rotation schedule

3.1 Production database credentials rotate every 90 days. The rotation is automated by the platform team and announced in #releases.

3.2 Cloud provider service account keys rotate every 30 days. Where possible, use short-lived tokens that expire on their own; long-lived keys require Security engineering approval.

3.3 Payment provider API keys rotate every 180 days, or sooner if the provider issues new ones. The checkout team coordinates with Finance operations on this.

3.4 Wholesale partner credentials rotate each quarter. The wholesale team is responsible for letting partners know the new values through the existing partner portal.

3.5 Store POS tokens rotate monthly as part of the standard maintenance window. The stores-ops team runs this via the POS back office and checks the rotation log.

3.6 Any secret that was provisioned for a specific person (e.g., a personal API key) must be rotated when that person leaves the company or changes roles. The HR system triggers this via the offboarding checklist.

## 4. If a secret leaks

4.1 If you believe a secret has been exposed — in a repo, a chat message, an email to an external party, or anywhere else — do not try to delete it and move on. Treat it as compromised and follow this section.

4.2 Immediately notify Security engineering in #security. Include which secret it was, where it appeared, and when you first saw it.

4.3 The Security engineering team will rotate the secret, usually within one working day. For payment or customer data related secrets, the team will also check the relevant logs and may involve the checkout or finance teams.

4.4 Do not continue using the secret while the investigation is under way. If you need the functionality, ask for a replacement secret from the system owner.

4.5 After the secret is rotated, the incident is logged in the tickets system with the `security` category. The person who spotted the leak does not need to file a separate helpdesk ticket.

4.6 If the leak was caused by a commit to a repository, the commit history must be rewritten to remove the secret from history. The platform team can assist with this. Do not attempt this alone if you are not familiar with history rewriting.

## 5. Related documents

- `eng-docs/security/access-reviews.md` — who has access to what
- `eng-docs/security/vuln-management.md` — handling vulnerabilities in systems that hold secrets
- `handbook/security/incident-reporting.md` — reporting a security incident
- `handbook/it/access-requests.md` — requesting access to the secrets manager
