# Sending email campaigns

**Owner:** CRM & lifecycle  
**Last edited by:** Lucas Rao (CRM Manager)  
**Applies to:** Marketing email sends (customer-facing, transactional emails are handled by the mailer service and are not covered here)

---

## Overview

This covers the standard path for getting a marketing email from a brief in chat to a send that lands in inboxes. It applies to all CRM & lifecycle sends, including store event invitations, wholesale catalogue drops, and seasonal promotions. If you are sending to more than one country, read the country-specific notes in each step.

The mailer service reads campaign definitions from the analytics warehouse. The CRM team owns the campaign definitions. The warehouse team owns the mailer itself.

---

## 1. Brief

- The requester (marketing, brand, stores-ops, wholesale) posts a brief in `#marketing` and tags `@crm-lifecycle`. Include: audience, offer or message, send window, and whether it is a one-off or part of a lifecycle series.
- A CRM Manager picks it up and confirms the brief in the thread. If the audience is a segment that has not been used before, the CRM Manager works with Data Eng to get the segment added to the warehouse catalogue (`data-docs/catalogue.md`).
- If the send is time-sensitive (for example, a store opening or a wholesale price change), flag it in the brief and in the `#releases` channel so the platform team knows.

## 2. Build

- Create the campaign in the mailer's campaign editor. The editor is part of the mailer service UI; you get access through the CRM system role.
- Use a template from the brand asset library (`marketing-docs/brand/asset-library.md`). Do not build emails from scratch unless the brand team has signed off a new template.
- Set the audience by referencing the warehouse segment name. Do not paste a list of email addresses into the campaign editor.
- Set the send window. The mailer enforces quiet hours per country. For UK and IE, quiet hours are set by the mailer config. For US, quiet hours are set per state; the mailer applies those automatically. If you need to override quiet hours, that requires a change ticket and approval from the CRM Manager.
- Add suppression lists. The mailer automatically applies the global unsubscribe list, the hard-bounce suppression list, and the complaint suppression list. You do not need to add those manually. If the brief calls for a temporary suppression (for example, customers who were sent a similar email in the last two working days), add that as a separate list in the campaign editor.

## 3. Seed test

- Add seed addresses. The CRM team keeps a seed list of internal addresses (including the `#marketing` channel members and the CRM team). Add the seed list to every campaign before testing.
- Send a test to the seed list. The mailer sends test emails to the seed addresses only; it does not send to the real audience until you confirm.
- Check the test emails on at least two email clients. The CRM team standard is: one desktop client and one mobile client. If you do not have access to a device for mobile rendering, ask in `#marketing` for someone to check on their phone.
- Check links. Every link in the email should point to the live destination. The brand team checks links for campaigns that are part of a larger campaign; for smaller sends, the CRM Manager does the link check.
- If the email includes a promo code, verify the code is active in the pricing system before sending. The pricing team can confirm in `#pricing`.

## 4. Approval

- The CRM Manager approves the campaign in the mailer UI. For sends to more than 50,000 customers, the Head of CRM & Lifecycle also approves.
- For store-related sends (events, opening hours, local offers), the stores-ops team lead approves the copy in the campaign editor thread.
- For wholesale sends, the wholesale team lead approves the copy. This is a separate approval step because wholesale customers are not the same audience as retail customers, and the content is different.
- If the campaign includes a new audience segment or a new suppression rule, the data-eng team reviews the campaign definition before approval. They flag this in the campaign editor thread.

## 5. Send windows

- The mailer handles scheduling. You set the send time in the campaign editor. The mailer only sends during allowed windows per country.
- Standard send windows: UK and IE are weekday mornings (the mailer picks the exact time to avoid clustering with other sends). US sends are scheduled for weekday late morning US Eastern time. Store event sends go out on the first half of the week.
- If you need a send outside these windows, the CRM Manager raises a ticket with the platform team. Include the reason in the ticket. The platform team can override the window for a specific campaign.
- Monthly newsletter sends go out on the first working day of the month. The CRM team books these in the campaign editor at least two working days ahead.

## 6. Suppression lists

- The mailer applies the global suppression lists automatically at send time. You do not need to upload them.
- If a customer unsubscribes through the email footer link, the mailer updates the global unsubscribe list immediately. The CRM also picks up that status from the mailer, so they drop out of later campaign sends.
- If a customer unsubscribes via the support desk (for example, by phone or chat), the support agent updates the CRM record. The mailer reads the CRM status each time it prepares a campaign send, so the change reaches the next mailer campaign.
- If a customer complains through a mailbox provider (spam complaint), the mailer adds them to the complaint suppression list automatically. The CRM team reviews complaint rates in the post-send report (see step 7).

## 7. Post-send report

- After the send completes, the mailer generates a post-send report. The report is available in the campaign editor and in the warehouse.
- The CRM Manager reviews: delivered rate, open rate, click rate, unsubscribe rate, complaint rate. For store event sends, also review the number of customers who clicked the store location link.
- If the campaign included a promo code, the pricing team reviews redemption rates. They may ask the CRM team for the send list to reconcile against the pricing system.
- The CRM Manager posts a summary in `#marketing` within two working days of the send. Include the final numbers and any follow-up actions.
- Reports are kept in the warehouse for the retention period set out in the records retention policy (`handbook/legal/records-retention.md`).

---

## If it goes wrong

- **Email did not send at the scheduled time.** Check the campaign status in the campaign editor. If it says "failed", the mailer will have logged an error. Post the campaign ID in `#incidents` and tag the platform team. Do not resend without checking why it failed.
- **Email went to the wrong audience.** Stop the campaign in the campaign editor immediately if it is still running. If it has completed, the mailer cannot recall it. Post in `#incidents` and tag the CRM Manager. The data-eng team will review the segment definition to see what happened. Customers who received the email in error should not be suppressed unless they ask.
- **Links are broken.** If the email has already gone out, post in `#incidents` and tag the web team (shop-web). They can redirect the destination URL if the page is live but the link was wrong. If the page is not live, the web team will put up a temporary page. The CRM team will send a correction email only if the original email is likely to cause customer confusion (for example, a wrong store address).
- **Unsubscribe rate is higher than 0.5%.** Check the campaign content and the audience segment. If the unsubscribe rate is high, the CRM Manager reviews whether the audience was too broad or the content was not relevant. Do not send the same campaign again without changing the audience or the content.
- **Complaint rate is above 0.1%.** Stop any follow-up sends for that campaign and review the suppression list. The CRM Manager works with the brand team to check whether the email content triggered the complaints. The campaign may need to be redesigned before it can be sent again.
