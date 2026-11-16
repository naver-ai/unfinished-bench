# Merchant due diligence (KYB)

**Owner:** Financial crime  
**Last edited by:** Kalani Bose (KYB Analyst)

## Purpose

This document describes how Kilbarra collects and verifies merchant information at onboarding, how we assign an initial risk rating, what triggers enhanced due diligence (EDD), and how we keep merchant records current through periodic refresh. It applies to all new merchant applications and to existing merchants when their circumstances change.

## Scope

Covers merchants onboarded through the KYB onboarding tool, including direct merchants, platform partners' sub-merchants where Kilbarra performs KYB, and US merchants acquired through the sponsor bank programme. It does not cover partner programme eligibility (see `merchant-docs/partners/partner-programme.md`) or ongoing transaction monitoring (`risk-docs/aml/transaction-monitoring.md`).

## 1. Information we collect at onboarding

1.1 Every merchant application must include, at minimum:

- Legal entity name, registered address, and jurisdiction of incorporation.
- Registration number or equivalent company identifier.
- VAT number where applicable (EU merchants) or tax identifier (US merchants).
- Nature of business and expected product/service descriptions.
- Website URL(s) and a brief description of how the merchant sells online.
- Estimated monthly processing volume and average transaction value.
- Settlement currency and settlement bank account details.
- Principal place of business if different from registered address.

1.2 For each merchant, we collect beneficial ownership information. A beneficial owner is any individual who directly or indirectly holds 25% or more of the shares or voting rights, or who otherwise controls the entity. We require:

- Full name, date of birth, and nationality.
- Residential address.
- Percentage of ownership or nature of control.
- Government-issued ID for each beneficial owner (passport or national ID).

1.3 For companies with complex structures (trusts, foundations, holding companies, or multiple layers), we may need to look through additional levels to establish the ultimate beneficial owner. If the structure cannot be established to our satisfaction, we treat the application as requiring EDD (see section 4).

1.4 We review the merchant's website as part of onboarding. The review checks:

- That the site is live and reflects the business described in the application.
- That the products or services offered match the declared MCC.
- Payment methods and checkout flow, where visible.
- Contact details on the site match the application.

1.5 The merchant's MCC is assigned by the KYB analyst at onboarding based on the primary business activity. The MCC determines base risk category (low, medium, high) as set out in the risk rating matrix in the KYB onboarding tool. Where a merchant has multiple business lines, we use the highest-risk MCC.

## 2. Risk rating at onboarding

2.1 Every merchant receives an initial risk rating: low, medium, or high. The rating is calculated in the KYB onboarding tool using:

- Jurisdiction of incorporation and residence of beneficial owners.
- MCC and product type.
- Expected processing volume and velocity.
- Ownership structure complexity.
- Any adverse media or sanctions hits.
- Whether the merchant is a platform partner or direct merchant.

2.2 Low-risk merchants are typically straightforward businesses in low-risk jurisdictions with simple ownership and modest processing volumes. Medium-risk merchants are the default for most online businesses. High-risk merchants include those in restricted MCCs, high-risk jurisdictions, or with complex ownership.

2.3 The initial rating is provisional until the merchant has completed onboarding and, where applicable, an EDD review. The final rating is recorded in the KYB onboarding tool and visible to the merchant support and risk teams.

2.4 Ratings are reviewed at each periodic refresh (section 5) and may change based on new information, including transaction monitoring findings, chargeback activity, or changes in beneficial ownership.

## 3. Standard due diligence (SDD)

3.1 For low-risk merchants, we complete SDD:

- Verify company registration via the relevant registry or a commercial data provider.
- Verify beneficial owners against sanctions and enforcement lists.
- Perform a basic adverse media check on the entity and beneficial owners.
- Confirm the website and MCC as described in section 1.4.
- No additional information is required unless something in the checks raises a flag.

3.2 SDD checks are completed within the KYB onboarding tool. Where a check returns no hits, the analyst confirms and moves the application forward. Where a check returns a potential hit, the analyst reviews and either resolves it (e.g., false positive) or escalates to EDD.

## 4. Enhanced due diligence (EDD)

