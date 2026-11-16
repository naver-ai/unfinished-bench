# Marketing consent

**Owner:** CRM & lifecycle  
**Last edited by:** Bilal Hughes (CRM Manager)  
**Applies to:** CRM & lifecycle, marketing, stores, wholesale, the helpdesk

## Purpose

This document sets out how we capture and record marketing consent for customers and contacts, and how we handle complaints about marketing. It covers every channel we send marketing on — email, post, and SMS — and how consent flows through the CRM into our sending tools.

## Scope

All Mossgrove staff who collect customer data or send marketing, including store colleagues using the POS back office, wholesale account managers, and the outsourced desk.

## 1. Opt-in sources

1.1 Consent must be captured at the point of data collection. The only acceptable sources are:

- Online checkout (orders-web and the checkout flow)
- Store POS back office at the till
- Wholesale account sign-up or renewal forms
- In-store events or competition entry forms
- The contact form on mossgroveoutdoor.co.uk
- Telephone orders handled by the helpdesk

1.2 Each source records a distinct consent flag in the CRM. The flags are: `email_opt_in`, `sms_opt_in`, `post_opt_in`. There is no combined "all channels" flag.

1.3 If a customer opts in on the phone, the helpdesk colleague must read the exact scripted opt-in wording from the CRM screen and log the time and date of the call against the consent record.

## 2. Soft opt-in

2.1 We apply soft opt-in for email only, and only where all three conditions are met:

- The customer bought a product from us (online, in store, or via wholesale account)
- The marketing is about a similar product or service to what they bought
- They had the chance to opt out at the point of purchase and did not

2.2 Soft opt-in does not apply to SMS or post. Those channels need explicit consent.

2.3 Soft opt-in is recorded automatically as `email_opt_in = soft` when the order is placed through orders-web or the POS back office. It must not be manually set by staff.

## 3. Consent flag sync from the CRM

3.1 The CRM is the source of truth for all consent flags. Campaigns in the mailer are built from CRM segments, so the flags the mailer sees are the ones in the CRM.

3.2 Flag changes propagate to mailer and the ad accounts through the standard CRM sync — this runs continuously. If a flag is updated in the CRM, the sync picks it up within a few minutes.

3.3 If a sync failure is suspected (for example, a customer who unsubscribed still receives a campaign), check the sync status in the CRM admin panel first, then contact the data-eng team via #data-eng. Do not edit flags directly in mailer.

3.4 Store colleagues must not change consent flags in the POS back office after the initial transaction. If a customer asks to change their marketing preferences in-store, the colleague should update the CRM record via the customer profile screen, which overwrites the POS flag.

## 4. Complaints about marketing

4.1 Any complaint about marketing content, frequency, or channel must be logged in the helpdesk as a complaint and tagged `marketing-consent`. This includes complaints received by store staff, the outsourced desk, or wholesale account managers.

4.2 The CRM & lifecycle team reviews tagged complaints twice a week. If the complaint relates to a specific campaign, the campaign owner is copied in and the campaign is paused until the review is complete.

4.3 If a complaint indicates that consent was not recorded correctly, the CRM record is corrected and the case is noted for the quarterly access review (see eng-docs/security/access-reviews.md) to check who changed the record.

4.4 For complaints escalated to the {{DATA_PROTECTION_REGULATOR}}, follow the incident process in eng-docs/oncall/incident-process.md and notify Ilse Jaramillo in Press & comms before responding to the {{DATA_PROTECTION_REGULATOR|code}}.

## 5. Retention and review

5.1 Consent records are kept for the life of the CRM account plus two years after account closure, per the records retention schedule in handbook/legal/records-retention.md.

5.2 This document is reviewed each quarter by the CRM & lifecycle team. Suggested changes go through Samir Farah before publishing.
