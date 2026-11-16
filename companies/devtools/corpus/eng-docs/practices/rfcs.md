# Writing an RFC

Owner: Product engineering · Last edited by Ingrid Holm

Some changes are small enough to discuss in a pull request, and some need a written proposal that the team can react to before any code is written. This page describes when Gantline uses RFCs, what the template looks like, and how a proposal becomes a decision.

## When an RFC is needed

An RFC is required when a change affects more than one team, changes a public contract (the CLI, the public API, the editor extension points, or the format of stored data), or introduces a new service or a new dependency that will be maintained by more than one group. If you are unsure whether your change needs an RFC, ask in #engineering and a product engineer will point you at the right process.

Smaller changes — a new flag on `gnt`, a bug fix in an existing service, a routine addition to the admin console — do not need an RFC. Use a normal pull request and the code review guidance in `eng-docs/practices/code-review.md`.

## The template

RFCs live as markdown files in the `rfcs` repo (a few service teams still keep an `rfc/` folder in their own repo). The template asks for:

- **Summary** — two or three sentences on what you propose and why.
- **Motivation** — the problem, with enough context that someone outside your team can follow it.
- **Design** — the actual change, including interfaces, data models, and operational impact. Diagrams are welcome but not required.
- **Alternatives considered** — at least one alternative, and why it was not chosen.
- **Open questions** — anything you have not resolved yet.

The template is deliberately short. If your RFC needs more sections, add them, but keep the five above in the order given.

## Review

Once the draft is in a pull request, ask for review from the teams that would own or operate the change. For platform-wide proposals, post a link in #engineering and in any team channel that would be affected (for example, #buildfarm for runner changes, #billing-ops for anything touching account data). The RFC author is responsible for chasing reviews; the pull request stays open until the relevant owners have commented.

For changes that touch the CLI, the editor, or the public API, Product engineering (Ingrid's team) must be included in the review. For changes to infrastructure or build services, loop in Infrastructure (Joaquim's team) and Release engineering (Georgia's team) as appropriate.

## Recording the decision

When the reviewers are satisfied, the RFC author updates the document with a **Decision** section at the top, stating what was decided and who approved it. The pull request is then merged. The RFC file remains in the repository as the record of the decision; do not delete it later. If the decision is later revisited, a new RFC supersedes the old one — do not edit an approved RFC in place.

Decisions that affect billing, legal, or customer commitments also need a sign-off from the relevant owner before the RFC is merged. For anything that changes what customers are promised, loop in Customer success early; Marcus's team has seen too many proposals that looked fine internally but contradicted a customer agreement. (tbc: who signs off billing-affecting RFCs — Mei-Ling's team to confirm.)

## How long an RFC stays open

An RFC stays open for at least five working days from the day the pull request is posted to #engineering, to give people in other time zones a chance to comment. After that, the author can merge once the required reviewers have approved, even if some optional reviewers have not responded. Still open: whether the five-working-day minimum applies to RFCs that touch the public API, or whether those need an extra review step — Henrik to confirm.

If an RFC has no meaningful review activity after ten working days, the author should ping the relevant team channels. If it still gets no response, escalate to the owner of the affected area.

One open question we have not settled: should RFCs that are superseded be moved to an `archive/` subdirectory, or left in place with a link to the newer RFC? To decide before the next quarterly cleanup (tbc).
