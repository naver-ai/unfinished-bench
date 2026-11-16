# VAT and customs notes for ops

Owner: Group controlling · last edited by Daisuke Castillo

## Context

Notes from the quarterly tax-operations sync, mostly around where VAT and customs sit for the operating sites. These are working notes, not the tax manual — if it contradicts something the group tax manager said, ask them.

## EU / UK VAT on sales

- **Intra-EU sales of MC and TX units from Reutlingen** to customers in other member states: zero-rated with a valid VAT number on the customer's order and the EC sales list filed via the ERP export. The ERP flags missing numbers at order entry; do not override without checking with Group controlling.
- **Sales from Reutlingen to Kessendorf UK Ltd** (Telford) and to Kessendorf Inc. (Greenville): exports, zero-rated in Germany with the export evidence from the broker; the receiving entity deals with import VAT and duty (see below).
- **UK domestic sales from Telford** (DU drives sold to UK machine builders): standard UK VAT at the UK rate. **Greenville sales** (US customers): no VAT; sales tax is handled at the US plant and is not a Group controlling topic.
- **Cross-site transfers of demo or loan units** (e.g. a TX transducer sent from Reutlingen to Telford for a customer trial): treat as a dispatch for VAT purposes, even if no invoice is raised. Raise an intercompany stock transfer in the ERP and copy Group controlling — this keeps the EC sales list right.

## Import VAT and duty on purchased parts

- **Telford** imports DU-series power components from the Reutlingen plant and from third-party suppliers in the EU. Import VAT is postponed (PVA) — the Telford finance team accounts for it on the VAT return; no cash payment at the border. Duty is paid via the customs broker, who invoices us monthly.
- **Greenville** imports finished DU drives and TX transducers from Telford and Reutlingen for US deliveries. Duty is paid at entry; the US plant's logistics team handles the entries and the amounts land in the ERP as landed cost.
- **Reutlingen** imports some sensor components from a Japanese supplier. They used to come in through the UK distribution centre; they now clear directly into Germany through the German broker, and Reutlingen deducts the import VAT on its return. A few old purchase orders still show Telford as ship-to — check before booking the receipt.

## EORI numbers

- Reutlingen (DE), Telford (GB) and Greenville (US importer number) each have their own EORI / importer reference. They are held in the supplier master data under the legal entity, not the site. If a carrier asks for one, point them to the purchasing team — do not type a number from memory into a shipment document.

## Where tax questions go

- VAT classification, EORI use, import duty queries and any customs broker questions: **group tax manager** (Finance, Reutlingen). Route via Group controlling if unsure.
- Operational questions about a specific shipment (who cleared it, what the duty amount was): Telford finance for the UK site, the Greenville plant controller for the US site, and the Reutlingen plant controller for Germany.

## Loose ends

- The UK distribution centre is still listed under "Kessendorf UK Ltd" in the ERP item master; the group tax manager wanted that revisited after the drives plant move but it has not happened yet.
- The old EC sales list extract (the one that ran via the legacy finance tool) has been retired — the ERP export is the only source now. The tax manager said they would update the intranet page on this; check with them if the page still shows the old tool.
