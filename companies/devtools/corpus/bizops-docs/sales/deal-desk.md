# Deal desk

**Owner:** Sales  
**Last edited by:** Colette Ramirez (Account Manager)

The deal desk is the review step for deals that fall outside the standard sales motion. It exists to keep pricing and terms consistent across the sales team, and to make sure finance has visibility into commitments before they reach a customer signature. Most deals never touch deal desk; if you are unsure whether a deal needs it, ask in #sales before you send a quote.

## When a deal goes to deal desk

A deal must go through deal desk if any of the following is true:

- Contract term is longer than 36 months
- Payment terms are not net-30 or annual prepay
- Seat count is over 2,000 at close, or the contract value is over $250k annual recurring
- Any discount below the bands in the table below
- Any usage of the public API or hosted runners that is not on the published rate card

Deals that only need a quote refresh, a seat adjustment within the same plan, or a renewal at the same terms do not go through deal desk.

## Discount bands

Sales can approve discounts within the bands below without deal desk, as long as the deal meets the criteria above. Anything below the floor of the band goes to deal desk.

| Plan | Standard discount band | Floor |
| --- | --- | --- |
| Team (per-seat) | 0–10% | 10% |
| Business (per-seat) | 5–15% | 15% |
| Enterprise (per-seat, annual prepay) | 10–20% | 20% |
| Enterprise (per-seat, invoiced) | 5–15% | 15% |

Discounts are calculated on the published list price for the plan and seat count at the time the quote is created. Volume-based pricing for large seat counts is separate from discounts; if you are quoting over 2,000 seats, the standard band does not apply and the deal goes to deal desk regardless.

## Who sits on deal desk

Deal desk is a small group pulled from Sales and Accounting & payroll. The Sales side is usually the Head of Sales (Alba Bergstrom) or the Chief Revenue Officer (Grant Holloway) for the largest deals. The finance side is always someone from Accounting & payroll who can commit to billing terms; Gaurav Jensen is the usual reviewer. The Account Manager who owns the deal does not sit on deal desk for their own deal, but they present the deal and answer questions.

Deal desk meets twice a week, or on request if a deal is time-sensitive. Turnaround is one working day for most deals; deals that need a payment-terms change can take two working days because billing needs to configure the schedule in the billing service.

## What deal desk checks

- Final discount against the bands above, and the reasoning for any overage
- Payment terms and whether the billing service supports them (the billing team can confirm in the admin console)
- Seat count and whether the plan matches the seats quoted
- Contract length and renewal timing, checked against `bizops-docs/cs/renewal-cadence.md`
- Any custom terms that would need the customer paper redlined — those go to `bizops-docs/legal/customer-paper.md`

When deal desk approves a deal, the Account Manager can issue the quote. When it does not approve, the Account Manager gets a short note on what needs to change — usually the discount, the term, or the payment schedule.

## Logging deal desk decisions

Every deal desk decision is logged in the CRM with the deal record. Use the deal desk field to record the outcome and add a note with the date the decision was made and who approved it. If a deal is approved but the customer later changes the scope significantly (seat count, term, or plan), the deal goes back through deal desk with the updated numbers.
