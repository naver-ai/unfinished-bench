# Public API overview

**Owner:** Public API  
**Last edited by:** Leila Haddad (Engineering Manager, Public API)

## What this is

Gantline Cloud exposes a public REST API and webhooks that let customers automate their workspaces, repositories, CI runs, and organization administration. This document is the entry point for working on that surface: how it is versioned, how it is rate limited, how SDKs are produced, and how to add a new endpoint. If you are looking for how the API is hosted or operated, see the service catalogue entry for the API gateway and Mateo or Ivan in #api-platform.

## API versions

The API is versioned by date. A new version is cut roughly twice a year, usually aligned with the release train. Each version is a full snapshot of the API surface: when we cut a new version, the previous one keeps working as-is and is deprecated on a published schedule. We do not make breaking changes to a version once it has shipped. Additive changes (a new field, a new endpoint) go into the current version immediately and do not require a new version cut.

Deprecation policy: a version is supported for at least 18 months after the next version ships. The deprecation date and the supported-until date are listed in the public changelog entry for each version, and the API returns a `Sunset` header on requests to a deprecated version.

## Endpoints and conventions

The base URL is `https://api.gantline.dev`. All endpoints are under `/v1/` and then by resource area, for example `/v1/orgs/{org}/runners`. The OpenAPI specification lives in the `api-spec` repository and is the single source of truth for the public surface. If an endpoint is not in that spec, it is not public and should not be documented or relied on by customers.

We use JSON for request and response bodies. Timestamps are ISO 8601 UTC. IDs are opaque strings; do not encourage customers to parse them. Pagination is cursor-based, using `page` and `per_page` parameters; the response includes a `next_page` cursor when more results exist.

## Rate limits

Rate limits are enforced per API token and are tied to the customer's plan. The limits are documented in the plans page and are also returned in the `X-RateLimit-*` response headers so customers can build their own backoff logic. The current limits per token:

- Free plan: 100 requests per minute
- Team plan: 1,000 requests per minute
- Enterprise plan: 5,000 requests per minute, with burst allowance

These are per token, not per IP. If a customer needs more headroom on an Enterprise plan, they should contact their account manager; the account manager raises it with us in #api-platform and we can lift the limit for a specific token once we have looked at the use case. We do not advertise this in the docs.

Webhook deliveries are not counted against the rate limit, but a customer who is slow to acknowledge deliveries can cause us to drop events. See the webhooks section below.

## Webhooks

Webhooks are delivered as JSON POSTs to a customer-provided HTTPS endpoint. Customers register webhook endpoints per organization and choose which event types they want. Delivery is at-least-once; customers must respond with `2xx` within 10 seconds and must handle duplicates via the `X-Gantline-Event-ID` header. We retry with exponential backoff for up to 24 hours, then the event is dropped and appears in the dead-letter report in the admin console.

Signature verification is mandatory. Each webhook endpoint has a secret; the signature is HMAC-SHA256 of the raw body using that secret, sent in the `X-Gantline-Signature` header. SDKs handle this automatically. Do not relax signature verification for any customer, and do not add endpoints that allow unverified delivery.

## SDKs

SDKs are generated from the OpenAPI spec for Python and TypeScript. The generation pipeline runs as part of the release train, and the generated packages are published to the package indexes by the CLI & SDKs team using relctl. The SDKs are versioned independently of the API versions; each SDK release pins the API version it was generated from.

When you add or change an endpoint, the SDKs are regenerated automatically at the next release. You do not need to hand-write SDK code. If a generated SDK is missing something (for example, a convenience method that would be genuinely useful), raise it with the CLI & SDKs team in #cli rather than patching the generator locally.

## Public changelog

Every user-visible change to the API — new endpoints, new fields, new webhook events, deprecations, rate limit changes — must have a changelog entry. Changelog conventions are in `eng-docs/release/versioning.md`; entries are published on the docs site with the release notes. Write the entry in the style guide's tone: short, factual, no marketing. Include the API version it applies to and, for deprecations, the supported-until date.

If a change is not user-visible (an internal refactor, a bug fix with no behavior change), it does not need a changelog entry, but it still needs a code review like any other change.

## How to add an endpoint

Adding a public endpoint is a normal code change with a few extra steps. The checklist:

1. **Design review.** Before writing code, write a short design note in the PR describing the resource, its fields, and the operations. For anything non-trivial, post the note in #api-platform for a quick review. Hana and Bianca are good people to poke if you want a second pair of eyes.
2. **Spec first.** Add the endpoint to the OpenAPI spec in the same PR as the implementation. The spec is the contract; if the spec is not merged, the endpoint is not public. The validation CI job will fail if the spec and the implementation drift.
3. **Implementation.** Implement against the spec. Use the shared API framework in the `api` service; do not hand-roll auth, pagination, or error formatting. Follow the error format documented in the spec (a `code`, a `message`, and an optional `details` object).
4. **Tests.** Add unit tests for the handler and integration tests that exercise the endpoint through the gateway. See `eng-docs/practices/testing.md` for the conventions. Every endpoint must have at least one test that covers an auth failure and one that covers a validation error.
5. **Rate limits.** Check that the endpoint falls under the existing per-token limits. If it is a heavy operation (for example, a bulk export), we may need to add a secondary limit; raise that in the design review rather than after the fact.
6. **Docs.** Add the endpoint to the public API reference on the docs site. This is generated from the OpenAPI spec as well; make sure the description fields in the spec are complete enough that the generated docs are useful. Write the changelog entry as described above.
7. **Rollout.** The endpoint ships with the next release train. If it needs to go out sooner (for example, for a customer who is waiting on it), talk to the on-call engineer in #releases. Do not merge a public API change directly to the release branch without going through the release process.

## General notes

- The API is served from both regions; the gateway routes to the region that matches the customer's data residency setting. See ADR 0011 for why we do this and `infra-docs/cloud/accounts-and-regions.md` for the region layout.
- We do not expose internal service names, hostnames, or error details in API responses. If an internal error occurs, the customer sees a generic `internal_error` code and we see the details in the metrics dashboards. If you find yourself tempted to return an internal error message, stop and fix it.
- The public API does not depend on internal-only services. It runs on the same hosted platform that customers use, which keeps us honest about what we ship. If you find the API depending on something that is not available to customers, that is a bug.
- For questions about the API's operational side (alerts, on-call, capacity), see the on-call guide and ask in #api-platform. For questions about what customers can do with the API, the customer success team in #customer-success usually knows the common patterns and can point you at a real customer example.
