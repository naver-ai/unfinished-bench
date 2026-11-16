# Email programs

**Owner:** Growth & lifecycle  
**Last edited by:** Mara Finch (Mobile Marketing Lead)

This document covers the lifecycle email programs we run from the email platform: the new-org onboarding sequence, the product update newsletter, and trial-ending emails. It also covers templates and how we report on opens and activation.

## Onboarding sequence for new orgs

1. A new org is created in the Gantline Cloud admin console when the first seat is claimed. The admin console fires an `org.created` webhook to `lifecycle-events` in the data warehouse.
2. The `lifecycle-worker` job in the email platform picks up the event and enrols the org into the onboarding sequence. The sequence has five messages:
   - WD+0: welcome to Gantline Cloud, with links to the docs site and the community forum.
   - WD+2: invite the rest of the team (link to the admin console's Members page).
   - WD+4: set up a cloud workspace and open a repo in the web editor.
   - WD+7: connect your first self-hosted runner (link to the runner setup page on the docs site).
   - WD+12: check billing and seats, and review the plan.
3. If the org has more than one owner, the owner who claimed the first seat gets the messages. If that person has not logged in since enrolment, the email platform re-routes the remaining messages to another owner.
4. Unsubscribe links and the list-unsubscribe header come from the `lifecycle` template footer; the email platform handles them.

## Product update newsletter

- Sent twice a month, on the first and third working day, mid-morning Lisbon time.
- Content is assembled from the release notes on the docs site. The Growth & lifecycle team curates the top items; the rest of the team can propose items in #growth.
- The newsletter goes to all opted-in addresses on the `product-updates` list. We maintain the list in the email platform; opt-in is captured on the docs site and in the web editor.
- The send is scheduled via the email platform's campaign scheduler. The campaign name must start with `product-updates-` so the metrics dashboards pick it up.

## Trial-ending emails

- Trials run for 30 days from org creation. The email platform checks the trial end date daily and sends:
  - WD-3: trial ending soon, with a link to the plan page in the admin console.
  - WD-1: last day, with a link to billing settings.
  - WD+0: trial ended, invite to downgrade to a free plan or contact sales.
- If the org converts to a paid plan before the trial ends, the worker removes the org from the trial-ending queue. The admin console emits `org.plan_changed`, which the email platform consumes.
- If the org's trial expires and the org has no active seats, we do not continue emailing. The customer success team picks up these orgs through the CRM.

## Templates

- All lifecycle emails use the `lifecycle` template group in the email platform. Templates live in the `templates/lifecycle/` folder and are versioned.
- The templates use the brand basics from `growth-docs/brand/brand-basics.md`. If you change a template, check that the header and footer match the current brand guidelines.
- Variable fields: `{{org_name}}`, `{{first_name}}`, `{{last_name}}`, `{{admin_console_url}}`, `{{docs_url}}`, `{{community_url}}`. Do not add new variables without checking with Devin Alcott, who owns the template variables.
- We test templates by sending to the `growth-test` list in the email platform before scheduling a campaign.

## Reporting

- Opens and clicks are tracked by the email platform and streamed to the metrics dashboards. The relevant dashboard is `Lifecycle Email Performance`.
- Activation is measured as: the recipient creates a cloud workspace within 7 days of the email send. The `lifecycle-worker` job writes an `email.activated` event to the data warehouse when it sees a workspace creation with a matching email interaction.
- The Growth & lifecycle team reviews the dashboard at the end of each month and posts a summary in #growth. If a message in the onboarding sequence has an open rate below the team's target for two consecutive months, we revise the copy or the send timing.

## If it goes wrong

- If a scheduled newsletter is not sent, check the campaign status in the email platform first. If the status says `failed`, look at the error in the campaign log. Most failures are from an invalid variable in a template — the log line names the recipient and the variable.
- If the onboarding sequence does not fire for a new org, verify that the `org.created` webhook reached the lifecycle-events topic in the data warehouse. If it did not, check the admin console's webhook delivery log and re-deliver the event from there.
- If a trial-ending email goes to an org that already converted, that is usually a race between the plan change and the daily check. The email platform de-duplicates on `org_id` and `message_key`, so the duplicate is dropped. If it still lands in the inbox, tell Stella Ibarra in #support so they can reply to the customer.
- For anything else, ask in #growth and, if it is an email platform outage, check the status page.
