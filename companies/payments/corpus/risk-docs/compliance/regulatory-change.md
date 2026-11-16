# Regulatory change log

**Owner:** Compliance  
**Last edited by:** Aleksander Das (Compliance Analyst)

## Purpose

Tracks how new regulatory obligations are identified, assessed, and assigned within Kilbarra. The Compliance team maintains this log; input comes from the reg-reporting team, treasury-ops, and the payments platform group.

## Tracking sources

- EU legislative monitoring via our external counsel briefings — covers PSD3, the Payment Services Regulation, and the instant payments regulation.
- DORA follow-up guidance from the Irish regulator and {{SECURITIES_REGULATOR|code}}/{{CENTRAL_BANK_2|code}} Q&As.
- National implementation timelines flagged by Grace Osei or Ilse Dahl.
- Ad hoc items from internal audits, the transaction monitoring team, and merchant risk ratings reviews.

## Impact assessment process

When a new rule is identified:

1. Compliance drafts a short impact note covering: which Kilbarra systems are affected, which merchant segments are affected, and which revenue streams (card acquiring, e-money balances, payouts, partner platform accounts) are in scope.
2. The note is reviewed by the relevant engineering owner — usually via #payments-platform or #treasury-ops — plus a risk owner from Dovile Kazlauskaite's team.
3. A decision is recorded here: implement, monitor-only, or no action. Implementations get an owner and a target working day.

## Open items

| Item | Source | Owner | Target | Status |
|---|---|---|---|---|
| PSD3 — changes to surcharging rules for card transactions | PSD3 text | Grace Osei | WD+20 | Impact note in progress |
| PSR — new requirements for displaying fees on payment initiation | PSR draft | Ilse Dahl | WD+30 | Awaiting legal annotation |
| Instant payments — SCT Inst scheme participation for payouts | Instant payments reg | Selin Hayashi | WD+45 | Confirming whether we offer SCT Inst on payouts today |
| DORA — third-party risk register updates for partner feeds | DORA follow-up | Aleksander Das | WD+60 | Gap analysis against the partner feed inventory |
| DORA — ICT incident reporting thresholds | DORA RTS | Beatriz Fonseca | WD+15 | Mapping the current incident process to the reporting thresholds |

## Recently closed

- PSD2 SCA exemption for low-value contactless — no change needed; the current 3DS exemption settings in the payments gateway already comply.
- Instant payments confirmation of funds requirements — implemented in the core ledger; ledger API response includes available balance where required.

## Loose ends

- Need to confirm whether the PSR's "right to a business account" provisions affect our platform accounts for software partners — to raise with Felix Oyelaran's team.
- The instant payments item depends on whether the treasury workstation already supports SCT Inst — to ask in #treasury-ops.
- DORA item on partner feeds: the outsourcing-register team is pulling a list of sub-processors; we need to cross-reference it with the partner feed list.

## Open question

- Does the instant payments regulation's execution time requirement apply retroactively to payouts initiated before the rule takes effect, or only to new payment instruments? Awaiting counsel's view.
