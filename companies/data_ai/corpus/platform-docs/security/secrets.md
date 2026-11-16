# Secrets

**Owner:** Cloud security  
**Last edited by:** Bianca Patel (Head of Cloud Security)  
**Applies to:** All staff, contractors, and systems that handle Brakwater credentials or customer-facing keys.

This document sets the rules for storing, rotating, and responding to leaks of secrets. It covers the secrets manager, repository hygiene, rotation for customer-facing keys, and the leak response steps.

---

## 1. Secrets storage

1.1 All credentials, API keys, tokens, certificates, and connection strings must be stored in the secrets manager. The secrets manager is the only approved store for non-human credentials.

1.2 Do not store secrets in source code, configuration files committed to git, notebook files, shell history, or any file that is shared through chat, email, or the helpdesk.

1.3 The secrets manager entry must include: the system or service it belongs to, the owner team, and a rotation date where one applies. Entries without an owner team will be flagged by Cloud security and may be disabled.

1.4 Service accounts and machine identities must use the secrets manager for their credentials. If a system cannot integrate with the secrets manager, contact Cloud security before creating any long-lived credential outside it.

## 2. Repositories and notebooks

2.1 Before pushing any change, check for secrets in the diff. If a secret is pushed, treat it as leaked — follow section 4 immediately, even if the repository is private.

2.2 Secrets that appear in notebooks must be removed from the notebook and rotated. Cloud security runs periodic scans of the notebook server; findings are routed to the workspace owner.

2.3 Do not use personal access tokens or personal passwords in shared scripts, pipeline definitions, or automation. Use service account credentials from the secrets manager instead.

## 3. Rotation schedule for customer-facing keys

3.1 Customer-facing API keys (including keys issued through the customer API console) rotate on a fixed schedule: every 90 days. Keys issued for imagery tasking orders or data deliveries follow the same schedule.

3.2 When a customer-facing key is rotated, the new key must be active before the old one expires. Coordinate the handover through the customer's onboarding contact and log the change in tickets.

3.3 Keys used for partner integrations (including imagery delivery to partners) rotate every 180 days unless the partner contract specifies a shorter interval. The integration owner is responsible for scheduling the rotation.

3.4 Internal keys used for warehouse connections or the batch cluster do not have a fixed rotation interval but must be rotated when a team member with access to them leaves Brakwater or changes roles.

## 4. Leaked secrets

4.1 If you suspect a secret has leaked, do not wait for confirmation. Rotate the secret immediately if you can, then report it through the incident process in `platform-docs/oncall/incident-process.md`.

4.2 When reporting a leak, include: which secret, where it was found (repository, notebook, chat, email, external site), when it was first committed or shared, and who has access to the location where it was exposed.

4.3 After rotation, check the helpdesk for any customer reports that might relate to the exposed key. If the leak involves a customer-facing key, inform the affected customer through their normal support channel.

4.4 Cloud security will follow up on every leak report to confirm the secret was rotated and to determine whether the exposure path needs a fix. Do not close the incident until Cloud security confirms it is resolved.

## 5. General hygiene

5.1 Do not share secrets in chat, even in private messages. Use the secrets manager's sharing feature or create a scoped credential for the person who needs access.

5.2 When a secret is no longer used, remove it from the secrets manager and rotate any dependent credentials.

5.3 Questions about secret handling go to #security. Suspected leaks go to #incidents.
