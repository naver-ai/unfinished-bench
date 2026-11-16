# Cash forecasting

**Owner:** Treasury  
**Last edited by:** Ibrahim Mahlaba (Treasury Analyst)

## Purpose

This note describes the rolling 13-week cash forecast: what each entity submits, by which working day, and how the consolidated view is built. It is the working reference for anyone in Treasury or Finance Ops who touches the forecast.

## Cycle and consolidation

- The forecast runs on a rolling 13-week horizon and is refreshed **every week**.
- Treasury consolidates the entity submissions into a single workbook and loads the result into the ERP's treasury module. The consolidated view is shared with the CFO and the Executive board on the same day.
- The ERP is the system of record for the consolidated forecast; entity-level working files live on the treasury share under `forecasts/` with a filename like `fc_<entity>_<week>.xlsx`.

## Entity submissions

Each entity sends its weekly input to Treasury by the following working days:

| Entity | Submitted by | Contact |
|--------|--------------|---------|
| Kessendorf GmbH (Reutlingen) | WD+1 | Treasury (Joost Bakker) |
| Kessendorf UK Ltd (Telford) | WD+1 | Treasury (Sanne Visser) |
| Kessendorf Inc. (Greenville) | WD+2 | Treasury (Ibrahim Mahlaba) |

- The German entity file also includes the Reutlingen test lab's external calibration income, which is small but volatile — we ask the lab to flag large one-off receipts a week ahead.
- The UK file includes the Telford distribution centre's outbound freight payments, which are batched by the warehouse team; Treasury does not re-estimate those.

## Bank accounts per entity

- **Reutlingen:** main EUR account (Reutlingen HQ), plus a EUR account for the test lab's calibration fees. No secondary operating accounts.
- **Telford:** GBP operating account and a GBP account for the drives plant's supplier payments. The UK entity also holds a small EUR account for intercompany purchases from Reutlingen.
- **Greenville:** USD operating account and a USD payroll account. All US customer receipts land in the operating account.

## FX exposure

- Sales from the US and UK plants create USD and GBP exposure against the EUR group base.
- Treasury tracks the net exposure from confirmed customer orders and from the forecast; the hedge decisions are made by Joost, with Margreet's sign-off above a threshold set in the treasury policy.
- For forecast purposes, the UK drives plant's output is treated as GBP revenue even when the end customer pays in EUR via the German sales entity — the intercompany settlement is what creates the actual FX movement. The UK team flags large one-off settlements in their submission.

## Intercompany cash

- Intercompany cash movements between the three entities are planned by Treasury as part of the consolidated forecast. The entities do not arrange their own intercompany funding.
- Ask Joost or Sanne about any intercompany cash question; the monthly intercompany reconciliation is handled by the Finance Ops team, but the cash timing sits with Treasury.
- The forecast assumes intercompany settlements happen on the last working day of each month unless Treasury is told otherwise by the entity's finance contact.

## Loose ends

- The Greenville submission often arrives late on WD+2; we are working with the US plant's finance team to move it to the morning.
- The test lab's income is still manually entered — Rafael's team is looking at pulling it from the calibration database, but nothing is scheduled yet.
- The Telford freight payments are paid out of the GBP operating account in one batch; if the batch is moved, the forecast needs the new date from the warehouse team.
- We do not include VAT or sales tax timing in the 13-week view; that is covered in the month-end close process.

## Questions

- Forecast content and deadlines: Ibrahim Mahlaba.
- FX and hedging: Joost Bakker.
- Intercompany cash: Joost Bakker or Sanne Visser.
