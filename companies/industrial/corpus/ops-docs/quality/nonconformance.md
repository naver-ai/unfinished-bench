# Nonconformance and 8D

**Owner:** Quality  
**Last edited by:** Kenji Farah (Supplier Quality Engineer)

---

## Purpose

This document describes how we handle nonconforming product and process deviations across Kessendorf sites — Reutlingen, Telford and Greenville. It covers raising an NCR in the QMS, containment, the MRB (Material Review Board) meeting, 8D reports for customer complaints, and supplier NCRs including chargebacks.

If you are unsure whether something counts as a nonconformance, raise it anyway. It is easier to close an NCR as "no action needed" than to reconstruct the facts weeks later.

---

## Raising an NCR in the QMS

1. Log in to the QMS and open **Nonconformance → New NCR**.
2. Select the **site** where the nonconformance was found (Reutlingen, Telford or Greenville). If it was found at a customer site by Field Service, select the site that owns the product line.
3. Fill in the **mandatory fields**:
   - **Product / part number** — use the item master number from the ERP, not the customer's drawing number.
   - **Lot / batch / serial** — if the unit has a serial number (motion controllers, drives, transducer), record it. For bulk parts, put the lot reference.
   - **Process step** where the issue was found (goods in, assembly, test, calibration, packing, field).
   - **Description** — what is wrong, how many pieces affected, what the acceptance criteria said.
4. Attach photos, test data or the calibration certificate that failed. If the file is too large, put it on the quality file share and note the path in the NCR.
5. Save. The NCR number is auto-generated in the sequence **NCR-YYYY-XXXX** (site prefix is added automatically by the QMS based on your login).
6. The QMS notifies the Quality team for the site automatically. Do not email the Quality team separately unless the issue is time-critical.

**Priority** — the QMS gives you three options:

- **Low** — cosmetic, no functional impact, can be dispositioned at the next MRB.
- **Normal** — default for most NCRs.
- **High** — product cannot be shipped, customer line is down, or there is a safety concern. High-priority NCRs notify the site Quality Manager by text message from the QMS.

---

## Containment actions

Containment must start before the MRB meets. The person raising the NCR is responsible for initial containment, with help from the line supervisor or warehouse manager.

