# Writing to customers

**Owner:** CRM & lifecycle | **Last edited by:** Bilal Hughes (CRM Manager)

This applies to any email sent to customers or wholesale partners, whether it goes out through mailer, the CRM, or is drafted by hand in support. Store staff sending local messages should follow the same rules.

## Tone of voice

- Write like a person, not a brochure. Short sentences, active voice.
- Use "you" and "we". We are Mossgrove, the customer is the reader.
- Be warm but not matey. No jokes, no exclamation marks except in genuine greetings ("Happy birthday!").
- When something has gone wrong, say so plainly and say what we are doing about it. Do not bury it.
- For wholesale partners, drop the cheerfulness slightly. They want facts and dates.
- Read it out loud. If you would not say it that way, rewrite it.

## Plain English

- Aim for reading age 11–12. The analytics warehouse logs readability scores for campaign emails; if you are under 60 on the Flesch scale, tighten it up.
- Avoid jargon: "SKU", "SKU-level", "backorder", "chargeback", "ledgerctl", "CRM" — none of these go in customer-facing text.
- Use "we" and "you" instead of "the company" or "the customer".
- Spell out acronyms the first time, then use the short form if you must. Better: do not use the short form at all.
- Use plain numbers and dates. "3 working days", "within 2 weeks", "by the end of the month".
- No legal boilerplate beyond what the Legal team has signed off. If you think you need a paragraph of terms, ask before adding it.

## Sign-offs

- Standard sign-off for customer email: "Best regards," then the sender's first name and surname, then "Mossgrove Outdoor & Home Ltd" on the next line.
- For wholesale: "Kind regards," then full name, role, and phone number. Wholesale partners sometimes need to call back quickly.
- Never sign off with just a first name in an automated mailer message. Customers need to know who they are dealing with.
- If the email is from a shared mailbox (like a store or the helpdesk), sign with the mailbox name plus a real person's name in brackets: "The Leeds store team (Samira)".

## What never goes in an email

- Full payment card numbers, card security codes, or PINs. Never. Even masked, do not put card numbers in email. If a customer sends them to us, reply asking them to phone the helpdesk instead.
- Passwords, one-time codes, or sign-in links that expire. We do not send these by email at all.
- Bank account or sort code details for refunds. We only use the existing payment method or the refunds flow in the POS back office / finance systems.
- Personal data about anyone other than the recipient. No order details for a different person, no account notes, no internal dispute info.
- Anything marked internal or restricted in the data classification guide (handbook/security/data-classification.md).
- Links to internal tools, chat channels, or wiki pages. Customers do not see those.
- Pricing or discount codes that have not been approved by Pricing or Marketing. Check the feature flag service if you are unsure whether an offer is live.

## Accessibility basics

- Use a plain font, left-aligned text, and a minimum font size equivalent to 14px in the email builder.
- Headings should be real headings (H1, H2), not bold paragraphs. The mailer template does this automatically; do not override it.
- Alt text on every image. Describe what the image shows, not just "camping tent".
- Do not use colour alone to convey meaning. "The green button" means nothing to someone using a screen reader.
- Keep links descriptive: "read our returns policy" not "click here".
- Buttons in emails must have a text fallback. The mailer does this, but check if you hand-code anything.
- No flashing or moving content in email. Ever.

## Practical checks before sending

- Run the spellchecker. Read it once as the customer, not as the author.
- Check that any dates, working days, or cut-offs match the current calendar. When in doubt, ask the team that owns the process.
- Verify that all links point to the live site or the correct portal. Broken links get reported.
- If the email mentions a store, confirm the store is still trading and the address and hours are correct. Stores close and hours change.
- If the email mentions a product, check it is not discontinued or out of stock indefinitely. The catalogue on the website is the source of truth.
- For anything going to more than a handful of people, ask another person on the team to read it first. Two pairs of eyes catches most mistakes.

## Questions

- If you are unsure whether something is allowed in an email, ask CRM & lifecycle before sending. Better to ask than to send something we have to un-send.
- For urgent issues with an email that has already gone out, contact the CRM team in #crm or raise a ticket through the helpdesk.
