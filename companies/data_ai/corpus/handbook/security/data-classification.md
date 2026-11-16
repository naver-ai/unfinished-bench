# Data classification

**Owner:** Cloud security  
**Last edited by:** Sara Olsen (Security Engineer)

This document defines the four data classes used across Brakwater and the controls that apply to each. If you are unsure which class applies to a piece of data, start with the most restrictive class that could reasonably apply and ask the data owner via #data-governance.

## Classes at a glance

| Class | Description | Examples |
|---|---|---|
| **Public** | Data we intentionally make available to anyone outside Brakwater | Datasets published on the open data hub, marketing materials, the status page, the imagery catalogue previews |
| **Internal** | Everyday working data with no particular sensitivity | Internal runbooks, most warehouse tables, the sensor site registry, non-confidential chat messages, internal dashboards |
| **Confidential** | Data that could harm Brakwater or our customers if disclosed | Customer AOIs and order history, sensor readings from customer sites, model weights, customer API keys, the customer API console configuration |
| **Restricted** | Data whose disclosure would cause serious harm or legal exposure | Employee records (HR system), payroll data, incident post-mortems with personal data, credentials for production systems |

## Storage and handling by class

| Class | Where it may be stored | Encryption | Data catalogue labelling |
|---|---|---|---|
| **Public** | The open data hub, the imagery catalogue, the status page, the website | Encryption at rest as provided by the platform; no additional requirement | Tagged `class:public` in the data catalogue |
| **Internal** | Any Brakwater system: the warehouse, batch cluster, notebook server, internal docs repositories, chat | Encryption at rest as provided by the platform | Tagged `class:internal` in the data catalogue |
| **Confidential** | Approved cloud projects (see platform-docs/cloud/accounts-and-projects.md), the warehouse, the modelhub, the tasking portal, the field app | Encryption at rest enforced by project policy; encryption in transit for any external transfer | Tagged `class:confidential` in the data catalogue; access requests go through data-docs/governance/data-access.md |
| **Restricted** | HR system, payroll files in approved storage, the password manager | Encryption at rest enforced by project policy; encryption in transit required; no exports to personal devices | Tagged `class:restricted` in the data catalogue; access is granted per-person by the owning team |

## Notes on specific data

- **Customer AOIs and order history** are confidential. This includes AOI polygons stored in the tasking portal, the imagery catalogue, and any derived tables in the warehouse. Order history in the CRM and billing records in finance systems are also confidential.
- **Customer API keys** are confidential and are treated as secrets under platform-docs/security/secrets.md. They are issued through the customer API console and must not appear in logs, support case records, or chat.
- **Sensor readings** from customer sites are confidential. This applies whether the readings are stored in the warehouse, in batch scratch, or in notebooks. Aggregated statistics that do not identify a customer site may be internal, but check with the data owner in #sensor-network first.
- **Employee records** are restricted. This includes HR system data, payroll data, and any performance or leave information. The People team is the data owner.
- **Model weights** are confidential. This includes run directories on the training cluster scratch, the modelhub, and copies staged for serving.
- **Published open datasets** in opendata are public by definition. Open data releases are covered in data-docs/governance/open-data.md.

## Handling rules

- All data in the warehouse must be tagged with a class in the data catalogue. New tables without a class tag are treated as restricted until the owning team assigns one.
- Confidential and restricted data must not be copied to personal devices, personal cloud storage, or unapproved notebooks.
- Partner deliveries are covered in data-docs/customers/partner-delivery.md.
- Screenshots or excerpts of internal dashboards that contain confidential data must not be shared externally, including in support cases that are visible to customers.
- If you see data that appears to be misclassified, raise it in #data-governance rather than reclassifying it yourself.

## Questions

For classification questions, ask in #data-governance. For storage or encryption questions, ask in #cloud-platform or #security. For access requests, use data-docs/governance/data-access.md.
