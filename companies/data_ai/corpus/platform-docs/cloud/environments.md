# Environments

> Needs updating after the move — ping #cloud-platform if something here looks wrong.

This page describes the main environments we run and what lives in each. For infrastructure changes, see `iac-workflow.md`; for how environments map to cloud accounts, see `accounts-and-projects.md`.

## Overview

| | Dev | Staging | Production |
|---|---|---|---|
| Purpose | Local development and early integration | Pre-release validation | Customer-facing |
| Cloud project | `brakwater-dev` | `brakwater-staging` | `brakwater-prod` |
| Access | Any engineer, self-serve (see below) | Platform team + nominated engineers | Named roles per system |
| Data | Synthetic or small samples | Masked subset of production | Full production data |
| Deploys | From your branch | From `main` via CI | Through the release pipeline |

## What runs where

| Component | Dev | Staging | Production |
|---|---|---|---|
| Web app | Local containers | Yes | Yes |
| Analytics API | Local containers | Yes | Yes |
| Ingest pipelines | On demand, small files | Yes, full schedule | Yes, full schedule |
| Model serving | Local only | Staging endpoint | Shadow and production endpoints |
| Warehouse | Local or shared dev schema | `wh-staging` | `wh-prod` |
| Batch cluster | — | Staging queue | Shared pool |

The customer API console and tasking portal only run in staging and production. The field app is developed against staging by default.

## Data in staging

Staging uses a masked subset of production data. Masking is applied at ingestion time by the warehouse loading jobs; sensor readings are offset and rounded, customer names and coordinates are replaced with synthetic equivalents, and imagery thumbnails are downsampled. The masked subset is refreshed on a working-day cadence from the last completed production load.

If you need a specific production record in staging that is not in the subset, request it via `data-docs/governance/data-access.md` — do not copy production data into staging directly.

## Getting a dev project

Dev projects are created on request in the `brakwater-dev` project via the IT service desk. Once the project exists, tag it with your team so the spend shows up in your showback. Most teams also have a shared dev namespace on the notebook server; check `handbook/it/access-requests.md` for the standard set of permissions.

The dev environment does not have its own copy of the imagery catalogue — use the staging catalogue or a small local extract for development.

## Notes

- Staging is a single shared environment. Long-running experiments or load tests should run in dev or on the batch cluster, not in staging.
- The analytics API in staging points at the staging warehouse; the production API points only at `wh-prod`.
- Model serving rollouts always go through staging first — see `ml-docs/serving/rollout.md`.
- Ingest pipelines in staging run the same schedule as production but with a smaller input window, so pipeline changes can be validated end to end before release.
