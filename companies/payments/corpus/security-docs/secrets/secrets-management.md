# Secrets management

**Owner:** Security engineering  
**Last edited by:** Marek Dvorak (Security Lead)

## Purpose

This document sets out how Kilbarra manages secrets — credentials, API keys, tokens, certificates and other material that authenticates a service or a human to a system. It exists so that secrets are stored in the secrets manager, never in source code, tickets, chat or logs, and so that rotation happens on a predictable calendar.

## Scope

Applies to all production and non-production systems operated by Kilbarra, all employees and contractors, and any service that authenticates to a Kilbarra system. Credentials Kilbarra issues to partners and certificates from the internal CA have their own pages (`security-docs/keys/partner-keys.md`, `security-docs/pki/ca-overview.md`).

## Policy

1. The secrets manager is the only approved store for secrets used by Kilbarra systems and people. This includes database credentials, API keys, tokens, signing keys and service account passwords.

1.1. Secrets must not be written into source code, configuration files stored in git repositories, tickets, chat messages, documents, spreadsheets or anywhere outside the secrets manager.

1.2. If a secret is committed to a repository, tell Security engineering in #security straight away and leave the commit as it is until they have looked at it.

1.3. If a secret appears in a log — application logs, the analytics warehouse or any other system — report it the same way. Security engineering checks whether the log content was exported anywhere.

2. Services fetch credentials at start-up from the secrets manager. No service may read secrets from environment variables set in deployment configuration, from files checked into a repository, or from any other location.

2.1. The secrets manager supports versioned secrets and automatic rotation for supported credential types. Services should use the versioned API so that a rotation does not require a redeploy.

2.2. If a service cannot use the secrets manager natively, it must use a thin wrapper that retrieves the secret at start-up and holds it in memory. The wrapper must not write the secret to disk.

3. Rotation follows the calendar below. Security engineering maintains the calendar in the secrets manager and flags upcoming rotations in #security two working days before they are due.

| Secret type | Rotation frequency |
|---|---|
| Database credentials (production) | Every 90 days |
| Database credentials (non-production) | Every 180 days |
| Internal API tokens | Every 90 days |
| Signing keys for webhooks | Every 12 months |
| Service account passwords | Every 90 days |

3.1. Rotations are performed by the service owner using the secrets manager's versioned secrets, so dependent services pick up the new version without a redeploy.

3.2. A rotation done off the calendar is logged in tickets like any other.

4. Human access to the secrets manager is granted through the access request process in handbook/it/access-requests.md. Access is reviewed quarterly as part of security-docs/access/access-reviews.md.

4.1. Secrets must not be shared between people. Each engineer retrieves their own credentials. If a credential needs to be shared with a service account, that account must be a managed identity in the secrets manager.

5. When a secret is rotated, the service owner must update any dependent systems — the merchant dashboard, the back office, partner feeds, or anything else that consumes the credential. The change record for the rotation should list the dependents checked.

6. If you find a secret outside the secrets manager, do not use it, do not copy it, and do not delete it without telling Security engineering. Report it via #security or the incident process in eng-docs/incidents/incident-process.md.

6.1. If the secret is in a public repository — including any repository outside Kilbarra's control — say so when you report it; Security engineering deals with those first.