4.1 EDD is required when any of the following apply:

- The merchant is a politically exposed person (PEP), a family member of a PEP, or a close associate of a PEP.
- Any beneficial owner or director appears on a sanctions list or is in a jurisdiction subject to sanctions.
- The merchant's jurisdiction of incorporation or residence is on the FATF list of high-risk jurisdictions, or is otherwise flagged by our risk team.
- The merchant operates in a high-risk MCC (e.g., gambling, digital assets, adult content, pharmaceuticals) as defined by the risk rating matrix.
- The merchant's ownership structure involves trusts, foundations, or multiple layers that obscure ownership.
- The merchant is unable or unwilling to provide the required documentation.
- Any adverse media suggests financial crime, fraud, or regulatory action.
- The merchant requests unusually high processing volumes relative to its stated business.
- A platform partner's sub-merchant triggers any of the above.

4.2 EDD requires, in addition to SDD:

- Source of funds and source of wealth for the merchant and, where applicable, its beneficial owners.
- Evidence of the merchant's physical operations (e.g., lease, utility bill, or site visit where practical).
- Independent verification of directors and beneficial owners through a second source.
- Explanation of any sanctions or adverse media hits, with supporting documentation.
- For high-risk jurisdictions: rationale for why the business is legitimate and how it operates.
- Approval from a Financial Crime Manager before the merchant can be onboarded.

4.3 EDD information is recorded in the KYB onboarding tool under the merchant's file. Where documents are provided in a language other than English or Irish, we may require a certified translation.

4.4 A merchant that triggers EDD but cannot be satisfactorily verified is declined. The decision is recorded in the KYB onboarding tool, and the merchant is notified through the standard decline process.

## 5. Periodic refresh

5.1 Merchant records are refreshed on a cycle based on risk rating:

- Low risk: every 36 months.
- Medium risk: every 24 months.
- High risk: every 12 months.

5.2 Refresh involves re-running the SDD or EDD checks described above against the merchant's current records. We confirm:

- That the registered entity is still active and in good standing.
- That beneficial owners have not changed (or that any changes have been captured).
- That the merchant's website and business activity still match the declared MCC.
- That there are no new sanctions or adverse media hits.

5.3 Where a refresh identifies a change that affects risk rating (e.g., new beneficial owner in a high-risk jurisdiction, change of business line to a higher-risk MCC), the merchant is re-rated in the KYB onboarding tool and the refresh cycle resets from the new rating.

5.4 If the merchant does not respond to refresh requests within 60 working days, we apply a temporary hold on new payouts and write to the merchant. The hold is lifted once the refresh is completed or the merchant provides the requested information.

5.5 Refresh tasks are queued automatically in the KYB onboarding tool. The Financial Crime team owns the queue and works through it ahead of the due date so that no merchant goes past its refresh date without action.

## 6. Working in the KYB onboarding tool

6.1 All KYB work is done in the KYB onboarding tool. Applications arrive there from the merchant application flow; analysts claim and work them. Notes and documents attached to a merchant's file are visible to the Financial Crime team and, where relevant, to Merchant Support through the back office.

6.2 Each application has a status: `draft`, `in review`, `approved`, `declined`, or `hold`. Only a KYB Analyst or Financial Crime Manager can move an application to `approved`. Declines require a Financial Crime Manager's confirmation.

6.3 Documents uploaded to the KYB onboarding tool are stored in line with the records retention schedule (`handbook/legal/records-retention.md`) and are accessible only to users with the KYB role.

6.4 Where the KYB onboarding tool is unavailable, the Financial Crime team works through the queue manually using the case tool and records decisions there, then backfills the KYB tool when it is available again. The team is notified of outages through the `#risk-controls` channel.

6.5 The KYB onboarding tool passes the onboarding rating to Risk controls, and the rating sets the limits profile the merchant starts on (see `risk-docs/risk/merchant-risk-ratings.md` for how ratings work).

6.6 Questions about a specific application are raised in the KYB onboarding tool's comment thread or in `#risk-controls` when they need a second pair of eyes. Do not discuss merchant information in `#general` or other non-risk channels.
