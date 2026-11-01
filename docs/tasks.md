# Implementation Roadmap

Tasks are ordered, small, and testable. Complete and evidence one task before starting the next.

## Phase 0 — Foundation

- [x] F0.1 Add repository engineering instructions and product documentation.
- [x] F0.2 Scaffold application, service, infrastructure, and CI boundaries.
- [x] F0.3 Add FastAPI liveness endpoint with unit test.
- [x] F0.4 Add Compose configuration for API and PostgreSQL with health checks and static tests.
- [ ] F0.5 Add dependency lock/update policy and lint/type-check configuration.
- [ ] F0.6 Add PostgreSQL migrations for operational jobs and audit events.
- [ ] F0.7 Add API readiness check and graceful dependency failure behavior.
- [ ] F0.8 Add CI container build/Compose validation on a Docker-capable runner.

## Phase 1 — Identity and Google Sheets CRM

- [ ] F1.1 Define RBAC roles and authenticated API skeleton.
- [ ] F1.2 Implement Google OAuth/service-account adapter with least-privilege scopes.
- [ ] F1.3 Define Sheet tabs, columns, stable IDs, and validation rules.
- [ ] F1.4 Implement idempotent batch upsert and sync cursor.
- [ ] F1.5 Detect row conflicts and expose reconciliation workflow.
- [ ] F1.6 Add audit events for privileged actions.

## Phase 2 — Founder discovery

- [ ] F2.1 Define discovery request and normalized founder/company schemas.
- [ ] F2.2 Implement Apify adapter with timeout, retry, and run provenance.
- [ ] F2.3 Add deterministic normalization and deduplication tests.
- [ ] F2.4 Add queued import workflow and Sheets batching.
- [ ] F2.5 Add operator review endpoints and dashboard view.

## Phase 3 — Lead intelligence and email verification

- [ ] F3.1 Define evidence, fact, inference, opportunity, and score schemas.
- [ ] F3.2 Implement research-source adapters with citations and freshness.
- [ ] F3.3 Implement versioned, explainable scoring with review thresholds.
- [ ] F3.4 Implement permitted business-email discovery adapter.
- [ ] F3.5 Implement verification and global suppression checks.
- [ ] F3.6 Add qualification review UI and Sheets synchronization.

## Phase 4 — Email outreach

- [ ] F4.1 Implement campaign state machine and transition tests.
- [ ] F4.2 Implement approval gate, scheduler, rate limits, and quiet hours.
- [ ] F4.3 Implement sandbox provider adapter and idempotent delivery.
- [ ] F4.4 Implement pause, resume, stop, and pending-job cancellation.
- [ ] F4.5 Implement signed delivery/reply webhook ingestion.
- [ ] F4.6 Implement follow-up cancellation on reply/bounce/complaint.
- [ ] F4.7 Implement unsubscribe endpoint and atomic suppression enforcement.
- [ ] F4.8 Add campaign dashboard, metrics, and failure recovery tests.
- [ ] F4.9 Obtain explicit approval before connecting a live sender or campaign.

## Phase 5 — Crypto payments

- [ ] F5.1 Select allowlisted test networks/assets and define invoice schema.
- [ ] F5.2 Build branded `pay.litatech.xyz` payment UI in test mode.
- [ ] F5.3 Implement RPC/indexer adapter and receipt/log verification.
- [ ] F5.4 Add confirmation, replay, reorg, token, and amount tests.
- [ ] F5.5 Implement reconciliation dashboard and audit history.
- [ ] F5.6 Run end-to-end testnet payment and document evidence.
- [ ] F5.7 Obtain explicit approval before production payment activation.

## Phase 6 — Vision AI

- [ ] F6.1 Benchmark candidate lightweight models against VPS constraints.
- [ ] F6.2 Implement authenticated structured inference endpoint.
- [ ] F6.3 Add size/type limits, transient storage cleanup, and timeouts.
- [ ] F6.4 Add CPU/memory/concurrency limits and representative tests.
- [ ] F6.5 Integrate health and latency monitoring into the dashboard.

## Phase 7 — Dashboard and operations

- [ ] F7.1 Build dashboard shell, authentication, and role-aware navigation.
- [ ] F7.2 Add lead, campaign, payment, and monitoring views.
- [ ] F7.3 Add confirmations and clear sandbox/production indicators.
- [ ] F7.4 Add structured logging, metrics, alerts, and correlation IDs.
- [ ] F7.5 Add encrypted backup and tested restore procedure.
- [ ] F7.6 Complete security, privacy, load, and failure-mode reviews.
- [ ] F7.7 Obtain deployment approval and execute the production runbook.

