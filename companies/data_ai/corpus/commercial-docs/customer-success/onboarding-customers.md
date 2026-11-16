# Onboarding a new customer

**Owner:** Customer success and delivery  
**Last edited by:** Erin Reyes

## Before the kick-off

- [ ] Confirm the customer's subscription tier and contracted services in the CRM; sync with the commercial team if anything looks off.
- [ ] Create the customer workspace in the customer API console (see `data-docs/customers/aoi-orders.md` for AOI naming conventions).
- [ ] Provision API keys for the customer's named contacts; send them through the password manager, not by email.
- [ ] Tell the support desk that covers the customer's region (see `commercial-docs/support/coverage.md`).
- [ ] Invite the customer's technical lead to the tasking portal and the customer API console.
- [ ] Book the kick-off call. Rotterdam-based customers: offer a session that fits the working day; Denver-based customers: offer a slot that overlaps both offices.

## Kick-off call

- [ ] Introduce the delivery team (usually Samir Moreau or Maeve Fujita for water boards, Priya Lund or Camille Sharma for co-ops) and the Customer Success Manager.
- [ ] Walk through the monitoring subscription: which products are included, what the analytics API returns, and how the field app reports sensor status.
- [ ] Set expectations on imagery tasking: lead times, minimum order sizes, and how the tasking portal shows delivery dates.
- [ ] Explain the support model: helpdesk for tickets, the status page for service updates, and the escalation path in `commercial-docs/support/escalations.md`.
- [ ] Collect the list of AOIs and the names of people who should receive notification emails.
- [ ] Agree on the first training date (see below).

## Workspace and API setup

- [ ] Create the customer workspace subfolders for each AOI in the imagery catalogue.
- [ ] Configure API rate limits and quotas per the customer's tier; check the customer API console for the defaults.
- [ ] Set up webhook endpoints for job completion and sensor alerts if the customer wants them.
- [ ] Verify the customer can reach the API from their network; if they are behind a firewall, share the API's published IP ranges from the customer API console.
- [ ] Point the customer to the data catalogue (`data-docs/catalogue.md`) for the layers and bands they have access to.
- [ ] If the customer is a co-op, add their field staff to the field app; if a water board, confirm their sensor data feed is mapped to the right station IDs.

## First AOIs

- [ ] Run a test AOI order through the tasking portal with the customer on the call.
- [ ] Confirm the AOI polygons are inside the coverage area and that no part falls outside the area their subscription covers.
- [ ] Check the imagery ingest pipeline picks up the first delivery; see `data-docs/pipelines/imagery-ingest.md` if anything fails.
- [ ] Show the customer where the first products land in their workspace and how to pull them via the API.
- [ ] For sensor-network customers: walk through the sensor health view and the alert thresholds.

## Training sessions

- [ ] Water boards: one session on flood monitoring products, one on the analytics API for their engineers. Usually delivered by Samir or Maeve.
- [ ] Co-ops: one session on crop and soil monitoring dashboards, one on the field app for their agronomists. Usually delivered by Priya or Camille.
- [ ] Schedule training no later than two working days after the kick-off call.
- [ ] Provide the customer with the written quick-start guide from the customer API console.
- [ ] Record the session if the customer agrees; the recording goes in the shared drive under Customer Success.

## Ninety-day check-in

- [ ] Customer Success Manager reviews API usage and AOI order history with the customer.
- [ ] Check whether the customer is using the products they signed up for; if not, offer a refresher or a different training slot.
- [ ] Review sensor uptime and imagery delivery performance over the period.
- [ ] Confirm the customer's contacts are still correct and rotate API keys if anyone has left their team.
- [ ] Ask for a short testimonial or a reference call if the relationship is going well; hand the lead to Marcus.
- [ ] Update the CRM with the check-in notes and any follow-up actions.

## Notes

- If the customer asks for something outside their tier, open a ticket in the CRM and tag the commercial team — do not promise anything on the call.
- For public-sector customers, check `commercial-docs/sales/public-sector-tenders.md` before the kick-off for any specific requirements.
