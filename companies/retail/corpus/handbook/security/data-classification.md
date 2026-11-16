# Data classification

**Owner:** Security engineering  
**Last edited by:** Kasia Vogel (Senior Security Engineer)

This page defines the four data classes we use at Mossgrove and the handling rules that apply to each. If you work with data and are unsure which class it falls into, ask in #security.

## The four classes

| Class | What it means | Examples from our systems |
|---|---|---|
| **Public** | Can be shared with anyone, including outside the company. No adverse impact if disclosed. | Product descriptions and prices on shop-web, store addresses, press releases, the handbook pages marked public, marketing imagery already published. |
| **Internal** | For use within Mossgrove. Disclosure outside the company would be undesirable but not catastrophic. This is the default class for most day-to-day work. | Store sales totals by region, stock levels by warehouse, internal org charts, non-public meeting notes, most chat messages in company channels. |
| **Confidential** | Sensitive business information or personal data where disclosure would cause real harm to individuals or the company. Access is on a need-to-know basis. | Order data (customer name, address, order contents), customer email addresses and phone numbers, employee records in the HR system, supplier pricing and credit terms, wholesale account contact details, card tokens held by the payments platform. |
| **Restricted** | The highest class. Reserved for data where unauthorised access or disclosure could cause serious harm, legal liability, or regulatory penalties. Access is tightly controlled and audited. | Full payment card numbers (PANs) in the clear, bank account details for supplier payments, payroll data, credentials and private keys in the secrets store, data subject access request case files, internal security findings before they are fixed. |

## Handling rules

| Rule | Public | Internal | Confidential | Restricted |
|---|---|---|---|---|
| **Access** | Anyone, including the public | All Mossgrove staff | Staff with a work need; ask the data owner if unsure | Named individuals only; access requests go through Security engineering |
| **Storage** | Company systems only for anything not yet published | Company systems; personal devices allowed for documents that are not sensitive | Company approved systems only (e.g. {{WORKSPACE_SUITE}}, the CRM, the analytics warehouse). No personal devices, no USB sticks | Company approved systems with additional controls (e.g. the secrets store, encrypted drives). Never on a personal device |
| **Transmission by email or chat** | No restriction | Allowed internally | Allowed internally to named recipients who need it; avoid broad channels | Not by email or chat. Use the approved secure transfer method |
| **Sharing outside Mossgrove** | Allowed | See `data-docs/sharing.md` | See `data-docs/sharing.md` | See `data-docs/sharing.md` |
| **Printing** | Allowed | Allowed | Allowed but must be collected promptly from a shared printer | Not allowed on shared printers |
| **Retention** | Per the records retention schedule | Per the records retention schedule | Per the records retention schedule, or per the specific system's retention policy | Per the retention schedule for the specific system. Logs follow `eng-docs/security/log-tiers.md` |
| **Disposal** | Normal deletion | Normal deletion; empty the trash | Shred paper, delete securely from cloud storage | Shred paper, use secure erase for drives. Contact Security engineering before disposing of any device that held restricted data |

## Notes on common cases

- **Order data** is Confidential. This includes any export from the checkout platform, the CRM, or the analytics warehouse that contains customer names, addresses, or order history. Aggregated figures with no personal identifiers may be Internal.
- **Card tokens** are Confidential. They are only useful to the payments platform and should not be copied into other systems. Full PANs are Restricted and should not exist outside the payments platform at all; if you find one in a log or a support ticket, report it in #security rather than copying it further.
- **Employee records** in the HR system are Confidential. Payroll data is Restricted. Line managers can see information about their direct reports but should not export it beyond the HR system.
- **Supplier pricing** and credit terms are Confidential. They are shared with the wholesale team, finance, and the merchandising teams that need them for margin work, but not with customers or with staff outside those teams.
- **Store-level sales and stock figures** are Internal. The wholesale team shares some of this with independent retailers under agreement; that is covered by `finance-docs/wholesale/credit-terms.md`.
- **Marketing lists** are Confidential. Whether a contact is opted in or out is personal data and is handled under `marketing-docs/email/consent.md`.

## If you are unsure

Start with the class that seems most cautious, then ask. The data owner is usually the team that created the data or runs the system it lives in. For anything that sits between Confidential and Restricted, or if the data is about a customer or employee, ask in #security and someone will point you at the right owner.

For sharing data outside Mossgrove, `data-docs/sharing.md` covers the steps and the standard agreement we use with partners.