1. **Stop shipment** of the affected stock. In the ERP, place the stock on block in the item master for the affected lot(s). The warehouse uses this block to prevent picking.
2. **Quarantine** the physical material. Use the red quarantine area at the site and attach the QMS-generated quarantine label. Do not leave material on the line "just for now".
3. **Check other lots / serial ranges.** If the failure mode could affect other batches, ask the planner to check the ERP for what is in stock and in WIP. Extend the block if needed.
4. **Notify** the relevant people through the chat channel for the site (#reutlingen, #telford, #greenville). Mention the NCR number and the block.
5. If products already shipped to customers, work with Customer Service (Hannah Brooks's team) to decide whether a customer notification is needed. Field Service can help assess the installed base.

Containment is not closed until the MRB confirms the block is complete or the affected material is dispositioned.

---

## MRB meeting

The MRB meets **twice a week** at each site, usually mid-morning. The site Quality team chairs the meeting. Attendees are Quality, Production/Manufacturing Engineering, Planning, and the warehouse lead for material-related NCRs. Reutlingen MRB also includes the test lab representative when the NCR involves test equipment or calibration.

Agenda is always the same:

1. Review open NCRs older than the last meeting.
2. Confirm containment is still in place (spot-check blocks in the ERP).
3. Decide the **disposition** for each NCR:

   | Disposition | When |
   |---|---|
   | **Use as-is** | Deviation is acceptable for the customer application. Requires Engineering sign-off and a note on the NCR. |
   | **Rework** | Material can be brought back to spec. The rework step must be written on the NCR. |
   | **Scrap** | Material cannot be recovered. |
   | **Return to supplier** | For supplier-caused issues; see below. |

4. Assign an owner for the disposition and a due date. The default is **five working days**, unless the MRB agrees otherwise.

Minutes are not circulated. The NCR record in the QMS is the record of the decision — update the disposition field and add the reasoning as a comment.

---

## 8D reports for customer complaints

When a customer complaint is received (via the RMA portal or directly to Customer Service), the Quality team opens a **complaint record** in the QMS and links it to the RMA. If the complaint involves a nonconforming product, an 8D report is required.

**D1–D3 (containment)** — same as the NCR containment above, but with the customer's specific requirements. The complaint record holds the containment actions and the customer communication log.

**D4 (root cause)** — the 8D owner (usually the site Quality engineer for the product line) runs the analysis. Use the 5-why template in the QMS. If the root cause is in firmware, involve the control firmware team (Henrik Andersen or Zoe Madsen) and check the firmware repo for related fixes.

**D5–D6 (corrective actions)** — actions must be specific enough that someone who is not on the team can verify them. "Retrain operator" is not acceptable. Write what training, who gives it, and how it is checked.

**D7 (preventive actions)** — update control plans, inspection sheets, or the firmware coding standard as needed. Link the change in the PLM or the firmware repo to the 8D.

**D8 (closure)** — the 8D is closed by the site Quality Manager, not by the 8D owner. Customer sign-off is required for complaints that went through the RMA portal.

8D reports for customer complaints are due **per the customer's request**, but internally we target 20 working days from complaint registration. If the target cannot be met, say so early in the complaint record — do not let it go silent.

---

## Supplier NCRs and chargebacks

If the incoming inspection or production identifies a nonconformance caused by a supplier, the NCR is assigned to Kenji Farah's team (Supplier Quality) for disposition through the MRB.

1. The MRB disposition is **Return to supplier** for material that is not reworkable in-house, or **Use as-is / Rework with supplier credit** if we accept the material.
2. Supplier Quality creates a **supplier NCR** linked to the internal NCR in the QMS. Supplier NCRs have their own numbering (SNCR-YYYY-XXXX).
3. The supplier is notified through the supplier portal. The notification includes the NCR number, the part number, the lot, and the failure description. Photos are attached from the QMS.
4. The supplier must respond with their own corrective action within **10 working days** unless the supplier portal states otherwise.
5. **Chargeback** — if the supplier NCR is confirmed as supplier-caused and we incur costs (inspection, rework, freight, line downtime), Supplier Quality raises a credit request in the ERP against the supplier's account. Attach the cost summary to the SNCR.
   - Credit requests under a defined threshold go through the normal AP process.
   - Larger chargebacks are reviewed by the purchasing team before release, and the supplier is informed through the supplier portal.
6. The SNCR is closed when the supplier's corrective action is verified. Verification is a physical check of the next delivery — do not close on the supplier's word alone.

If the same supplier part fails **three times** within a rolling quarter, Supplier Quality escalates to a supplier audit. That triggers a separate process outside this document.

---

## If it goes wrong

- **Containment was missed and material shipped.** Do not hide it. Contact the site Quality Manager immediately and work with Customer Service on recall or field modification. The 8D for this will be uncomfortable, but the cover-up is worse.
- **MRB cannot reach a disposition.** Escalate to Alana Yamamoto (Head of Quality) before the meeting ends. Do not leave the NCR hanging.
- **The QMS is down.** Use the physical NCR form at the site and enter it into the QMS once the system is back. The form number is the NCR number until the QMS assigns one.
- **A supplier disputes the chargeback.** Keep the evidence in the SNCR. Supplier Quality mediates. If the dispute is not resolved, the purchasing team decides.
- **You raised an NCR by mistake.** Do not delete it. Add a comment "raised in error, no nonconformance found" and set the disposition to No action. Deleting NCRs is not possible in the QMS and that is deliberate.

---

## Related documents

- ops-docs/quality/rma-process.md — customer returns and the RMA portal
- ops-docs/quality/gauge-calibration.md — calibration failures and their NCR path
- ops-docs/plants/maintenance-requests.md — equipment-related nonconformances
- ops-docs/warehouse/goods-in.md — incoming inspection and supplier material hold
