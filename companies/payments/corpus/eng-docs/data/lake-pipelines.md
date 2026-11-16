# Data lake pipelines on-call

**Owner:** Data platform  
**Last edited by:** Shreya Bergstrom (Data Engineer)

## Purpose

This document covers the operational runbook for the data lake DAGs that load source system data into the analytics warehouse. It is for the Data platform on-call rotation. If you are on-call for the first time, read through this once before your shift starts and keep it open in a tab.

## DAG failures

1. When a DAG fails, the first place to look is the DAG run page in the analytics warehouse UI. The failure reason is usually in the first log lines of the failed task.
2. If the failure is a transient connection error (source system unavailable, network timeout), click **Retry** on the failed task. Allow one retry before digging further.
3. If the retry fails, check whether the source system is reporting an incident. Look in #incidents and the status page before paging anyone.
4. If the source system is fine, check the warehouse write path. A common cause of failures is the warehouse being out of capacity on the loading cluster. In that case, pause non-critical loads from the warehouse UI and retry.
5. If you cannot determine the cause within 15 minutes, escalate to #data-lake with a summary of what you tried. Do not silently retry more than twice.

## Reruns and backfills

1. To rerun a failed DAG run, use the **Clear** action on the DAG run and let it reschedule. This is appropriate when the failure was transient.
2. For a backfill (reprocessing a range of dates), use the DAG's backfill option in the UI and select the date range. Backfills should only cover dates that are known to be wrong or missing — never backfill an entire table "just in case".
3. Backfills that touch more than 30 days of data need a quick message to #data-lake first, so other teams know the tables may be briefly inconsistent. Wait for at least one acknowledgement before starting.
4. After a backfill completes, spot-check row counts on a couple of dates against the source system's own counts. If the numbers do not match, stop and re-examine before doing anything else.

## Late loads and who to tell

The morning loads feed finance and regulatory reporting. The finance team runs their daily processes from these loads, and the regulatory returns calendar depends on them. The morning loads must complete by **mid-morning Dublin time** at the latest.

- If a morning load is going to be late, message #finance-eng and #reg-reporting **before** the expected completion time, not after. Say which DAG is affected and your best estimate of when it will finish.
- If a load completes but the data looks wrong (row counts off, timestamps in the future, nulls where there should not be), treat it as late — tell the same channels and do not mark the DAG as successful until you have confirmed the data is sane.
- Still to add: the list of DAGs that feed the month-end close. The finance-docs/close/month-end-close.md file references them, but we still need to capture them in one place.

## If it goes wrong

1. The most common "wrong" symptom is a DAG that succeeds but produces no output rows. The warehouse will not flag this, so check row counts as part of your normal DAG review, not just on failures.
2. If a table is partially loaded (some partitions updated, others not), the safe move is to clear the affected partitions and rerun that part of the DAG. Do not try to patch rows by hand — the warehouse does not support manual inserts into managed tables.
3. If you need to re-run a DAG that writes to a table other DAGs read from, tell #data-lake and #payments-platform before you start, and again when you finish. Consumers need to know the window where the table is inconsistent.

## Open questions

- Should the on-call runbook cover the partner feed DAGs (the ones that publish extracts for partners)? Right now those are handled by RevOps, but they read from the same warehouse tables we load. If a feed fails because of our data, who owns the rerun? — Shreya

## Still to write

- Add the escalation matrix for after-hours failures (who to page, in what order).
- Confirm the row-count thresholds for "looks wrong" — the current guidance is vague.
- Write down what happens when a DAG is stuck in "running" but has not emitted anything for over an hour. There is a known issue with one of the loader workers where this happens, and the workaround is in the warehouse UI, but it is not documented here.
