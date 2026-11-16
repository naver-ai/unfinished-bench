# Secrets

**Owner:** Product security  
**Last edited by:** Connor Meyer (Application Security Engineer)

**Purpose.** Gantline services and developer tooling depend on secrets — API tokens, signing keys, database credentials, and similar material. This document sets the rules for storing, reading, rotating, and responding to leaks of secrets across gnt, Gantline Cloud, and internal infrastructure.

**Scope.** Applies to all Gantline employees, contractors, and any system that runs under Gantline's control, including the lab and build farm. Customer-provided secrets (for example, a token a customer pastes into a pipeline) are covered by the same storage rules.

## 1. Secrets manager

1.1. All secrets must be stored in the secrets manager. The secrets manager is the single source of truth for secret values; there is no separate vault or local keyring that holds production credentials.

1.2. Access to the secrets manager is granted through the identity system. Requests to add or change access go through the normal access process in the handbook (`handbook/it/getting-access.md`). Product security reviews access quarterly.

1.3. Secrets must be referenced by path, never by value, in configuration files. A reference looks like `secrets://<service>/<key>` and is resolved by the service at start-up.

1.4. Secrets manager entries must include an owner (a team, not a person) and a rotation date. The rotation date is enforced by the secrets manager; entries past their date appear in the weekly report to #security.

## 2. Reading secrets at start-up

2.1. Services read secrets at process start-up only. Once a process has started, it must not re-read the secrets manager unless it is restarting. This keeps behaviour consistent during a rotation.

2.2. Services must fail to start if a referenced secret is missing or unreadable. A service that starts with a default or empty value for a secret is a misconfiguration and will be treated as an incident.

2.3. Secrets are never written to disk by the runtime. If a service needs to pass a secret to a child process, it does so through the environment for the lifetime of that child.

## 3. Keeping secrets out of repositories

3.1. Secret values must never be committed to any git repository, including private repositories. This applies to gnt source, Gantline Cloud services, internal tooling, and documentation repositories.

3.2. If a secret value is needed for local development, use a local override file that is git-ignored. The file must contain only references, not values; values come from the secrets manager or a local developer copy of the secret store.

3.3. The pre-commit hook in the Gantline repositories scans for secret-shaped values. A commit that trips the hook is blocked; do not bypass the hook to push a value. If the hook produces a false positive, open a ticket with #security.

3.4. Service logs go through the logging layer's filters, which catch most secret-shaped values in our own services' output. The filters are not a substitute for 3.1.

## 4. Rotation schedule

4.1. Rotation happens on a fixed schedule per secret class:

- Signing keys for releases: every 12 months.
- Database credentials: every 6 months.
- API tokens for external services: every 6 months.
- CI runner tokens: every 3 months.
- Emergency access credentials (break-glass): after every use, and at least every 12 months.

4.2. The rotation date in the secrets manager is the date the value is replaced, not the date the new value is generated. Plan rotations so the new value is available at least two working days before the old value expires.

4.3. Rotations are performed by the team that owns the secret. If the owning team does not rotate by the due date, Product security will start a ticket and may rotate on their behalf.

4.4. After a rotation, anything that cached the old value must be restarted. The restart is part of the rotation; do not leave services running with a stale secret beyond the next deploy.

## 5. Leaks

5.1. If a secret is leaked — committed to a repository, posted in chat or pasted into a ticket — the first action is to rotate the value. Rotate immediately; do not wait for a post-mortem or an incident review to start.

5.2. After rotating, notify #security in the `#security` channel. Include the secret's path, when it was rotated, and what you know about the exposure. Do not include the secret value in the message.

5.3. If the leaked secret is a release signing key, also notify #releases so that any artifacts signed with the old key can be identified and re-signed if needed.

5.4. If the leaked secret belongs to a customer (for example, a token a customer shared for support), notify #support so they can coordinate with the customer. The rotation still happens first.

5.5. Product security will follow up on every leak report within one working day. Until the follow-up is resolved, keep the relevant service or repository in the state it was in after the rotation; do not revert the rotation.
