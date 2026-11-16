# Enterprise onboarding

**Owner:** Customer success  
**Last edited by:** Nkechi Obi

This checklist covers the first working weeks of an enterprise account, from kickoff through the first check-in. Customer success leads the process; support and engineering teams join where noted.

## Kickoff

- [ ] Schedule the kickoff within 5 working days of the signed order. Invite the customer's technical lead and the CSM assigned to the account (Dev, Kirsten, or Aurelie on larger accounts).
- [ ] Confirm the customer's region (EU vs. US) so the right cloud region is used. EU customers stay in the EU region per ADR 0011.
- [ ] Send the customer a copy of our public API overview and the editor overview so they know what integrations are available.
- [ ] Create the customer org in the admin console. Add the CSM and the support team as org admins.
- [ ] Set up the success plan in the admin console (template: `enterprise-success-plan`). Fill in the customer's goals and the expected rollout date.

## SSO connection

- [ ] Ask the customer for their IdP details (SAML or OIDC metadata). Point them at the SSO setup guide on the docs site if they need background.
- [ ] Create the SSO connection in the admin console. Use the identity team's checklists; they own the IdP side.
- [ ] Test the connection with a single test user before enabling it for the whole org.
- [ ] Enable the connection and confirm the customer can sign in. Leave a note in the ticket if anything needs follow-up.

## Repository migration

- [ ] Collect the list of repos to migrate. Check with the customer whether they want history or just latest state.
- [ ] Use `gnt repo import` for each repo. For large repos, ask in #sre if the import times out.
- [ ] Set up branch protection rules to match what the customer had on their old host. Confirm the rules with the customer before applying.
- [ ] Migrate open pull requests where the customer asks for it. Note: this is manual, so queue it behind the repo imports.
- [ ] Update the customer's DNS or webhooks so their CI endpoints point at Gantline Cloud runners.

## Runner configuration

- [ ] Confirm whether the customer will use hosted runners or their own. Most enterprise accounts start with hosted runners.
- [ ] For hosted runners: pick the runner pool (default or a dedicated pool if the customer has compliance requirements). The Hosted runners team (Grace's team) can provision dedicated pools — open a ticket.
- [ ] Set up the runner registration token in the customer org. Make sure the token is stored in the password manager, not in the customer's chat.
- [ ] If the customer needs custom runner images, point them at the custom images page on the docs site.

## Success plan

- [ ] Schedule the success plan review for the first week after the customer is live. Marcus or Lucia usually join for larger accounts.
- [ ] Define the rollout milestones with the customer: which teams move first, which repos come over when, and who the internal champions are.
- [ ] Set the renewal cadence (see `cs/renewal-cadence.md` for the standard timelines).

## First check-in

- [ ] Book the first check-in for two working days after the customer is fully live. Use the customer's timezone, not Lisbon time.
- [ ] Prepare a short list of what to cover: usage stats from the metrics dashboards, any open support tickets, and whether the SSO and runner setup is holding up.
- [ ] If anything is blocked, escalate through the escalations doc.

## Open questions

- Should the checklist include a step for customers who want to migrate their CI pipelines from their old host, or is that covered by the runner configuration section? We've had two customers ask about it this quarter.

## Still thin

- The SSO section could use more detail on what to do when the customer's IdP doesn't support SAML (tbc).
- The success plan section is missing the template fields for the customer's adoption targets. The admin console has the fields but the CS team hasn't agreed on the defaults yet.
