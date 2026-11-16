# Data classification

**Owner:** Security engineering  
**Last edited by:** Chidi Kato (Security Engineer)

## Purpose

This document defines the four data classes used across Kilbarra and how to apply them to data in our warehouses, schemas, feeds and documents. If you are unsure what class applies to a piece of data, ask the data owner (listed in the system's entry in the back office or the analytics warehouse catalogue).

## The four classes

| Class | Definition | Examples from our systems |
|---|---|---|
| **Public** | Information that is already published or written for publication. | Marketing collateral approved for external release, the public status page (status.kilbarrapay.com), job postings, the company overview in the handbook. |
| **Internal** | Information meant for Kilbarra employees and contractors. | Internal org charts, most runbooks and internal documentation, expense policy, office procedures, internal tooling names and how they fit together. |
| **Confidential** | Information that could harm Kilbarra or its merchants if disclosed outside the company. Access is on a need-to-know basis. | Transaction records (individual transactions, volumes, values), merchant risk ratings, chargeback and fraud data, partner fee schedules, pricing and plan details, internal certificate and key inventory, SIEM rule content. |
| **Restricted** | Information whose disclosure could cause serious harm to individuals or to Kilbarra's regulatory standing. Access is limited to named individuals or specific roles, and handling is controlled. | Card numbers (PANs) — only the card vault holds these; cardholder data is never stored outside the vault. Merchant bank account details and settlement instructions. KYB documents and due-diligence files. Employee records, payroll data, disciplinary records. Data subject request files. |

## Assigning a class

The **data owner** assigns the class. For merchant data, the data owner is the team that owns the source system — for example, Merchant payments owns transaction records, Integrations & partners owns partner feed data, and Financial crime owns KYB documents. For internal data, the owning team is listed in the system catalogue in the analytics warehouse.

When a new dataset, table, feed or document is created, the owning team assigns a class at creation time and records it in the warehouse catalogue. If you inherit a dataset and the class is not recorded, treat it as **Restricted** until the owner confirms otherwise.

## Labelling data

### In the analytics warehouse

Every table and column in the analytics warehouse carries a `data_class` attribute. Set it when the table is created. The warehouse's access controls rely on these labels, so a missing label means the table is not queryable by anyone outside the owning team until it is added.

For columns that are more sensitive than the table's default, set the column-level label. For example, a table holding transaction records is **Confidential** by default, but the column holding the merchant's settlement IBAN is **Restricted**.

### In schemas and APIs

Schema definitions and API specifications should include a `data_class` field on each property. The merchant API team and the Integrations & partners team follow this convention for all new endpoints. Existing schemas are being backfilled as they are touched.

### In documents and files

Documents in the company's document repositories should state the class in the header or metadata block if they contain anything beyond **Public**. Files in shared drives and wikis that contain **Confidential** or **Restricted** data must be stored in the access-controlled locations, not in open team folders.

## Changing a class

Only the data owner may change a class. To request a change, raise a ticket in `tickets` with the dataset or document path, the current class, the proposed class and the business reason. The owning team reviews the request. If the change is from **Restricted** to a lower class, Security engineering reviews it as part of the ticket.

A class change applies from the date the ticket is closed; the catalogue keeps the history of earlier classes.

## Common questions

- **Where does pricing sit?** Pricing, plan fees and partner fee schedules are **Confidential**. The list prices published on the website are **Public**.
- **What about merchant names and contact details?** Merchant names, contact details and the fact that a company is a Kilbarra merchant are **Confidential** when they appear in transaction, risk or KYB contexts. The merchant's own dashboard shows them to the merchant, but internal documents should treat them as **Confidential** unless the context is clearly **Internal** (for example, a list of merchants in a merchant-success coverage plan).
- **Aggregated data.** Aggregations that could be reverse-engineered to individual merchants (for example, a breakdown by merchant segment with very few merchants in a cell) remain **Confidential**. Fully aggregated figures with no re-identification risk, like total monthly processed volume, are **Internal** unless the data owner says otherwise.
- **Logs and monitoring data.** Logs that contain transaction references, IP addresses or account identifiers are **Confidential**. Logs that could contain cardholder data are treated as **Restricted** — if you are unsure whether a log source can contain PANs, check the log-sources documentation in `security-docs/soc/` before storing the data.

## References

- Warehouse catalogue and table metadata: analytics warehouse
- Access request process: `handbook/it/access-requests.md`
- Records retention periods: `handbook/legal/records-retention.md`
