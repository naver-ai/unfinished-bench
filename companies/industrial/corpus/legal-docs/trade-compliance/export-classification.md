# Export classification

**Owner:** Trade compliance (export control)  
**Last edited by:** Stella Yilmaz, Export Control Specialist

## Purpose

This document describes how Kessendorf products are classified against the dual-use export control lists (EU Annex I, UK Strategic Export Control Lists, US EAR). It covers who performs classifications, where results are stored, and typical outcomes for our main product families.

## Classification process

New product classifications are owned by Trade compliance (export control). The request typically comes from Engineering via the PLM at the point a new item number is proposed, or from Sales when a customer asks for a classification statement before placing an order.

Classification results are recorded in the ERP item master against each sales item. The relevant fields are:

| Field | Content |
|---|---|
| `ECCN` | US Export Control Classification Number (for US-origin content / re-export considerations) |
| `EU Annex I` | Entry number, e.g. 3A225 or 3A002 |
| `UK List` | Corresponding UK strategic list entry |
| `Status` | `Classified`, `Pending`, `Not controlled` |
| `Classified by` | Initials of the trade compliance team member |
| `Review date` | Rolling review date (usually 3 years from classification) |

Firmware releases are classified separately from hardware. The release engineering team notifies Trade compliance (export control) when a new firmware version is tagged for general availability; the classification is recorded in the PLM against the release record, not in the ERP item master. Most firmware releases fall under the same entry as their host controller, but this must be confirmed each time — encryption functionality in a release can change the outcome.

## Typical results by product family

| Product family | Typical EU/UK entry | Typical US ECCN | Notes |
|---|---|---|---|
| MC series motion controllers | 3A225 (or 3A002 if high-speed ADCs present) | 3A225 / 3A002 | Depends on ADC resolution and sample rate; check the item master for the specific variant |
| DU series servo drives / direct-drive units | 3A225 | 3A225 | Standard drives are 3A225; units with integrated position feedback above 5 nm resolution may be 3A002 |
| TX series torque transducers | Not controlled (3A999 in some configurations) | EAR99 | Transducers themselves are not on the lists; check the signal conditioning electronics |
| Laser encoders | 3A002 (resolution-dependent) | 3A002 | Encoders with interpolation above a certain factor fall under 3A002 — check the datasheet revision |

## Notes on interpretation

- The EU and UK lists are aligned but not identical. For shipments from Telford we classify against the UK list; for shipments from Reutlingen or Greenville, the EU or US lists apply respectively. Where a product is classified differently across jurisdictions, the strictest applicable entry is used for the ERP record and the difference is noted in the item master text field.
- Packing lists and commercial invoices generated from the ERP pick up the classification automatically. If a field is blank, ask in `#trade-compliance` for the status.
- The trade compliance team reviews the lists on a rolling basis. When a list amendment affects an existing classification, the affected items are flagged in the ERP and the team re-classifies before the amendment's effective date.
- For retrofits and upgrades: a retrofit kit that changes the performance characteristics of an existing machine (e.g. encoder upgrade) gets its own item number and classification. Field service does not need to re-classify the machine itself unless the upgrade crosses a control threshold — in that case the service report notes the change and Trade compliance issues an updated statement for the customer.

## Contacts

Questions on classification go to Trade compliance (export control) via `#trade-compliance`. Ruth Adler and Stella Yilmaz handle the majority of item classifications; Samir Karimi covers firmware release classification and list amendment reviews.
