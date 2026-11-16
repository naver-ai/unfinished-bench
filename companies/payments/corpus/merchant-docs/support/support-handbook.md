# Support handbook

**Owner:** Merchant support  
**Last edited by:** Clara Bianchi  

---

## Queues and triage

**Which helpdesk queues exist and what goes where?**

Our helpdesk has four queues: `merchant-support`, `partner-support`, `finance-support`, and `internal-support`. Merchant-facing requests land in `merchant-support` unless they come from a platform partner, in which case they go to `partner-support`. Anything that touches invoicing, fee disputes, or reconciliation queries gets routed to `finance-support` after initial triage if the merchant queue cannot resolve it. Internal requests (from other Kilbarra teams) go to `internal-support` and are handled on a best-effort basis.

**Who triages incoming tickets?**

Triage is shared across the whole team on a rotating daily rota. The triage person works through the unassigned queue, applies the correct queue and priority, assigns a named owner, and adds any relevant merchant account links. Triaging also means checking whether a ticket is actually a duplicate of an open conversation — if it is, close it and link it to the original.

**What are the priority levels and response targets?**

We use three priorities in the helpdesk. `P1` is for a merchant who cannot process payments at all or who has a live outage affecting their customers. `P2` is for a merchant who is impaired (for example, payouts delayed or dashboard errors) but still processing. `P3` is everything else.

First-response targets are based on merchant segment. Enterprise merchants (our top tier by volume) get a first response within one working hour during coverage hours. Platform partners get a first response within two working hours. Mid-market and smaller merchants get a first response by the end of the next working day. P1 and P2 tickets always get an immediate acknowledgement regardless of segment, even if the full response takes longer.

**What happens if a ticket sits in the queue past its target?**

The triage person for the day watches for anything approaching its target and reassigns or escalates if the assigned owner is unlikely to respond in time. If a ticket misses a target, the assigned owner notes why in the ticket and raises a flag so we can look at whether the queue needs rebalancing.

---

## Coverage and shifts

**What are the coverage hours?**

Coverage is split between Vilnius and Austin. Vilnius covers from early morning to mid-afternoon Vilnius time. Austin covers the US working day, which means we have someone available from roughly when the US East Coast comes online until late afternoon US Central. Dublin provides additional overlap during the middle of the day but is not a primary coverage site for the helpdesk.

**How do the shifts line up?**

Each site runs its own shift pattern. Vilnius has two shifts: a morning shift and a mid-day shift, with a handover between them. Austin has a single shift running across the US working day. The Vilnius and Austin shifts are timed so there is at least an hour of overlap during the US morning, which is when the highest volume of enterprise merchant traffic comes in.

**What does the handover between shifts cover?**

The outgoing person writes a short handover note in the `#merchant-support` channel covering: open P1 and P2 tickets and where they stand, any merchant who is waiting on a response from another Kilbarra team, anything that came up in the last shift that the next shift should keep an eye on, and anything that needs to be picked up the following working day. Handover notes are kept brief — a few bullets, not a novel. The incoming person reads the note and acknowledges it with a reply in the channel so we know the handover actually happened.

**Who is the escalation point when something goes wrong during a shift?**

The duty escalation for the helpdesk sits with the Merchant Operations desk. For technical incidents affecting payments or the merchant dashboard, follow the incident process in `eng-docs/incidents/incident-process.md` and page the on-call engineer. For anything involving a merchant being unable to process payments, always open an incident ticket in `tickets` even if you are not sure it is an incident yet — better to close it as a false alarm than to miss one.

---

## First response and macros

**What should the first response contain?**

The first response acknowledges the merchant by name, confirms we have received their request, and sets expectations. If we can resolve it immediately, we do. If not, we tell them what we are doing next and when they can expect an update. For P1 and P2, we also give them a direct contact path in case their issue becomes more urgent.

**Where do macros live and how are they organised?**

Macros live in the helpdesk under the `Merchant Support` macro group. They are organised by category: `greetings`, `onboarding`, `billing`, `payouts`, `payment-links`, `platform`, and `outage`. Macros are a starting point, not a final answer — always read the macro text before sending and adjust it to the specific merchant and situation. A blind macro send is how merchants end up with answers that do not match their question.

**How do I request a new macro or suggest a change?**

Talk to Lena Fischer or Clara Bianchi. We keep a running list of macro requests in the `#merchant-support` channel. If you find yourself typing the same thing three times in a week, that is a strong sign it should be a macro. Macros are reviewed quarterly to remove outdated content and make sure the language matches our current merchant messaging guidelines.

---

## Quality reviews

**How do quality reviews work?**

Each month, a sample of closed tickets from each support person is reviewed by a support lead. The review looks at whether the first response was within target, whether the resolution actually addressed the merchant's request, whether internal tools were used correctly, and whether the tone matches our writing guidelines in `merchant-docs/comms/writing-to-merchants.md`. Reviews are shared with the individual directly, not posted publicly.

**Who gets reviewed and how many tickets?**

Everyone in merchant support gets at least two tickets reviewed per month. If someone is new, they get four reviews in their first two months. If a particular ticket gets a complaint from a merchant, that ticket is always reviewed regardless of whether it was already in the sample.

**What happens if a review flags a problem?**

The reviewer discusses it with the person in a one-to-one. Most reviews produce small adjustments — a missing update on a ticket, a macro that needs rewording, a case where the merchant should have been pointed to the dashboard instead of given a manual workaround. Repeated issues in the same area lead to a focused coaching session. Nothing from a quality review goes into the HR system unless it is part of a broader performance conversation.

---

## Odd questions and edge cases

**What do I do if a merchant asks a question I cannot answer?**

You do not guess. You say you will check with the right team and get back to them, then you ask in `#merchant-success` or the relevant channel. For billing questions, `#billing` is the right place. For payout timing questions, `#treasury-ops`. For anything about a merchant's risk limits or chargebacks, ask in `#risk-controls` before answering. If you are not sure which channel, ask in `#merchant-success` and someone will point you to the right one.

**Can I promise a merchant a specific payout date?**

Only if you are certain. If the payout is already scheduled and visible in the treasury workstation, you can confirm it. If it is not visible, you say the payout is being processed according to the settlement schedule and you cannot give a specific time. Never invent a date to make the merchant feel better — a missed promise becomes a complaint, and we would rather under-promise.

**What about merchants who ask to speak to a manager?**

You ask what the concern is and try to resolve it first. If they insist, you escalate to Lena Fischer or Adrian Walsh for partner-related tickets. If it is a complaint about the support experience itself, point them to our complaints process as described in `risk-docs/compliance/complaints.md`.
