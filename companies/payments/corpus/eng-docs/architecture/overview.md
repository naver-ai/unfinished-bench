# System overview

**Owner:** Engineering  
**Last edited by:** Mateo Silva (VP Engineering)

## Purpose

This document gives a broad view of the Kilbarra production platform: the main services, the teams that own them, and how they fit together. It is meant as a starting point for anyone who needs to understand the shape of the system — new joiners, engineers moving between teams, and people in non-engineering roles who work with the platform.

The platform is split into two production regions: the EU region, which runs from our Dublin and Vilnius sites and serves merchants across the European Economic Area, and the US region, which supports our sponsor bank programme. Both regions are run by the same engineering teams in Dublin and Vilnius. The two regions are separate deployments with separate data stores; there is no cross-region replication of merchant or transaction data. Most of the services described below exist in both regions, with a few regional differences called out where they matter.

## Merchant-facing services

The merchant API is the primary interface for merchants and platform partners. It handles authentication, request validation, and rate limiting at the gateway, then routes to the relevant backend service. The Merchant payments team owns the API surface and the developer experience around it — versioning and deprecation. The API gateway in front of it is run by API platform & edge.

The hosted checkout is a separate service that renders payment pages for merchants who do not want to build their own UI. It is owned by the same team as the merchant API. The checkout talks to the payments gateway directly rather than going back through the merchant API, which keeps the critical path short.

## Payments gateway

The payments gateway is the core transaction processing service. It handles authorisation requests, capture, refunds, and 3DS flows. It maintains connections to the card schemes and to our acquiring banks, and it is responsible for keeping those connections healthy and for routing traffic when one of them degrades.

Merchant payments owns this service end to end. The service is stateless in the sense that it does not keep the system of record for transactions — it writes events to the payments bus and relies on the core ledger for the authoritative state — but it does keep a short-lived local cache of recent transactions for idempotency and fast retry handling.

3DS handling is split between the gateway and a dedicated 3DS service. The 3DS service manages the interaction with the cardholder's bank, including the redirect flows and the authentication result verification. The gateway calls into the 3DS service when a transaction requires authentication.

## Payments bus (pbus)

The payments bus is the internal event backbone. Every significant business event — authorisation result, capture, refund, payout instruction, merchant onboarding change — is published to pbus as an event. Consumers read from the bus and build their own views of the data.

The Payments platform team owns pbus. It is built on a partitioned message store; each partition is an ordered log. Message retention is generous but not unlimited; the retention policy is documented in the message store guide. Consumers are expected to keep up with the log, and there are SLOs around lag.

## Core ledger and ledger API

The core ledger is the system of record for all money movement. It is event-sourced (see ADR 0004) and holds the authoritative state for merchant balances, fees, settlement runs, and any internal adjustments. The ledger is not a payment system; it records movements that other services instruct.

The ledger API is the only way to read from or write to the ledger. Services that need to move money — the gateway for captures and refunds, the settlement service, the billing service — call the ledger API. Direct database access to the ledger store is restricted to the Payments platform team and is not available to other teams.

Payments platform owns both the core ledger and the ledger API; the ledger API engineers sit in Vilnius.

## Settlement and payouts

Settlement is the process of moving funds from the merchant's acquiring position into their Kilbarra e-money balance, and payouts move funds from the balance out to the merchant's bank account. These are separate services, both owned by Payments platform, and they share a lot of code.

The settlement service runs on a schedule — it settles transactions in batches according to scheme rules and our own cut-off times. The payout service is more event-driven: it picks up payout instructions from the bus, validates them against the merchant's account and risk profile, and submits them to the banking rails.

Both services are heavy users of the treasury workstation. The treasury operations team monitors the settlement and payout runs and handles exceptions — failed bank transfers, returned payouts, and the like. The payout service is also where the US region differs most from the EU region, because the banking rails and the sponsor bank arrangement have different settlement cycles and different file formats.

## Webhooks and events

Webhooks are how we push events out to merchants and partners. The webhooks service subscribes to pbus, filters for events that have webhook destinations, and delivers them to the registered endpoints with retries and signature verification. The contract is documented in the webhooks guide.

The webhooks engineers sit in Integrations & partners. They own the delivery infrastructure and the signing keys; the endpoint settings in the dashboard are built with Merchant apps.

## Scheme and bank file ingestion

A significant amount of external data arrives as files rather than API calls — scheme settlement files, bank statement files, chargeback files, and the like. The ingestion service handles these: it watches the file drop locations, parses the files, validates them against the expected format, and publishes the contents as events on pbus.

Data products owns ingestion. There is a separate service for each major file type, but they share a common framework for file handling, error reporting, and manual reprocessing. The reconciliation tool is the main consumer of the ingested scheme and bank files; it uses them to match our internal records against what the schemes and banks actually moved.

## Merchant dashboard and mobile app

The merchant dashboard is the self-service UI for merchants. It covers transaction search, balance and payout views, API key management, webhook configuration, and plan changes. It is a web application served from the same edge as the merchant API.

The mobile app is a native companion to the dashboard. It covers the most common merchant tasks — checking balances, viewing recent transactions, receiving push notifications about payouts and chargebacks. Both are built by the Merchant apps team and share most of their backend.

## Back office

The back office is our internal operations console. It is used by merchant support, risk, compliance, treasury, and billing. It provides views into merchant accounts, transaction history, risk flags, and the tools to take operational actions — updating merchant details, replaying webhooks, adding notes, and so on.

The back office is owned by the Merchant apps team. It is a large application with many feature areas, and it is often the first place a new internal tool gets built before it is productised into the merchant dashboard. There is a long-running effort to move back-office functionality into more focused internal services; ADR 0014 covers the retirement of the legacy merchant portal, which was the predecessor to both the dashboard and parts of the back office.

## Data platform

The data platform consists of the analytics warehouse and the data lake. The warehouse is the main destination for reporting and analytics; the lake holds raw event data for longer-term storage and for use cases that do not fit the warehouse. Both are fed from pbus through the data pipelines.

The Data platform team in Vilnius owns the lake pipelines, the warehouse schemas and the lake layout; the warehouse sync engineers in Data products keep the warehouse views in step with the ledger. The analytics warehouse has its own on-call rotation, documented in the lake pipelines and warehouse pages.

## EU and US regions

The EU region is the original deployment and the larger of the two. It runs the full set of services described above. The US region is a separate deployment that serves US merchants through the sponsor bank programme; it was stood up after the EU region and has a smaller service footprint.

The main differences in the US region are in settlement and payout — the banking rails are different, the sponsor bank has its own file formats and cut-offs, and the settlement cycle does not align with the EU one. The US region also has its own merchant API and dashboard instances, and its own back office instance, used mostly by the Austin teams. The data platform spans both regions: warehouse tables are partitioned by region, and the lake stores both. There is no cross-region traffic for payment processing; each region is self-contained for its merchants.

## Ownership summary

Merchant payments owns the merchant API, the hosted checkout, the payments gateway and the 3DS service. Payments platform owns pbus, the core ledger and the ledger API, and the settlement and payout services. API platform & edge runs the API gateway and the edge. Integrations & partners owns webhooks and partner integrations. Data products owns file ingestion and warehouse sync; Data platform owns the lake, the warehouse and the pipelines. Merchant apps owns the dashboard, the mobile app and the back office.

These boundaries are not absolute — there is a lot of collaboration across teams, and the platform teams in particular work on services that other teams operate — but they are a good guide to who to talk to about a given service. The organisation overview in the handbook has a fuller breakdown.
