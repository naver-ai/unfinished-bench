# Coordination of benefits

**Owner:** Claims  
**Last edited by:** Maeve Chandra

---

## When COB applies

A member has coordination of benefits when they are covered under more than one health plan. This includes:

- A spouse or domestic partner's employer plan
- A parent's plan (for dependents)
- {{PUBLIC_HEALTH_INSURANCE_1}} (Part A, Part B, or a {{MANAGED_PLAN_PROGRAM}} plan)
- A retiree plan from a former employer
- Another group plan through Kellsbrook Health Plan (rare, but happens with employer groups where both spouses work for the same employer)

The claims adjudication system determines primary and secondary automatically from the COB record on the member profile. If the COB record is incomplete or stale, claims can deny or pay incorrectly, so keeping it current matters.

---

## Primary vs secondary rules

The claims adjudication system applies these ordering rules in this order:

1. **Active vs retiree coverage** — If one plan is an active employee plan and the other is a retiree plan, the active plan pays primary.
2. **Birthday rule (dependent children)** — For dependent children covered under two parents' plans, the parent whose birthday (month and day only, not year) falls earlier in the calendar year has the primary plan. If both parents have the same birthday, the plan that has covered the parent longer is primary.
3. **{{PUBLIC_HEALTH_INSURANCE_1}} secondary payer** — For members with employer group coverage and {{PUBLIC_HEALTH_INSURANCE_1}}, the employer group plan pays primary if the employer has 20 or more employees. For individual plans and {{MANAGED_PLAN_PROGRAM}} members, {{PUBLIC_HEALTH_INSURANCE_1}} pays primary unless the member is covered under a spouse's active employer plan and that employer also has 20 or more employees.

When the claims adjudication system cannot determine primary automatically, the claim pends to the **COB work queue** for manual review. The examiner should validate the COB record and, if needed, ask the member for their other plan's Explanation of Benefits (EOB) before completing the claim.

---

## The COB questionnaire

The COB questionnaire is part of the member enrollment flow and is also available in the member portal under **Coverage → Other coverage**. It asks:

- Whether the member has other health coverage
- The type of coverage (employer, retiree, {{PUBLIC_HEALTH_INSURANCE_1}}, individual)
- The policyholder's name, date of birth, and relationship to the member
- The other plan's carrier and policy/member ID
- The other plan's effective and termination dates

The questionnaire is also collected at the following touchpoints:

- **Annual renewal** — Member services sends the questionnaire through the member portal for all individual and {{MANAGED_PLAN_PROGRAM}} members.
- **New dependent** — When a dependent is added to a policy, the questionnaire is triggered for the responsible party.
- **Provider services** — When a provider calls to ask about coverage and mentions other insurance, the provider services team can initiate the questionnaire request through the member portal on the member's behalf, but the member must complete it.

---

## Updating the COB record

When a member's other coverage ends, the COB record needs to be updated. This can come in as a member portal update, a call to member services, or a note from the employer group's benefits administrator.

To update the COB record in the claims adjudication system:

1. Open the member's profile in the claims adjudication system.
2. Go to the **COB** tab.
3. Select the other coverage entry and choose **End coverage**.
4. Enter the end date of the other coverage.
5. If the member states they have no other coverage now, select **No other coverage** as the new status.
6. Set the effective date of the change to the day after the other coverage ended.
7. Save the change. The claims adjudication system will re-price any pended claims that were waiting on COB.

If the member is adding new other coverage (for example, they changed jobs and have a new plan through their spouse), select **Add coverage** and complete the questionnaire fields directly rather than sending the questionnaire again.

---

## If it goes wrong

- **A claim paid as primary when it should have been secondary** — Recover the overpayment through the standard recovery process. Update the COB record first, then adjust the claim and reprocess.
- **The member says their other coverage ended months ago and we never updated it** — Update the COB record with the actual end date and reprocess claims that paid within the affected period. The retroactive change will reprocess automatically.
- **Two plans both say they are primary** — This is usually a birthday rule issue or a {{PUBLIC_HEALTH_INSURANCE_1}} secondary payer issue. Check the other plan's EOB or call the other carrier's COB line. If it cannot be resolved, escalate to Janet Kowalik's team.
- **The COB record shows coverage that the member says they never had** — Do not delete the entry. End it with the date the member says the coverage never started, and add a note to the member profile. The claims adjudication system audit trail retains the original entry.

---

## Related documents

- plan-docs/claims/adjudication-basics.md
- plan-docs/claims/timely-filing-and-corrections.md
- plan-docs/members/member-calls.md
