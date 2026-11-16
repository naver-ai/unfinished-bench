# Onboarding a log source

**Owner:** Security operations (SOC)  
**Last edited by:** Tessa Duarte

This checklist covers adding a new log source to the SIEM, from parser creation through to telling the teams that need to know.

## Before you start

- [ ] Confirm the source is in scope for the SOC. If it is a new service, check with the owning team that the logs will actually be useful — we have had sources onboarded that nobody ever queried.
- [ ] Open a ticket in `tickets` under the Security project, type "Request", and link it to the source's deployment or change ticket.
- [ ] Check the data classification in `handbook/security/data-classification.md`. If the logs contain cardholder data or other restricted fields, note that in the ticket and flag it in #security before proceeding.

## Parser and field mapping

- [ ] Create the parser in the SIEM's parser library. Use the naming convention `<vendor>_<product>` and follow the style of existing parsers.
- [ ] Map fields to the common information model. If a field does not fit, leave it unmapped rather than forcing it — we can revisit later.
- [ ] Preserve the raw message in a dedicated field. We have needed this more than once for investigations.
- [ ] Set the timezone explicitly in the parser. Do not rely on the SIEM's default.
- [ ] Add the parser to the SIEM ingestion pipeline. Ask in #soc-platform if you are unsure which index the stream belongs in.

## Stream naming and routing

- [ ] Use the stream name format `<team>_<source>_<environment>`, for example `soc_nginx_prod`.
- [ ] If the source is multi-tenant, include the tenant or merchant identifier in the stream name only if it is stable. Otherwise keep it generic and rely on fields.
- [ ] Route the stream to the warm tier in `segctl` unless there is a specific reason to keep it in the hot tier. Cold storage is for sources we are unlikely to query more than a few times a quarter.

## Test events

- [ ] Ask the owning team to generate a small number of real events from the source. Do not use synthetic data — it does not exercise the same code paths.
- [ ] Verify the events appear in the SIEM within the expected ingestion lag. If they do not, check the parser, the stream, and the source's own logging config in that order.
- [ ] Confirm the field mapping looks right on the test events, especially timestamps, IP addresses, and any identifiers the SOC uses in triage (see `security-docs/soc/alert-triage.md`).
- [ ] Check that the events are not being dropped by any existing ingest rules. If they are, update the rules and re-test.

## Dashboards

- [ ] Create a dashboard for the source using the standard SOC dashboard template. Keep it to the views the SOC analysts actually use: volume, error rates, and any source-specific signals.
- [ ] Add the dashboard to the SOC dashboard folder. If the source is likely to be relevant to another team (for example #payments-platform or #partner-integrations), mention that in the dashboard description.

## Once it is live

- [ ] Update the SIEM source inventory in `security-docs` — there is a table of sources and their owners that we keep current.
- [ ] Post a short note in #soc-platform with the source name, stream name, and a link to the dashboard. Include the owning team so they know who to contact with questions.
- [ ] If the source generates alerts, make sure the alert rules reference the correct stream and that the on-call rotation in `paging` is wired up. Do not leave alerting for later.
- [ ] Tell the owning team when it is live so they can stop sending test events and rely on the pipeline.
- [ ] Add a line to the source's service documentation pointing to the SIEM stream and dashboard, so future engineers know where to look.
