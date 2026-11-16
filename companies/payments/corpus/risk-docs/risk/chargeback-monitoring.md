# Chargeback monitoring

Owner: Risk controls. Last edited by Gideon Hartmann.

## Purpose

This note covers how Risk controls works with scheme monitoring programmes, the weekly chargeback ratio report, and merchant remediation plans. It is written for Risk controls staff and for the disputes desk in merchant operations.

## Scheme monitoring programmes

Kilbarra participates in the card scheme monitoring programmes for {{CARD_SCHEME_1}} and {{CARD_SCHEME_2}}. The programmes track chargeback ratios (and, for {{CARD_SCHEME_1}}, the fraud-to-sales ratio) on a rolling basis. The scheme thresholds are not always published in the same way, so we rely on the scheme dashboards through the acquirer portal and on the notifications we receive when a merchant is placed in a monitoring programme.

When a merchant is placed in a programme, the disputes desk will see the scheme notification first and should flag it in the case tool with the reason code and the programme window. Risk controls picks this up from the case tool and the weekly report.

## Weekly chargeback ratio report

The weekly chargeback ratio report is produced by Risk controls every week, using data from the reconciliation tool and the transaction monitoring system. The figures are pulled for the trailing eight weeks, which is the window the schemes use for their assessments.

The report lists:

- Merchants above the scheme ratio thresholds.
- Merchants trending towards the thresholds (defined as 60% or more of the threshold).
- Merchants in an active monitoring programme, with the programme end date and the current ratio.

The report is shared in the #risk-controls channel and with the disputes desk in merchant operations. It does not go to the wider business unless the disputes desk or Merchant success asks for it.

## Merchant remediation plans

When a merchant appears on the weekly report above the threshold, Risk controls opens a remediation plan. The plan is owned by Risk controls and the disputes desk together. It covers:

- The reason code breakdown for the merchant (from the transaction monitoring system).
- Whether the chargebacks are concentrated in a particular product or payment method.
- What the merchant has done so far (from the disputes desk notes).
- A remediation target: the merchant should be below the threshold within eight weeks.

The merchant is contacted through the merchant dashboard by the disputes desk. The disputes desk sends the initial notice, and Risk controls reviews the merchant's response. If the merchant does not respond within five working days, the case is escalated through the disputes desk to Merchant success.

For merchants already in a scheme programme, the remediation plan is made available to the scheme if they ask for it. The disputes desk handles that request, and Risk controls provides the numbers.

## Working with the disputes desk

The disputes desk sits in merchant operations and handles the day-to-day work of submitting and responding to chargebacks. Risk controls and the disputes desk meet twice a week to go through the weekly report and the open remediation plans.

The disputes desk owns the reason code data and the merchant-facing communication. Risk controls owns the ratio calculation and the decision on whether a merchant needs a remediation plan. Neither side should change the other's output without a conversation first.

## Loose ends

- The disputes desk still routes some scheme notifications through the old mail alias (the one from before the case tool rollout). We have asked them to move over; the notifications should not be acted on from the alias after the end of the quarter.
- The report initially used a lookup table in the analytics warehouse that was maintained by Finance engineering. Lina Gallagher moved the table into the reconciliation tool, and the report now reads from there. The old table is still in the warehouse but is no longer updated.
- The remediation plan template lives in the case tool. There is an older copy in the shared drive that is out of date; do not use it.
