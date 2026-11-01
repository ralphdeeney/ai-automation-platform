# AI Automation Platform Requirements

## 1. Purpose

The platform discovers founders worldwide, researches their companies, identifies credible AI-automation opportunities, finds permitted business contact channels, runs compliant scheduled outreach, accepts crypto payments, and gives operators one place to monitor the workflow.

## 2. Users and roles

- **Administrator:** configures integrations, users, policies, and system limits.
- **Campaign operator:** reviews leads, approves outreach, schedules campaigns, and handles replies.
- **Analyst:** reviews research, scoring, and evidence.
- **Finance operator:** creates payment requests and reconciles verified transactions.
- **Viewer:** read-only access to dashboards and audit history.

Role-based access control is required. Sensitive actions must be recorded in an immutable audit trail.

## 3. Functional requirements

### 3.1 Founder discovery

- Run configurable Apify actors for geography, industry, company size, and recency filters.
- Support worldwide discovery and preserve source URL, actor run ID, timestamps, and provenance.
- Normalize people and company records, deduplicate deterministically, and make imports idempotent.
- Respect source terms, robots/policy restrictions, rate limits, and applicable privacy law.
- Allow operators to review and reject discovered records before outreach eligibility.

### 3.2 Lead intelligence

- Research public company sources and cite evidence for claims.
- Produce company summaries, signals, likely workflow pain points, proposed AI-automation opportunities, and confidence scores.
- Separate observed facts from model inferences.
- Make scoring criteria versioned and explainable; allow human overrides with reasons.
- Detect stale or conflicting evidence and route uncertain results for review.

### 3.3 Business email discovery and verification

- Discover only permitted business email addresses through approved providers and public business sources.
- Record source, verification status, verification provider, timestamp, and confidence.
- Never generate or use sensitive personal contact data without a lawful basis.
- Suppress invalid, risky, opted-out, complained, or previously bounced addresses.
- Re-check suppression immediately before every send.

### 3.4 Google Sheets CRM

- Use Google Sheets, not Baserow, as the CRM system of record.
- Support configurable spreadsheets and stable row identifiers for leads, companies, campaigns, and activity summaries.
- Use a service account or OAuth with least privilege, batch writes, retries, and quota-aware backoff.
- Detect concurrent edits and avoid silently overwriting operator changes.
- PostgreSQL may keep sync cursors, locks, job state, and idempotency keys, but must not become a duplicate CRM.

### 3.5 Email campaigns

- Create drafts, segments, templates, schedules, sender identities, and multi-step follow-up sequences.
- Require an explicit approval gate before any live campaign starts.
- Support scheduled start, pause, resume, stop, and terminal completion states.
- Cancel pending follow-ups when a reply, unsubscribe, hard bounce, complaint, or stop condition is detected.
- Detect replies through provider webhooks or a least-privilege mailbox integration.
- Process unsubscribe requests immediately and expose a one-click unsubscribe mechanism where required.
- Enforce per-sender/domain rate limits, quiet hours, time zones, daily caps, idempotency, and retry limits.
- Keep delivery events and operational queue state in PostgreSQL; write useful activity summaries back to Sheets.
- Provide test/sandbox sending that cannot accidentally reach real leads.

### 3.6 Crypto payments

- Provide a branded payment page at `pay.litatech.xyz` with invoice amount, asset, network, destination, expiry, and status.
- Never expose private keys or seed material to the browser or repository.
- Verify payment independently from blockchain RPC/indexer data: correct chain, asset/contract, recipient, amount, confirmations, transaction success, and uniqueness.
- Handle pending, detected, confirmed, underpaid, overpaid, expired, failed, and manually reviewed states.
- Protect against replay, chain reorganizations, spoofed tokens, duplicate transactions, and client-supplied confirmation claims.
- Store invoices, verification observations, transaction identifiers, and audit events in PostgreSQL.
- Require approval before any production payment activation or fund-moving action.

### 3.7 Vision AI

- Host a lightweight image-understanding model on the InstaBox VPS.
- Accept authenticated image-analysis requests with bounded size and supported formats.
- Return structured descriptions/tags/confidence suitable for downstream automation.
- Apply request timeouts, concurrency limits, resource limits, and safe file handling.
- Avoid retaining uploaded images by default; make retention explicit and configurable.

### 3.8 Unified dashboard

- Show lead pipeline, research status, campaign state/delivery, replies, suppression, payments, job health, and service health.
- Provide filters, search, pagination, role-aware actions, audit history, and actionable error states.
- Require confirmations for high-impact actions and clearly distinguish sandbox from production.
- Obtain backend data through the API; do not embed provider credentials in the frontend.

## 4. Data requirements

- Google Sheets owns CRM entities and human-editable lead/campaign views.
- PostgreSQL owns operational state, queued jobs, locks, idempotency records, delivery events, payment records, and audit events.
- Store timestamps in UTC and present them in the operator's selected timezone.
- Define retention and deletion policies per data class and support subject-access/deletion workflows where applicable.
- Encrypt data in transit and sensitive persisted values at rest.

## 5. Non-functional requirements

- **Deployability:** Docker Compose deployment to an InstaBox VPS with health checks and persistent volumes.
- **Reliability:** idempotent jobs, bounded exponential retries, dead-letter handling, graceful shutdown, and recovery after restart.
- **Security:** least privilege, RBAC, CSRF/session protection as applicable, input validation, secret scanning, dependency scanning, and audited privileged actions.
- **Observability:** structured logs with correlation IDs, metrics, health/readiness endpoints, and alerts for queue, delivery, sync, payment, and resource failures.
- **Performance:** paginate external data, batch Sheets operations, and protect the VPS with concurrency/memory/CPU limits.
- **Maintainability:** modular services, versioned contracts, typed schemas, migration discipline, and automated tests.
- **Compliance:** configurable consent/lawful-basis fields, suppression enforcement, unsubscribe handling, and region/provider policy compliance.

## 6. Acceptance criteria for an initial production candidate

- An approved Apify run imports deduplicated leads into a configured Google Sheet with provenance.
- A reviewed lead has evidence-backed research, an opportunity score, and a verified permitted business address.
- A sandbox campaign demonstrates scheduling, pause/resume/stop, follow-up cancellation, reply handling, and unsubscribe suppression.
- A testnet invoice progresses only after independent on-chain confirmation and cannot reuse a transaction.
- The vision endpoint completes a representative image request within documented VPS resource bounds.
- The dashboard exposes the four core areas and operational health with RBAC.
- Compose recovers services after restart; backups and restore steps are tested.
- CI and security checks pass and the production gates have documented human approval.

## 7. Out of scope for the first release

- A general-purpose CRM replacing Google Sheets.
- Custody of customer private keys or automated treasury movement.
- Training a large foundation model.
- Fully autonomous outreach without operator approval and compliance controls.

