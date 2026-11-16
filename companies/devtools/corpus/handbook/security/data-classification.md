# Data classification

**Owner:** Security  
**Last edited by:** Daniela Ferraz

Gantline data falls into one of four classes. The class of a piece of data determines where it may live inside Gantline and who can see it. When in doubt, assign the higher (more restrictive) class and ask Security.

| Class | What it covers | Examples |
|---|---|---|
| **Public** | Data Gantline intentionally publishes or that is openly available. | `gnt` source code, public docs on docs.gantline.dev, blog posts, marketing pages, the status page. |
| **Internal** | Data used to run Gantline that is not public and not sensitive enough to be restricted. | Internal RFCs and eng-docs, most of the handbook, internal runbooks, non-public meeting notes, internal metrics dashboards. |
| **Confidential** | Data that could harm Gantline or its customers if disclosed broadly. Access is on a need-to-know basis. | Customer account records, billing records, customer pipeline configurations, sales deal data, employee HR data, workforce SSO configuration, secrets (see `eng-docs/security/secrets.md`). |
| **Restricted** | Data whose disclosure would cause serious harm to Gantline or a customer. Access is individually granted and audited. | Customer source code hosted on Gantline Cloud, customer private keys or credentials, legal holds and litigation materials, board materials, incident forensics. |

## Labelling

We do not have a formal label to apply to every file or message, but documents and dashboards should state their class in the header or title where it is not obvious. For example, an eng-doc that discusses customer data flows should say "Confidential" near the top. A slide deck that will be shown to a customer should be "Public" unless it contains internal metrics.

## Storage and access

The table below is the baseline. If a system is not listed, treat data stored there as at most one class above the least restrictive system you would reasonably put it in, and check with Security.

| Class | May be stored in | May be seen by |
|---|---|---|
| **Public** | Any Gantline system, the public internet, customer-facing docs and repos. | Everyone, including outside Gantline. |
| **Internal** | Gantline Cloud (internal teams and repos), chat, the admin console, the metrics dashboards, the wiki, the HR system (for non-HR internal data, generally not appropriate — use the HR system only for HR data), the CRM (only where the data is not customer-identifying). | All Gantline employees and contractors with the relevant system access. |
| **Confidential** | Gantline Cloud (private repos), the admin console, the CRM, the billing service, the data warehouse, the helpdesk, the expenses tool, the HR system. Must not be stored in public repos, public gists, or on laptops outside Gantline's device management. | Employees and contractors whose role requires it. For customer data, the customer's assigned account team, the billing and support teams, and the relevant engineering teams (e.g. SRE for incident response). |
| **Restricted** | Gantline Cloud (private repos with restricted team access), the lab, the artifact store (for customer build artifacts), the secrets store. Must not be copied to chat or the helpdesk. | Named individuals only, as granted by Security or the data owner. Access is reviewed on a schedule. |

## Notes and edge cases

- **Customer source code** is always Restricted, even if the customer has a public repo. We host it in isolated storage and access is limited to the customer's support and engineering contacts.
- **Aggregated metrics** (e.g. "how many builds per day across all customers") are Internal. Any metric that can be broken down to a single customer is Confidential.
- **Logs** from Gantline Cloud services may contain customer identifiers (usernames, repo names, IP addresses). Treat logs as Confidential.
- **Chat history** — treat chat as Internal by default. If you post customer billing details or source code excerpts to chat, you are creating a Confidential or Restricted copy in a system that is not approved for it. Don't.
- **Public repos** on Gantline Cloud are Public only if the repo itself is public. A private repo that is shared with a customer is still Confidential (or Restricted, if it contains customer source).
- **HR data** is Confidential. Salary, performance reviews, and medical or family data are Restricted. See `bizops-docs/people-ops/hris.md` for where HR records live.
- **Press and social** — anything you post to public channels is Public, of course. For what you may say about Gantline's roadmap or customers, see `handbook/comms/talking-to-press.md`.

## Changing a class

If you believe data should move up or down a class, raise it in #security. The Head of Security approves any move to a less restrictive class. Moving data to a more restrictive class is usually fine but should still be noted in the relevant repo or ticket so it is not later downgraded by accident.

## Related

- `eng-docs/security/secrets.md` — secrets and credentials
- `handbook/security/reporting-an-incident.md` — what to do if you think data was exposed
- `bizops-docs/cs/vendor-feeds.md` — customer data shared with vendors
- `infra-docs/cloud/accounts-and-regions.md` — where data lives and the EU region rule
