# Data pipelines on-call

Owner: Data engineering · Last edited by Leila Doyle

## Scope

This covers the {{WORKFLOW_SCHEDULER}} DAGs that feed the analytics warehouse, the CRM, and the daily files sent to stores and wholesale. It does not cover the GPU lab or the recs model release pipeline — see `eng-docs/ml/`.

## Before your shift

- Read `eng-docs/oncall/oncall-guide.md` if you haven't done a rotation before.
- Make sure you're in #data-eng and #incidents.
- Check the DAG list in {{WORKFLOW_SCHEDULER}} for anything paused that shouldn't be. If unsure, ask in #data-eng.

## During the shift

1. **Check the {{WORKFLOW_SCHEDULER}} UI first thing.** Look at the last 24 hours of DAG runs. Anything in `failed` or `upstream_failed` state needs a decision, not just a rerun.
2. **For a failed DAG run:**
   1. Open the DAG, click the failed run, and look at the task logs.
   2. If it's a transient error (network blip, warehouse connection reset), clear the task and let it retry. Use the "Clear" button in the graph view.
   3. If it's a code or data issue, do not clear. Post in #data-eng with the DAG name, the failing task, and the log snippet. Tag the team.
3. **For a late-running DAG that hasn't failed yet:** check how long past its SLA it is. If it's more than 30 minutes past SLA and it feeds a store report or the wholesale price file, tell #finance-ops and #wholesale. They will tell you if the file is critical for that day.
4. **Backfills:** if someone asks for a backfill in #data-eng or via tickets, use the {{WORKFLOW_SCHEDULER}} backfill UI. Set the dates, and make sure you only rerun the tasks that are downstream of the change — don't rerun the whole DAG unless asked.
5. **Dashboard lateness:** if a dashboard in the warehouse is stale because a DAG hasn't finished, check if the DAG is still running. If it's stuck, see step 2. If the DAG finished but the warehouse refresh hasn't run, check the refresh job — it sometimes needs a manual trigger. Tell #data-eng when it's done.
6. **Store-facing files:** the daily stock file for stores goes to the POS back office. If it's late, #stores-ops will notice before you do. Tell them a revised ETA and check that the file gets picked up — there's a known issue where the store system doesn't retry after a certain time.
7. **Wholesale files:** the wholesale order feed goes out twice a day. If the morning feed is late, #wholesale will want to know before the account managers start their calls. Mention it in #wholesale and give an ETA.

## If it goes wrong

- If a rerun causes duplicates in a warehouse table, do not delete rows manually. Post in #data-eng and we'll sort out a reconciliation query.
- If a DAG is failing in a loop and generating alerts, pause it. Say so in #incidents and #data-eng.
- If you're not sure whether a failure matters, ask. Most store and wholesale files have a cut-off — missing it means the recipients work off stale data, which is worse than a delay.

## Open question

Should we add a page that lists which DAGs feed which reports and files? I started one but it's not finished — it's in data-docs/ but the owner list is still blank.

## Still to write up

- Add the runbook link for the warehouse refresh job (it's in eng-docs/data/warehouse.md but the exact section is tbc).
- Document the retry behaviour for the wholesale order feed — it was changed recently and the old notes say "retries twice" but I think it's now...
- Confirm with Finance ops whether the monthly VAT file is still on the same DAG or if it moved. It might be under a different name now.
