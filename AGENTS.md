# Engineering Instructions

## Scope

These instructions apply to the entire repository. More specific `AGENTS.md` files may refine them for a subtree.

## Delivery workflow

1. Work on a feature branch and open a pull request; never push directly to `main`.
2. Implement one small, independently testable task at a time.
3. Run the relevant tests and independently inspect the resulting behavior or configuration.
4. If verification fails, make at most two bounded fix attempts before documenting the blocker.
5. Record commands, results, and limitations in `docs/progress.md`; never fabricate evidence.
6. Continue through approved roadmap tasks while safe, in-scope work remains.

## Safety gates

Explicit human approval is required before:

- deploying to production;
- starting a live email campaign or sending non-test email;
- initiating, refunding, or otherwise moving funds;
- destructive data or infrastructure operations;
- pushing directly to `main`.

Never commit secrets, credentials, API tokens, seed phrases, or private keys. Keep secrets in environment variables or an approved secret manager. Keep `.env` files untracked and provide redacted `.env.example` templates.

## Architecture rules

- Google Sheets is the system of record for CRM lead and campaign-facing data. Do not introduce Baserow.
- PostgreSQL stores only operational state, job/queue metadata, idempotency keys, and payment records.
- Services communicate through versioned HTTP contracts and durable queued jobs; avoid shared service internals.
- All externally triggered writes must be idempotent and auditable.
- Email discovery must use lawful sources and permitted business addresses. Honor suppression, unsubscribe, and provider policies before every send.
- Payment status is determined by independent on-chain verification, never only by a browser redirect or client callback.
- Keep the vision service lightweight enough for the target InstaBox VPS and place it behind resource limits.

## Quality rules

- Prefer typed interfaces, structured logs, health checks, and explicit timeouts.
- Add tests for new behavior and regression tests for fixes.
- Do not weaken or delete tests merely to obtain a passing build.
- Pin production dependencies deliberately and review upgrades.
- CI must run linting, tests, secret scanning, and container/config validation where supported.
- Keep modules small and avoid coupling vendor SDKs to domain logic; use adapters.

