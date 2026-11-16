# Security design reviews

**Owner:** Application security  
**Last edited by:** Samir Haddad (Application Security Engineer)

## When to ask for a review

- Any new service, API, or integration that handles merchant, cardholder, or partner data.
- Changes to authentication or authorisation boundaries, including how API keys are issued.
- Anything that touches PCI DSS scope, safeguarding, or cardholder data environments.
- Major refactors of existing payment processing paths, even if the external behaviour is unchanged.

If you are unsure whether your change needs a review, ask in #appsec. A quick conversation is cheaper than a review request that gets bounced.

## The intake form

- File a ticket in `tickets` under the "Security review" category, or use the form in the #appsec channel bookmark.
- Include: what you are building, the data involved (use the data classification guide), who the users are, and whether it touches any regulated flows.
- Link the design doc or ADR. If it is an ADR, also link the relevant `eng-docs/adr/` entry.
- Name the engineering lead for the work; they are the point of contact for follow-ups.
- Do not start the threat-modelling session until the form is complete. Incomplete forms get sent back.

## The threat-modelling session

- A 45-minute session with the engineering team and one appsec reviewer. Usually via video call; Dublin people join from the office if they are in.
- The reviewer walks through the data flow diagram you provided. We will draw on a whiteboard if there is no diagram yet.
- Come with the main components, trust boundaries, and where data is stored or transmitted. It is fine to sketch it during the session.
- The session is not a gate on its own; it produces the list of findings the team works through.

## What reviewers look at

- **Authentication and session handling** — how tokens are issued, rotated, and revoked.
- **Authorisation** — who can call what, and whether the merchant or partner boundary is enforced server-side, not just in the UI.
- **Data at rest and in transit** — encryption, key management through the secrets manager, TLS configuration.
- **Secrets and credentials** — no keys in code, config, or logs; use the secrets manager.
- **Input handling** — validation, size limits, and whether the payload can reach parts of the system it should not.
- **Logging and monitoring** — whether the flow emits the events SOC and the transaction monitoring system need, and how long those logs need to be kept.
- **Failure modes** — what happens when a downstream service times out, and whether the error path leaks data or bypasses checks.
- **Operational changes** — whether the change needs configuration work from another team, and whether that team knows.

## Typical turnaround

- Initial response to the intake form within one working day.
- Threat-modelling session within three working days of the complete form.
- Written findings within two working days after the session.
- Larger reviews (new platform products, new partner programme) are scoped with the team; expect a longer cycle and a named reviewer.

## After the review

- Findings are tracked in the same `tickets` ticket. Each finding has an owner and a target to close.
- Anything marked "must fix before launch" blocks the release train; work with the Developer Platform team on timing.
- If a finding is disputed, bring it to the Application Security Lead rather than resolving it informally in the ticket.

For anything urgent (active incident, data exposure in production), skip the form and page the appsec on-call via the paging tool, then follow up with the ticket.
