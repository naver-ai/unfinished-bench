# Public-sector tenders

**Owner:** Sales  
**Last edited by:** Elif Farah  

This note covers how we respond to tenders from water boards, municipalities, port authorities and US state agencies. It is a working document — update it when we learn something from a submission.

## Bid / no-bid

The bid/no-bid decision sits with the VP Sales for the region. For tenders above €150k or $180k, Marcus Ellery is looped in before we commit to a response. For anything below that, Jasmine Madsen (Americas) or the EMEA-side Sales lead can decide.

We only respond when:

- The buyer's procurement process allows a commercial supplier to bid (some water boards require a cooperative arrangement we do not have).
- We can point to at least two reference customers in a similar segment (water board, port, agricultural co-op, insurer).
- The scope fits our existing monitoring subscriptions, imagery tasking orders or the analytics API. We do not bid on custom platform builds through tenders.

If a tender asks for functionality we do not have, we do not force a fit. Decline early and note the opportunity in the CRM so we can track the account.

## Who writes what

For a standard tender response, the account executive owns the submission and the timeline. The Sales Engineer writes the technical response. Sections are split as follows:

- **Commercial and pricing:** the account executive, with pricing from the current price sheet. If the tender requires a fixed-price schedule that differs from our standard packaging, the CCO signs off.
- **Technical approach and methodology:** the Sales Engineer, with input from the relevant delivery team. For flood monitoring, that is the sensor network team; for satellite imagery, the imagery ops team; for the analytics API, the Web app and API team.
- **Security questionnaire:** the security team (via the security channel). They maintain a standard response pack — request it through the team channel, not through individual engineers.
- **References:** the account executive collects reference contacts from the CRM. We only offer references who have agreed to be contacted for tenders. Check with the reference before including them.

The account executive is responsible for merging all sections into one document and checking that the response matches the tender's formatting requirements. The Sales Engineer reviews the merged version before submission.

## Security questionnaires

Most US state agencies and several Dutch water boards send a security questionnaire alongside the tender. These are handled by the security team. The standard response pack covers:

- Data classification and handling (see the data classification guidance in the handbook).
- Access controls and authentication.
- Sub-processors and where data is stored (our EU cloud region, as per the standard response).
- Incident response and reporting commitments.

If a questionnaire asks something not in the standard pack, the security team will coordinate a written answer. Send the questionnaire to the security channel as soon as you receive it — they need lead time. Do not draft security answers yourself, even when the question seems straightforward.

## References

References are a required part of most public-sector tenders. We maintain a shortlist of customers who have agreed to act as references. Current segments covered:

- Water boards (flood monitoring)
- Ports (water level and tide monitoring)
- Agricultural co-ops (crop and soil monitoring)
- Insurers (analytics API)

When a reference is used, confirm with the contact that they are still comfortable, and give them a heads-up on what the buyer might ask. The account executive handles this — do not pass reference contacts to the buyer before the reference has agreed.

## Loose ends

- A few tenders have asked for a security certification we do not hold. The security team is tracking which certifications are worth pursuing. Until that is decided, we decline tenders that require them.
- The standard response pack for security questionnaires lives with the security team. Ask in the security channel if you cannot find it.
- We have an older tender response template floating around from before we moved to the current sales tooling. Do not use it — the formatting does not match current buyer requirements.
- Pricing for tenders that include a multi-year commitment goes through the CCO. Margins on public-sector work are watched by finance — the FP&A team reviews any tender above €150k before submission.

If in doubt about whether a tender is worth the effort, ask on the sales channel before starting. A half-written response that misses the deadline is worse than a clear no.
