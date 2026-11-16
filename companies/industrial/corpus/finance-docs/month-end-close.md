# Month-end close

**Owner:** Group controlling  
**Last edited by:** Shreya Keller (Controller)

## Purpose

This document describes the group month-end close calendar and the steps Group controlling runs from WD-2 through WD+6. The calendar is the same for every month-end; the year-end close follows the same sequence with additional statutory audit activities described in `finance-docs/audit/year-end-audit.md`.

## Close calendar overview

All dates are working days relative to the month-end (WD0). Plants and the UK distribution centre report into the group close; the US plant follows the same calendar in local time.

| WD | Activity | Owner | System |
|----|----------|-------|--------|
| WD-2 | Cost centre accrual submissions due from department heads | All departments | ERP |
| WD-1 | Plant stock counts and WIP valuation worksheets due from Reutlingen, Telford and Greenville | Plant controlling | ERP |
| WD0 | Month-end cut-off in the ERP; no further postings to the closed period | Group controlling | ERP |
| WD+1 | Stock and WIP valuations loaded; variance analysis against prior month | Group controlling | ERP |
| WD+2 | Accrual postings completed; intercompany matching run | Group controlling | ERP |
| WD+3 | FX revaluation for non-EUR balances; intercompany differences cleared | Group controlling | ERP |
| WD+4 | Reporting package upload to the consolidation tool | Group controlling | Consolidation tool |
| WD+5 | Review of the uploaded package; adjustments from consolidation | Group controlling | Consolidation tool |
| WD+6 | Group report to the CFO | Margreet de Wit | — |

## Detailed steps

### WD-2 — Accrual submissions

Department heads submit accrual proposals for services received but not yet invoiced. The ERP accrual template is used; submissions that do not reference a purchase order or contract are returned by Group controlling. Accruals below the threshold in the ERP accrual template do not need supporting documents.

### WD-1 — Plant valuations

The three plants submit:

- **Reutlingen:** finished goods and WIP valuation from the main plant and the test lab's calibration equipment inventory (the calibration database feeds the asset side, not the stock valuation).
- **Telford:** drives line stock and WIP, plus the distribution centre inventory (UK distribution centre stock is valued separately by Pavel Jensen's team).
- **Greenville:** US plant stock and WIP in USD; the valuation is translated at the month-end rate in the ERP.

Inventory controllers sign off the worksheets in the ERP before the close cut-off.

### WD0 — Cut-off

No postings are accepted into the closed period after the cut-off. The ERP blocks the period automatically; exceptions require a reopening ticket via the tickets system and are logged with the reason.

### WD+1 — Valuations loaded

Group controlling loads the plant valuations into the ERP. Variance analysis compares the current month against the prior month for:

- stock value by plant and product family (MC, DU, TX series, encoders)
- WIP value by production line
- inventory days by plant

Variances above the threshold in the ERP parameter set are flagged for the plant controllers to explain before the close proceeds.

### WD+2 — Accruals and intercompany matching

Accrual postings are completed by mid-afternoon UK time. The intercompany matching run is executed in the ERP; it matches intercompany balances between the GmbH, Kessendorf UK Ltd and Kessendorf Inc. Unmatched items must be resolved or have a documented reason from the entity controller.

### WD+3 — FX revaluation

Non-EUR balances are revalued at the month-end rates published in the ERP. Revaluation differences are posted to the FX revaluation account. Intercompany balances that remain open after revaluation are followed up with the entity controllers.

### WD+4 — Reporting package upload

The reporting package is generated in the ERP and uploaded to the consolidation tool. The package includes:

- group income statement and balance sheet
- plant-level stock and WIP detail
- intercompany balance confirmations
- FX revaluation summary

Uploads are queued in the consolidation tool; the tool runs validation checks before accepting the package.

### WD+5 — Review and adjustments

Group controlling reviews the uploaded package in the consolidation tool. Adjustments (reclassifications, elimination entries) are posted in the tool and must be referenced to the underlying ERP posting. Daisuke Castillo reviews the intercompany eliminations.

### WD+6 — Group report to the CFO

The group report is prepared from the consolidation tool and sent to Margreet de Wit. The report covers:

- group revenue and operating result by entity
- stock and WIP by plant and product family
- intercompany balance status
- FX impact on the group result
- key variances against the budget figures in the consolidation tool

## Roles and responsibilities

| Role | Responsibility |
|------|----------------|
| Selin Gonzaga | Overall close management, sign-off of the reporting package |
| Shreya Keller | Close calendar coordination, accrual reviews, package upload |
| Daisuke Castillo | FX revaluation, intercompany eliminations, variance analysis |
| Plant controllers | Stock and WIP valuation worksheets, variance explanations |
| Margreet de Wit | Receives the group report, approves the close |

## Common issues

- Late accrual submissions from departments are the most frequent cause of WD+2 overruns. The ERP flags submissions after the WD-2 cut-off automatically.
- Intercompany differences between the UK distribution centre and the GmbH often trace to goods-in timing at Telford. The warehouse team logs goods receipts in the MES; the MES feed to the ERP runs hourly, but receipts after the WD0 cut-off land in the next period.
- FX revaluation on the USD balance for Greenville occasionally produces large differences when the month-end rate moves sharply; these are reported separately in the group report.

## Related documents

- `finance-docs/controlling/budgeting.md` — budget and forecast cycle
- `finance-docs/intercompany.md` — intercompany process details
- `finance-docs/treasury/cash-forecasting.md` — cash forecast inputs from the close
- `finance-docs/audit/year-end-audit.md` — year-end audit activities
- `ops-docs/quality/gauge-calibration.md` — calibration lab inventory (feeds WD-1 valuations)
