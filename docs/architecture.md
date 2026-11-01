# Modular System Architecture

## 1. System context

```text
Operator -> Dashboard -> FastAPI API -> domain services
                                  |-> Google Sheets (CRM)
                                  |-> PostgreSQL (operational state)
Founder Discovery -> Apify -------|
Lead Intelligence -> research/AI -|
Email Outreach -> mail provider ---|
Crypto Payments -> chain RPC/indexer
Vision AI -> local lightweight model
```

The API is the authenticated control plane. Long-running or retryable work is represented as durable jobs in PostgreSQL. Services own their domain behavior and integrate with vendors through adapters. Google Sheets remains the CRM source of truth.

## 2. Repository modules

| Module | Responsibility | Primary dependencies |
| --- | --- | --- |
| `apps/dashboard` | Administrative web UI | API only |
| `apps/api` | Authentication, RBAC, validation, orchestration, health | PostgreSQL, service APIs |
| `services/founder-discovery` | Apify runs, normalization, deduplication, Sheets writes | Apify, Google Sheets |
| `services/lead-intelligence` | Evidence collection, opportunity analysis, scoring | research providers, model provider, Sheets |
| `services/email-outreach` | Campaign state machine, scheduler, delivery and inbound events | email provider, PostgreSQL, Sheets |
| `services/crypto-payments` | Invoice lifecycle and independent chain verification | RPC/indexer, PostgreSQL |
| `services/vision-ai` | Resource-bounded image understanding | local model runtime |
| `infra/docker` | Compose deployment, container config, health checks | Docker Engine/Compose |

## 3. Data ownership

Google Sheets stores lead/company CRM fields, review decisions, campaign membership, and operator-facing activity summaries. PostgreSQL is restricted to operational tables such as `jobs`, `job_attempts`, `sync_cursors`, `idempotency_keys`, `campaign_runs`, `scheduled_messages`, `delivery_events`, `inbound_events`, `suppression_events`, `payment_invoices`, `chain_observations`, `payment_transactions`, and `audit_events`.

Each CRM row receives an immutable platform ID. Sync operations compare an expected row version or content hash before update. Conflicts are surfaced for human resolution.

## 4. Main workflows

### Discovery and qualification

1. An operator approves discovery criteria.
2. Founder Discovery starts an Apify run and records its provenance.
3. Results are normalized, deduplicated, and written to Sheets in batches.
4. Lead Intelligence gathers sources and returns facts, inferences, opportunity proposals, and a versioned score.
5. Email discovery verifies a permitted business address and checks suppression.
6. The operator approves qualified leads for a campaign.

### Campaign lifecycle

```text
draft -> approved -> scheduled -> running -> completed
                         |          |  ^
                         v          v  |
                       stopped    paused
```

`stopped`, `completed`, and `failed` are terminal. A transaction locks due messages, re-checks campaign/suppression state, and creates an idempotent provider send request. Provider webhooks are signature-verified and deduplicated. Replies, unsubscribe, complaints, and hard bounces suppress future steps before acknowledgment.

### Payment lifecycle

```text
created -> pending -> detected -> confirmed
    |          |          |
    +-------> expired     +-> review (mismatch/reorg/underpayment)
```

The page may display a transaction submission, but only the verifier changes authoritative payment status. Verification uses allowlisted networks and token contracts, recipient and amount checks, receipt success, configured confirmations, and a unique `(chain_id, transaction_hash, log_index)` constraint.

## 5. Service contracts

- REST/JSON contracts are versioned under `/v1` and described with OpenAPI.
- Commands accept an idempotency key and return a stable operation/job ID.
- Events contain event ID, type, schema version, occurred-at time, correlation ID, and aggregate ID.
- Outbound calls use explicit connect/read timeouts, bounded retries with jitter, and circuit-breaking where appropriate.
- Health endpoints distinguish liveness (`/health/live`) from dependency readiness (`/health/ready`).

The initial scaffold implements a dependency-free liveness endpoint at `/health`; readiness is added when database access is introduced.

## 6. Security boundaries

- TLS terminates at a reverse proxy; internal services are not publicly exposed unless required.
- Dashboard authentication uses secure, HTTP-only sessions or a vetted OIDC provider; authorization is enforced by the API.
- Secrets are injected at runtime and rotated; `.env` is development-only and ignored.
- Webhooks require signature verification, replay windows, and idempotency.
- Uploaded images are decoded in an isolated, resource-bounded service and deleted after processing by default.
- Live email, production payments, deployment, and destructive operations require explicit approval recorded as audit events.

## 7. Deployment topology

Docker Compose runs the reverse proxy (future), dashboard, API, worker processes, PostgreSQL, and vision service on a private network. Only required ingress ports are published. Named volumes persist PostgreSQL and model assets. Containers run as non-root users where possible, expose health checks, have restart policies and resource limits, and receive secrets through VPS-managed environment files or Docker secrets.

Backups encrypt PostgreSQL dumps and necessary configuration off-host. Restore exercises are scheduled and evidenced. Google Sheets data is protected through Google Workspace retention/export controls rather than copied wholesale into PostgreSQL.

## 8. Observability

All services emit JSON logs containing timestamp, level, service, correlation ID, and safe identifiers. Metrics cover job age/failures, Sheets quota/conflicts, send/reply/bounce/unsubscribe rates, invoice verification lag, RPC health, model latency, and resource pressure. Logs must redact addresses, message bodies, tokens, and payment secrets.

## 9. Key architectural decisions

- **Modular services with adapters:** isolates vendor changes and permits independent resource controls.
- **PostgreSQL-backed jobs initially:** avoids adding a second infrastructure datastore on a small VPS; a dedicated broker can be introduced only with measured need.
- **Sheets as CRM, PostgreSQL as operations:** preserves the required operator workflow without abusing Sheets as a queue.
- **Independent blockchain verifier:** eliminates trust in browser callbacks.
- **Small local vision model:** aligns inference cost and resource usage with InstaBox constraints.

