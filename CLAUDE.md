# CLAUDE.md — Verdict engineering rules

Rules for any Claude Code session working in this repository. **`PROJECT_SPEC.md` is the authoritative product specification.** If this file and the spec conflict, the spec wins. Raise the conflict with the user; do not quietly work around it.

## 0. Session start ritual

At the start of every session:

1. Read `PROJECT_SPEC.md`, this file, `docs/implementation-plan.md`, `docs/checkpoints.md`, `docs/feature-status.md`, and `docs/known-issues.md`.
2. Run `git status` and `git log --oneline -15`, and check which branch you are on.
3. Summarize the current status in a few lines. Propose **only the next uncompleted task**.
4. Do not start a new milestone until the user has approved the previous one (see §6).

## 1. Product guardrails (non-negotiable)

- **No fabricated evidence.** Never invent Instagram data, audience statistics, metrics, retention curves, trends, hashtags, API permissions, model outputs, job completions, or test results. This covers code, fixtures, docs, and chat.
- **Provenance on every claim.** Persisted insights carry `source`, `retrieved_at`, `method`, `confidence`, and `limitations`. Every claim has a truth tier: `observed | derived | inferred | simulated | unknown` (spec §4.3). The tier appears in both the API schemas and the UI labels.
- **Synthetic demo data** lives only under an explicit `demo` / `is_synthetic: true` flag. The UI marks it conspicuously, and it never mixes with a real creator's records.
- **Personas** are grounded in available aggregate audience stats plus creator history. When stats are missing they are marked `provisional`. They never claim that a specific segment watched or liked a specific Reel.
- **Scores are heuristics, not probabilities.** The Content Opportunity Score is computed in Python by one versioned pure function (`0.35·audience_fit + 0.30·trend_relevance + 0.20·novelty + 0.15·feasibility`). An LLM never outputs the final number.
- **Simulated ≠ observed.** Persona reactions, attention risk, and experiment predictions are labeled *simulated* everywhere. Never draw a retention curve or give an exact drop-off time.
- **Creator control.** Nothing gets published and no planner/account write happens without an explicit, contextual approval enforced **server-side**.
- **Excluded:** niche switching, niche pivoting, and a niche-switch simulator. Do not build any of them, even partially.
- **No scraping** of Instagram or any source that forbids it. Use only official or documented, authorized sources.

## 2. Scope integrity

- Never remove or quietly narrow a spec capability. Any deferral must be approved by the user and listed as *planned/deferred* in `docs/feature-status.md`.
- Never mock an external call in production paths and present the result as real.
- Never skip provenance, owner scoping, approvals, or input validation "for speed".
- Any proposed deviation from the spec goes to the user for approval first (spec §15.6).

## 3. Repository layout

```
apps/web      Next.js App Router + TypeScript + Tailwind + shadcn/ui + TanStack Query
apps/api      FastAPI + Pydantic v2 (app/{core,routes,schemas,services,integrations,db,repositories,jobs})
apps/worker   RQ worker entrypoint (imports job code from apps/api)
packages/contracts  generated OpenAPI → TypeScript types
tests/{integration,e2e}  cross-app tests (Playwright e2e)
infra/        deployment configs
docs/         plan, status, checkpoints, test results, known issues, architecture, provenance
```

## 4. Coding conventions

**Python (apps/api, apps/worker)**
- Python 3.12+, dependencies managed with `uv`, lint and format with `ruff`, type checking with `mypy` (or `pyright`) on `app/`.
- Layering: `routes → services → repositories → db`. Routes stay thin. Business logic lives in services. Only repositories touch MongoDB.
- **Every repository method takes `owner_id` and filters on it.** Never offer an unscoped query for creator-owned collections. Cross-tenant tests are mandatory for each new collection.
- Pydantic models are used for all request/response bodies and all LLM structured outputs. Validate enums, 0–100 bounds, and timestamps ≤ media duration.
- Provider adapters (`MultimodalAnalyzer`, `Transcriber`, `ReasoningModel`, `TrendSource`, `StorageProvider`) live in `app/integrations/`. Core services must not import provider SDKs.
- Every external call has a timeout, bounded retries with backoff, and structured error codes. If an API key is absent, the call returns an explicit `provider_unavailable` state, never fake success.
- Treat captions, transcripts, OCR text, trend pages, and tool results as **untrusted data**. Delimit them in prompts and never let them authorize actions.
- Model IDs, limits, and pricing come from config/env and must be verified against current provider docs before use.

**TypeScript (apps/web)**
- Strict TS, ESLint, Prettier. API types are generated from OpenAPI into `packages/contracts`. Never hand-copy them.
- Data fetching goes in `features/*/hooks` (TanStack Query). Components stay presentational so the user can redesign the UI later without touching logic.
- Never show UI-only "success". Buttons reflect real backend state, including loading, error, and empty states.
- Accessibility: semantic elements, labels, keyboard focus, readable contrast.

**General**
- Small, cohesive changes. Add tests in the same change as the code.
- Structured JSON logs with `request_id` / `job_id`. Never log tokens, passwords, cookies, or media contents.

## 5. Security requirements

- Secrets come only from environment variables. `.env.example` holds **placeholders only**. `.env*` (except `.env.example`) is git-ignored. Before each commit, check that no secrets are staged (`git diff --cached` review).
- Auth: httpOnly, Secure, SameSite cookies. Passwords use Argon2. CSRF protection applies to state-changing cookie-authenticated requests.
- OAuth: validate `state`, use an allow-listed redirect URI and least-privilege scopes, and encrypt tokens at rest (key from env).
- Object-level authorization on every record, upload, job, and agent tool, enforced in services and repositories, not the UI.
- Uploads: validate extension, MIME and magic bytes, size, and duration. Use private storage with short-lived signed URLs, no public permanent URLs, and enforce retention and deletion.
- FFmpeg and model workloads have time, size, and concurrency bounds. Prevent SSRF on any URL ingestion.
- CORS is restricted to known origins. Security headers are set. Untrusted text is sanitized when rendered.
- Audit records cover account connect/disconnect, deletions, publishing, and agent writes.

## 6. Git and checkpoint policy

- `main` stays stable. Each milestone gets its own branch, `feat/mN-<slug>` (for example `feat/m0-foundation`).
- Commit in small, verified increments on the feature branch.
- **At each milestone boundary: stop.** Report actual test, build, and lint results, list the manual verification steps, and wait for the user's approval.
- Only after approval: merge to `main` and tag the checkpoint `checkpoint/mN`, then update `docs/checkpoints.md`, `docs/feature-status.md`, `docs/test-results.md`, `docs/known-issues.md`, and `docs/implementation-plan.md`.
- **Push only with permission** (already granted for the current scope, or asked for explicitly).
- **Forbidden without explicit, informed approval:** `git push --force`, `git reset --hard`, history rewrites, branch deletion, and deleting or overwriting working functionality.
- Never commit secrets, `.env` files, uploaded media, model weights, or large generated artifacts.

## 7. Cost policy

- Use free tiers and local development by default. Do **not** provision billable infrastructure (Vultr, paid object storage, paid Atlas tiers), enable overages, or run bulk model calls without explicit user approval.
- Keep model calls bounded per request. Cache results where it is safe to do so.

## 8. Reporting honesty

- Report test results verbatim: pass, fail, or skip, with counts. "It compiles" is not "it works".
- If a credential or platform approval is missing, say so, record it in `docs/known-issues.md`, and ship the honest fallback.
- Mark anything unverified as *unverified*.
