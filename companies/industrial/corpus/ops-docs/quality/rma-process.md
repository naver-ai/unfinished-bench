# Returns (RMA)

**Owner:** Customer service  
**Last edited by:** Bilal Bose (Order Administrator)

---

**How does a customer get an RMA number?**

Customers request a return through the RMA portal. The portal issues the RMA number immediately and sends the customer a return form with the number pre-filled. The form asks for the serial number, the product type (MC controller, DU drive, TX transducer), the purchase order or invoice number, and a short description of the fault. If the customer cannot access the portal, our team raises the RMA on their behalf.

**Who picks up an RMA request when it comes in?**

The Customer service team owns the queue. Hannah Brooks assigns incoming RMAs to the order administrators — usually Bilal or Harriet — depending on workload. The assignee checks the serial number against the ERP item master to confirm the product is ours and within its warranty window. If the unit is out of warranty, we still accept the return but the customer gets a repair-quote option instead of a free-of-charge repair.

**What happens after the RMA is logged?**

The assignee emails the customer the return label and the RMA number. The customer sends the unit to the Reutlingen test lab (for controllers and transducers) or to the Telford drives plant (for DU drives). The RMA number must be written on the outside of the box. Goods-in at both sites scans the RMA number into the MES so the unit is tracked from receipt.

**How long does the customer have to send the unit back?**

60 calendar days from the RMA issue date. After that the RMA expires and the customer has to raise a new one. We do not chase expired RMAs automatically — the assignee checks the portal list at the start of each month and sends a reminder to any customer with an expiring RMA that has not shipped yet.

**What does the test lab do with a returned controller?**

The lab books the unit in on the repair bench and runs the standard diagnostics. The technician records the fault code, the test results and the repair decision in the MES. For controllers, the usual outcomes are: repair in-house, replace with a refurbished unit, or no fault found. If no fault is found, the unit goes back to the customer with a note explaining what was tested, unless the customer asked for it to be scrapped.

**And for drives at Telford?**

Same principle, but the Telford drives line handles the diagnostics and repair. The line supervisor decides whether a drive is repairable or should be replaced. Drives that are beyond repair are stripped for usable parts and the rest goes to the scrap bin. The MES records the part recovery so the ERP stock levels for spare parts stay correct.

**Who decides between repair and replacement?**

The test lab at Reutlingen makes that call for controllers and transducers. At Telford it is the drives line supervisor. The decision is based on the repair cost compared with the unit's replacement value. If the repair would cost more than 70% of a new unit, we replace it. That threshold is in the MES as a guideline but the lab technician can override it with a note in the RMA record.

**What does the customer receive after the return is processed?**

A return confirmation email with the outcome (repaired, replaced, or no fault found) and the RMA record number. If the unit was under warranty and repaired or replaced, there is no charge. If it was out of warranty and the customer accepted the repair quote, the invoice goes out through the normal ERP billing process. If the customer decides not to accept the quote, the unit is returned unrepaired and the customer pays the return freight.

**When does the customer get a credit note?**

When the customer returns a unit that was delivered in the current fiscal year and the fault is covered under warranty, we issue a credit note for the original invoice value. Credit notes are raised in the ERP by the Customer service assignee and approved by Hannah. If the unit was returned because of a shipping error on our side (wrong model, wrong variant), the credit note covers the freight as well.

**How does RMA data feed into quality?**

The MES pushes RMA records to the QMS once a month. The quality team reviews the fault codes and looks for patterns — for example, a particular drive model with the same encoder fault, or a batch of controllers with a common firmware issue. If a pattern shows up in more than a handful of units, quality opens an 8D. The RMA portal also has a simple report view that Customer service uses to answer monthly trend questions from Ralf Dietz's team.

**Can a customer return a unit that was customised for them?**

Customised units (special firmware, non-standard connectors) go back to the same process, but the test lab flags them so the engineering team can confirm the fault is not in the custom part. The lab may need to contact the firmware team for a custom build to reproduce the issue. This adds a few days to the turnaround.

**What is the target turnaround time?**

From the moment the unit arrives at the site (scanned into the MES) to the moment the return decision is recorded, the target is ten working days. If the lab is waiting on a spare part or on the firmware team, the assignee updates the RMA record with the reason and the customer is informed. The portal shows the current status so customers can track it themselves.

**What if the customer sends the wrong unit or the unit is damaged in transit?**

If the serial number on the unit does not match the RMA, the site logs it in the MES as a mismatched return and the assignee contacts the customer. If the unit arrived damaged and the packaging looks intact, the lab takes photos and attaches them to the RMA record; the assignee passes that to the freight company claim process. The customer can still proceed with the return if they want, but the damage may affect the warranty assessment.

**Who can look up an old RMA?**

Anyone in Customer service can search the RMA portal by customer name, RMA number or serial number. The quality team has read-only access for trend analysis. Outside those teams, access is granted through the usual access request process — the portal is listed in the access catalogue under "RMA portal".
