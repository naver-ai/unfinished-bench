# Pipelines on-call

**Owner:** Data engineering  
**Last edited by:** Tariq Nakamura

This page covers what to do when the workflow scheduler shows a failed DAG run, when you need to rerun or backfill something, and who to tell when downstream consumers are waiting on data.

## First things

1. Check the workflow scheduler UI for the failed run. The DAG list shows the last run state per DAG — start there, not in the logs.
2. Open the failed run's log (the scheduler UI links to the log from the run page). Look for the first error, not the last line of the stack trace.
3. Decide whether the failure is in the **imagery ingest DAG** or a **warehouse DAG**. They have different owners and different blast radii.

## Imagery ingest DAG failures

The ingest DAG pulls new scenes from the imagery catalogue into the archive and updates the STAC metadata. Failures here usually mean a source feed is slow or a conversion step hit a malformed scene.

4. Check the imagery acquisition status page (linked from the DAG's run page) to see if the source feed itself is behind. If it is, the DAG will usually catch up on the next run — no action needed.
5. If the failure is in a conversion or metadata step, rerun the failed task only, not the whole DAG. The DAG supports single-task reruns from the run page.
6. If the same task keeps failing, save the scene ID from the logs and ping #imagery-ops — Ana Asante's team can tell you whether the scene is worth keeping or should be dropped from the ingest.

## Warehouse DAG failures

Warehouse DAGs are the ones that build tables in the analytics warehouse. Failures here are usually SQL errors or upstream data quality issues.

7. Read the error message from the warehouse connector. Most failures are a single query failing — rerun that task from the run page.
8. If the error mentions a missing column or table, check whether the upstream DAG actually finished. Look at the dependency graph on the run page — if upstream is still running, wait for it and then rerun.
9. If the error is a SQL syntax issue, do **not** edit the DAG definition yourself. Ping #data-eng and describe the error. (tbc: the naming convention for warehouse DAGs, so people can tell which team owns which.)
10. For backfills, use the scheduler's backfill option from the DAG page. Set the backfill window to the affected dates only — don't guess at a wider range.
11. After a successful rerun or backfill, check the warehouse table's row count and freshness in the data catalogue. If the numbers look wrong, (tbc — Mei was going to write the exact thresholds we use here).

## Who to tell when a dashboard is late

12. If a dashboard hasn't updated on time and the cause is a warehouse DAG failure, post in #bi with the DAG name, the run ID, and the expected recovery time. Don't wait for someone to ask.
13. If the dashboard is customer-facing (anything under the customer analytics namespace), also tell #support. Elif has asked that Sales gets a heads-up for any customer-impacting delay — if in doubt, post in #sales too.
14. For internal dashboards, #bi is enough. The BI team can usually work around a few hours of delay.

## If it goes wrong

- If a rerun makes things worse (for example, the table now has duplicate rows), stop the DAG and get help in #data-eng. Don't try to "fix" the table with manual SQL — that's how we end up with divergent data.
- If the failure looks like it affects multiple DAGs at once, check #data-platform for a warehouse-side problem before rerunning anything.
- If the scheduler itself is unreachable, that's an infrastructure issue — follow the on-call guide in `platform-docs/oncall/oncall-guide.md`.

## Open question

We still haven't decided whether imagery ingest DAG failures should page anyone outside of working hours. Right now they only page the on-call, but a bad source feed can mean a gap in the archive that's expensive to fill later. Worth raising with Joanna Kowalski and Ana Asante — maybe at the next data engineering sync.
