# Goods in

**Owner:** Logistics & distribution centre  
**Last edited by:** Pavel Jensen (Inventory Controller)

---

## Purpose

This covers receiving at the Telford DC — delivery slots, checking deliveries against the PO, booking the goods receipt in the ERP, and what to do with damaged or quarantined stock.

## Delivery slots

1. Suppliers book delivery slots through the supplier portal. The dock team confirms or rejects slots at least one working day ahead.
2. Unscheduled deliveries are accepted only if the dock has capacity — check with the shift supervisor before turning a truck away. Tomas Ortiz and the dock team keep the slot list in the shared warehouse calendar.
3. Deliveries for the Reutlingen plant do not come to Telford. If a truck arrives with Reutlingen-bound goods, do not unload — contact the planning team so they can reroute.

## Checking the delivery against the PO

1. Take the delivery note from the driver and scan the barcode into the ERP goods-receipt screen.
2. The ERP shows the open PO lines. Verify:
   - Item number and description match the PO
   - Quantity matches the delivery note and the physical count
   - Serial numbers match for DU series drives and TX series transducers (these are serial-tracked)
3. Count the physical goods before signing anything. Spot checks are not enough for partial pallets — count every unit.
4. If the delivery note references a PO that is not visible in the ERP, do not book it. Contact Procurement (Jada Zhang for UK-sourced items) before proceeding.

## Booking the goods receipt

1. In the ERP, go to **Goods Receipt → Create**.
2. Enter the PO number and the delivery note reference.
3. Confirm the quantities received (shortages go in as received quantity, not the PO quantity).
4. For serial-tracked items, scan each serial number into the receipt lines.
5. Save and post the receipt. The system creates the stock transfer to the DC location.
6. Print the goods-receipt label and attach it to the pallet or bin location.
7. If the PO is fully received, the ERP closes the line automatically. Partial receipts keep the line open.

## Damaged deliveries

1. If goods arrive damaged or the packaging shows signs of transit damage, photograph the damage before unloading.
2. Note the damage on the carrier's delivery note and have the driver sign it.
3. Book the goods in with the quantity received, then raise an NCR in the QMS with the photos attached.
4. Do not put damaged goods into stock. Move them to the quarantine area immediately.

## Quarantine area

The quarantine area is racking H-12 near the dock — labelled with red and white tape.

1. Goods go into quarantine when:
   - They are damaged (as above)
   - They are marked for incoming inspection (usually on the PO or the supplier portal note)
   - The ERP flags them as quality-hold
2. Each quarantined pallet or bin needs a quarantine label with the goods-receipt number, date, and the reason.
3. Incoming inspection is handled by Quality (the supplier quality engineers). They scan the quarantine label and record the result in the QMS.
4. Once released, the stock moves from quarantine to the picking location. The QMS update clears the hold in the ERP automatically.
5. If a quarantined pallet sits for more than five working days, chase it in #quality.

## If it goes wrong

- **Wrong goods delivered** — do not book them. Contact Procurement and return to the carrier with the delivery note marked "rejected".
- **PO not found** — hold the goods in quarantine and contact Procurement. Do not create a manual receipt without a PO reference.
- **Serial number mismatch** — do not book. Contact the supplier and the quality team before anything moves.
- **ERP booking error** — post a reversal the same day and rebook. If the reversal fails, raise a ticket to Finance Operations.
- **Driver refuses to sign for damage** — note it on the delivery note anyway and keep a copy. The carrier's refusal does not block the NCR.
