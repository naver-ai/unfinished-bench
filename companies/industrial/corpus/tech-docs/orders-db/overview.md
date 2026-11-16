# Orders database

**Owner:** Order management systems  
**Last edited by:** Jonas Kaplan (Backend Engineer)

## What the database holds

The orders database is the operational store for everything that happens between a customer placing an order and the goods leaving the dock. It holds:

- **Customers** — ship-to and bill-to records, including the customer master data that the ERP interface keeps in sync with the ERP item master.
- **Orders** — header-level data (customer reference, currency, incoterms, requested delivery date) plus status history.
- **Order lines** — the line items with part numbers, quantities, agreed prices, and line-level status.
- **Deliveries** — outbound shipments, including partial deliveries and the connection to the outbound dock releases in the MES.

It does **not** hold pricing rules or discount structures — those live in the CPQ tool and the ERP. The orders database stores the agreed price at the time the order was booked.

## Services that read and write

| Service | Direction | Notes |
|---|---|---|
| ERP interface | Writes orders, order lines, customer master | The interface service pushes new and changed orders into the orders database. It also writes back delivery confirmations from the ERP. |
| RMA portal | Reads orders, writes returns | The portal looks up original order lines when a customer raises a return. Return lines are written back here so shipping and planning can see them. |
| Shipping service | Reads orders, writes deliveries | Used at the Telford distribution centre and at Greenville. It reads open order lines for pick/pack and writes the delivery record once the shipment is released. |
| MES | Reads orders | Shop-floor terminals read the order lines for the Telford drives line and the DU assembly lines in Reutlingen. The MES does not write to the orders database. |
| Reporting | Reads orders | The consolidation tool and group controlling pull order data from here for the monthly figures. |

The Telford distribution centre does not keep a separate order book — all UK distribution orders are in the same database, with the site identified on the order header.

## Replicas

We run one read replica for reporting and one for the RMA portal. The replica for reporting is refreshed continuously; the RMA portal replica is allowed to lag by up to a few minutes. If the portal replica falls behind, the portal will still serve from it but will show stale order lines — the portal team knows to check the primary if a customer asks about a very recent order.

The MES reads from the primary. It is a small number of reads and the MES team prefers not to deal with replica lag on the shop floor.

## Ownership

- **Order management systems** owns the schema, the migration process, and the service accounts that connect to the database.
- **Database Engineer (Orders)** — Colm Ndlovu is the contact for schema changes, index tuning, and replica health. Most migration requests come to him via the tickets system.
- **ERP interface** is owned by the same backend team; Diego Marchetti is the usual contact for interface questions.
- **Shipping service** is owned by Business applications (Aiko Tanaka), not by Order management systems.
- **RMA portal** is owned by the quality team.

## Loose ends

- We still have a handful of legacy order lines from before the ERP interface was switched on that were never fully reconciled. Colm has a list; most are from the Telford site's first year. Plan is to clean them up during the next quiet period.
- The replica for reporting is due for a storage refresh; it moves with the other orders volumes in the nfs-a retirement waves.
- There is an open question about whether the warehouse goods-in team should get read access for return receipts. Currently they only see returns via the MES, which is fine for most cases, but the dock team in Greenville has asked for direct access twice. No decision yet — the warehouse team is welcome to raise it in the next operations review.
