# Claims document ingest and OCR

**Owner:** Records platform  
**Last edited by:** Olivier Harper (Records Analyst)

## What this covers

How claim-related documents arrive in the Records platform, how they get OCR'd and indexed to the right claim, and how monthly claim bundles are sealed and loaded. Also covers reprocessing a failed batch.

## Document sources

Claims documents come in through three main paths:

1. **Clearinghouse attachments** — EDI 275 attachments from clearinghouses land in the interface engine and get pushed to the records ingest queue. These are mostly referral authorizations, progress notes, and other supporting docs that come attached to claims.
2. **Mailroom scans** — South Bend and Valparaiso mailrooms scan paper claims and supporting documents at the mailroom scan stations, which push to the ingest queue. Kalamazoo mailroom scans go through the same path.
3. **Member portal uploads** — Members can attach documents to a claim inquiry through the member portal. These go through the portal's file validation (size, type) and then land in the same ingest queue.

All three paths end up in the same queue in the Records platform. There is no separate queue per source.

## OCR workers

OCR runs on a worker pool in the Records platform. Workers pick up documents from the ingest queue, run OCR, and write the extracted text back to the document record. The extracted text is used for search and for auto-indexing.

- Workers run in the Kalamazoo data centre, on the same hosts as the archive bucket services.
- OCR output is stored alongside the document in the archive bucket — we do not keep a separate OCR store.
- If OCR fails, the document stays in the queue and the failure is logged. The document is still visible in the archive but won't appear in text search until OCR succeeds.

## Indexing to the claim

After OCR, the document is indexed to a claim. Indexing uses:

- The claim number from the clearinghouse attachment envelope, if present.
- The member ID and date of service from the OCR text, matched against the claims adjudication system.
- For mailroom scans, the barcode cover sheet that the mailroom prints and attaches — still to confirm: confirm whether the cover sheet barcode is being read reliably for Kalamazoo scans. There was a coversheet template change a while back and I don't think we ever verified the barcode format still matches what the indexer expects.

If indexing can't find a match, the document goes to a review queue in the Records platform. Records Analysts work that queue. Documents that sit in the review queue for more than a few working days get flagged — still to confirm: decide what the escalation path is and whether the claims team should be notified automatically or if it's still manual.

## Monthly claim bundles

At month end, the Records platform runs a job that:

1. Collects all claim documents ingested during the calendar month (based on ingest timestamp, not date of service).
2. Seals the bundle — documents in a sealed bundle cannot be modified or re-OCR'd.
3. Loads the bundle into the long-term archive bucket. Sealed bundles are stored by month and by source (clearinghouse, mailroom, portal).

The bundle job runs automatically on the first working day of the following month. The job ran fine for the last few months but the load into the archive bucket has been slow — Tariq is looking at whether month-end ingest and the bundle load are competing for the same workers.

## Reprocessing a failed batch

If a batch fails (for example the ingest queue backs up or the OCR worker pool goes down), the batch stays in the queue with a failed status. To reprocess:

1. Go to the Records platform admin view, find the batch, and select "Retry".
2. Retry re-queues the documents. Documents that already got OCR'd are skipped — only the failed ones get re-picked.
3. If the whole batch is stuck, delete the batch from the queue and re-run the ingest from the source. For clearinghouse attachments that means asking the interface team to replay the feed. For mailroom scans, the scans are still on the scan station share so we can re-forward them.

Still open: figure out whether retry and re-forward handle duplicates correctly. I think there's a dedup check on the document hash but I'm not sure it catches everything when a batch is partially processed.

## Open question

Do we want to add a fourth source for provider portal uploads? Providers keep asking whether they can attach documents to a claim through the provider portal. The portal team says the capability is there but not wired to the Records platform. Worth discussing with claims ops whether that's something we want to take on this year or leave for later.

## Related docs

- it-docs/records-platform/archive-buckets.md
- it-docs/clinical-systems/chart-archive.md
- plan-docs/claims/adjudication-basics.md
