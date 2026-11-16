# ADR 0004: Event-sourced ledger

**Status:** Accepted  
**Owner:** Payments platform (bus & ledger API)  
**Last edited by:** Tomas Rahman (Software Engineer, Ledger API)

---

## Context

The core ledger was originally implemented as a set of balance tables in the main payments database. Each merchant account had a row per currency holding the current balance, and every post (charge, payout, settlement, adjustment) did a read-modify-write on that row inside a transaction.

This worked while the transaction volumes were modest, but it has caused recurring problems since we started onboarding larger platforms:

- Balance rows are a contention point. Concurrent posts to the same merchant account force serialisation and we have seen lock waits surface in the payments bus consumers.
- The balance tables only record the resulting state, not the sequence of events that produced it. Reconciling a merchant’s balance to the bank settlement file means replaying the same arithmetic in the reconciliation tool, and when the two disagree it is hard to say which side is wrong.
- A failed post that was retried could leave a half-applied adjustment if the transaction boundary was not respected. We have had support cases where the merchant dashboard showed a balance that did not match the sum of the transaction list, and fixing those required manual ledger entries.

We considered patching the existing tables (adding per-account sequence numbers, moving to a queue per merchant) but the core problem is the model: balances as mutable state are not auditable in the way our regulators and the internal audit team expect. Dmitri Asante’s team has flagged this in the last two quarterly control reviews.

## Decision

The ledger will move to an event-sourced model. Every financial event — a charge, a payout, a settlement, an adjustment, a reversal — is appended to an append-only event stream. The stream is partitioned by account ID and ordered by a monotonically increasing sequence number within that partition. The current balance of an account is derived by replaying the event stream, with a snapshot table holding the balance as of a given sequence number to avoid replaying the full history on every read.

The events are written through the payments bus. The bus already provides the ordering and delivery guarantees we need for this, and the message store gives us a durable copy that survives a ledger database failure. The ledger API exposes both the current balance and the event history for an account, and the merchant dashboard and treasury workstation will read from the API rather than querying the balance tables directly.

The old balance tables stay in place for the duration of the migration but are no longer the source of truth. They are maintained by a shadow writer that applies the same posts to both the event stream and the legacy tables, so we can compare the two during the cutover period. Once the comparison has been clean for a sustained period, the legacy tables are dropped as part of the migration completion.

## Migration notes

- The migration is per-account-group, not per-currency. We move the largest platform accounts first, then the mid-tier merchants, then the long tail. The shadow writer runs for the whole population from the start so we have a comparison set for every account.
- Each account group gets a cutover date on the change calendar. The cutover is coordinated with the treasury operations team because settlement files for the affected merchants are regenerated from the event stream from that point on.
- The reconciliation tool is being updated to read from the ledger API. Until that lands, the treasury team will keep using the existing reconciliation flow against the legacy tables.
- The analytics warehouse ingestion will be repointed from the balance tables to the event stream. That work is tracked in the data products team’s backlog and is not a blocker for the ledger cutover.

## Consequences

- Balance reads become cheaper and do not contend with writes, because the snapshot is updated asynchronously from the event stream rather than in the same transaction as the post.
- The event stream becomes the audit trail. The internal audit team can trace any balance back to the individual events that produced it without needing the reconciliation tool.
- The payments bus message store now holds a copy of every ledger event, which means the retention policy for that store needs to match the ledger retention requirement. That is a follow-up for the payments platform team.
- The chargeback monitoring and transaction monitoring systems consume events from the bus already, so they will see the same events the ledger does. No change needed there.
- The risk controls team’s existing reports that query the balance tables will break when those tables are dropped. The reporting queries need to be migrated to the ledger API before that happens. Adaeze Okonkwo’s team has offered to help with the warehouse side of that.

## Loose ends

- The snapshot table rebuild procedure is documented in the on-call guide, but the automated rebuild job is not yet wired into the paging tool. Until it is, a snapshot corruption means a manual replay and a longer read outage for that account.
- The legacy balance tables are still written by the shadow writer. The cleanup job that drops them per account group is defined but not fully tested against a production-sized account group.
- The migration of the treasury workstation’s settlement view is still open. The treasury ops team wants the event stream to be queryable by settlement date before they switch over, and that query path is not built yet.
