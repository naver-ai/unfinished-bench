# Export paperwork

**Owner:** Trade compliance (export control)  
**Last edited by:** Samir Karimi (Trade Compliance Analyst)

---

## Commercial invoice

- Use the standard commercial invoice template from the intranet (under Sales → Export documents).
- Invoice must show: seller, buyer, consignee (if different), item descriptions, harmonised codes, quantities, unit prices, total value, currency, Incoterm, and country of origin per item.
- For DU-series drives shipped from Telford, the invoice must reference the UK plant as seller. For TX-series transducers and MC controllers from Reutlingen, the German entity is the seller. Greenville handles all US domestic and Canada shipments.
- Value in EUR for Reutlingen invoices, GBP for Telford, USD for Greenville. Add the other two currencies only when the customer asks.
- Attach the signed commercial invoice to the shipment record in the ERP; the dock prints it with the packing list.

## Packing list

- Packing list must match the invoice line for line. If a line is split across boxes, say so on the packing list.
- Include gross and net weight per box and total, plus dimensions.
- Mark the packing list with the RMA number when the shipment is a return (see the RMA portal).

## EORI and customs declarations

- German EORI is used for all Reutlingen exports. UK EORI for Telford. The US entity uses its {{TAX_AUTHORITY_3|code}} number on the AES filing.
- Customs declarations are filed through the broker we use per site — the ERP picks the broker from the ship-from plant. Do not override the broker field without asking Trade compliance.
- For shipments to new destinations, the ERP will block the order until the destination country is set up in the item master. The block message tells you who to contact.
- Telford shipments to the EU need the EORI of the importer on the invoice. If the customer has not given one, ask them before the shipment is booked.

## Incoterms

- Standard terms: EXW for Reutlingen, FCA for Telford, and FOB for Greenville seafreight. DAP is used only for EU deliveries from Reutlingen when the customer asks.
- Do not quote CIP or DDP without Trade compliance approval.
- The Incoterm on the invoice must match the one in the ERP order. If they differ, the order will not release.

## Certificates of origin

- Non-preferential certificates of origin are issued on request for TX-series and MC-series. The certificate is generated from the PLM BOM data and the ERP item master.
- For preferential certificates (EUR.1, ATR, or the UK-EU statement on origin), the request goes through the CPQ tool — the quote must already carry the preference claim.
- Telford can issue UK origin statements for DU-series drives if the drive content meets the rule. Check the origin matrix in the PLM before promising it to the customer.

## New destination country

- Customer service must get from sales, in writing: the destination country, the Incoterm, the end-use (industry is enough), and whether the customer is a distributor or the final user.
- Send that to Trade compliance via chat (`#trade-compliance`) before the order is entered. Export classification and licensing come first.
- For countries on the restricted list, Trade compliance will tell you the terms and the paperwork; the standard Incoterms above may not apply.
- If the customer asks for a language other than English or German on the paperwork, mention it in the request. Translation is handled by the export team in Reutlingen.
