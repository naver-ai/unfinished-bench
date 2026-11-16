# MRP and the planning cycle

**Owner:** Production planning  
**Last edited by:** Marco Blanco (Head of Production Planning)

## Purpose

This document describes the weekly MRP cycle used across the Reutlingen, Telford and Greenville plants, the planning horizons and the frozen zone, and how shortages and sales order changes are handled. It is aimed at planners, buyers, and anyone who receives MRP output.

## The weekly MRP run

The MRP run executes in the ERP every working day, but the *planning* cycle is weekly. The main run happens on the first working day of the week, before the plant shifts start. A second, lighter run happens mid-week and only picks up urgent changes — new sales orders with a requested date inside the next two working days, and material movements that have created a negative on-hand balance.

The weekly run covers all items with a planning flag, which includes:

- All manufactured parts (motion controllers, drives, direct-drive units, torque transducers, laser encoders)
- All purchased parts and raw materials
- Sub-assemblies that are stocked rather than made-to-order

Service parts are planned on a separate monthly cycle and are not part of the weekly MRP output. If you need a service part expedited, raise that through the RMA portal or contact the service desk.

## Planning horizons and the frozen zone

The planning horizon is 26 weeks. The first two weeks of the horizon are the **frozen zone**. Within the frozen zone, planned order dates and quantities are not changed by the MRP run itself. If a change is needed inside the frozen zone, it has to be done manually by a planner, and it should be flagged in the ERP so that purchasing and the plants can see the change was deliberate.

The frozen zone exists because the plants have already committed labour and machine time, and suppliers have already received purchase orders or firm schedules. Changing a date or quantity inside the frozen zone without telling anyone causes missed deliveries and idle lines.

Shortages that appear inside the frozen zone are handled through the shortage list (see below), not by letting MRP re-plan the orders.

## Shortage lists

After each weekly MRP run, the planning team in each plant reviews the exception messages and produces a shortage list. The shortage list is a report from the ERP (it is not the same as the MES exception screen) that shows:

- Items where the available quantity is negative or projected to go negative
- The demand source (sales order, forecast, or dependent demand)
- The earliest date the shortage hits
- The quantities already on order and the expected receipt dates

The shortage list is reviewed in a short meeting with purchasing on the second working day of the week. The Reutlingen meeting covers the German plant and the Telford drives plant; the Greenville meeting covers the US plant. Owen Maddox joins the Greenville meeting when the shortage is on a part sourced from a supplier in the Americas.

Items on the shortage list that are inside the frozen zone are expedited with the supplier directly. The buyer raises the expedite request through the supplier portal so there is a record, and the supplier confirms a new date. If the supplier cannot meet the date, the planner decides whether to split the order or re-source, and the plant manager is told if the line could stop.

## Expediting with purchasing

Purchasing runs expediting from the shortage list. They do not expedite from the MES queue — the MES shows what is happening on the shop floor, not what is missing for a customer order.

Expediting is done by the buyer who owns the supplier. Each plant has its own buyers in Group purchasing or, for Telford, Procurement (UK). If you need something expedited and you do not know which buyer owns the supplier, ask in #purchasing and someone will point you to the right person.

For parts that are on a call-off schedule with a supplier, the expedite is done by changing the schedule in the supplier portal. For one-off purchase orders, the buyer sends a confirmation through the portal and follows up by phone if the date is critical.

## Sales order changes and how they reach the plants

Sales order changes come into the ERP from the sales teams. When a customer moves a date or changes a quantity, the sales order is updated in the ERP and the MRP run picks up the change on the next daily run. If the change is inside the frozen zone, the planner sees the exception and decides whether to adjust the plan manually.

If a customer change arrives by phone or email to a plant directly — which happens, especially with test rig builders who order through the Telford office — the person taking the call must make sure the sales order is updated in the ERP before the end of the working day. The plant cannot plan against a verbal change; it has to be in the ERP.

Changes that affect the Telford drives line or the Greenville plant are visible to those plants through the ERP. There is no separate sales order notification to the plants — the ERP is the single source of truth. If you see a sales order change that looks wrong (a date that has moved by more than four weeks, or a quantity that has dropped to zero), raise it with the customer-orders team in #customer-orders before planning against it.

## Related documents

- `tech-docs/orders-db/overview.md` — how the orders database feeds the ERP
- `finance-docs/procurement/po-release.md` — how purchase orders are released to the supplier portal

If you have questions about the MRP cycle, post in #planning or come to the shortage review meeting on the second working day of the week.
