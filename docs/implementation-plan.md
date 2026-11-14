# Verdict — Implementation Plan

**Status:** DRAFT. Awaiting user approval. No application code exists yet.
**Source of truth:** `PROJECT_SPEC.md`. This plan sets the order of work and how each step is verified. It does not change scope.
**Last updated:** 2026-11-14 (session 1)

---

## 1. Time budget and strategy

- Plan drafted at 2026-11-14 02:10 UTC, which is Fri Nov 13, ~21:10 US Eastern.
- **Submission deadline: unconfirmed.** If it is Sunday Nov 15 morning ET, about **34–36 working hours** remain for one person, including sleep and the demo.
- Strategy: build **one honest, working vertical slice** (spec §13), deploy it early, then deepen it. Every hour estimate below is a planning guess, not a commitment.
- **Hard cut lines** (re-evaluated at each checkpoint):
  - By **T+20h**: the slice M0→M4, M6, and the M7 core runs locally from demo fixtures.
  - By **T+26h**: M8 basics and the planner done. Deployed at least once.
  - Last **4h**: freeze features, rehearse the demo, fix bugs, update docs. Nothing new after the freeze.

### MVP critical path (hackathon)

```
M0 → M1(min) → M2(import + demo fixtures) → M3 → M4 → M6(+M5 fallback) → M7 → M8 → M9(planner only) → M12(deploy + demo)
```

Off the critical path for the hackathon (still full-product scope, tracked as *planned*): live Meta OAuth (M2b, attempted only if a Meta app with tester access already exists), live trend adapters (M5b), full experiments (M9b), the agent (M10), publishing and learning (M11).

---

## 2. Key technical decisions (for approval)

| # | Decision | Proposal | Why / Ponytail Lite note |
|---|---|---|---|
| D1 | Auth | FastAPI-owned email/password auth (Argon2), server-side sessions in MongoDB, httpOnly cookie. Next.js proxies `/api/*` to FastAPI via rewrites so cookies are same-origin. | No third-party auth account, and the backend stays the authority for tenant scoping. A provider like Clerk or Auth.js can be swapped in later behind `AuthService`. |
| D2 | DB driver | PyMongo's native async API (`AsyncMongoClient`). Motor is deprecated in favor of it; the version is verified at M0. | One driver. |
| D3 | Local MongoDB | No Docker daemon or `mongod` in this dev container. M0 will check, in order: a MongoDB Atlas free (M0) cluster (user-provided URI), a downloaded `mongod` binary, or `mongomock-motor`/in-memory **for unit tests only**. Integration tests need a real `mongod` or Atlas. | Document whichever works. |
| D4 | Queue | Redis 7 (installed locally) + RQ worker. Job state mirrored into the Mongo `jobs` collection. | As in spec. |
| D5 | Object storage | `StorageProvider` interface. A `LocalStorageProvider` with HMAC-signed, short-expiry upload and download URLs for dev and the hackathon. An `S3StorageProvider` (presigned) is enabled once a free or approved bucket exists. | Same contract as presigned S3, no spend. |
| D6 | Transcription | `Transcriber` adapter. Primary: Groq-hosted Whisper large-v3-turbo (verify availability, limits, and free-tier quota). Fallback: local `faster-whisper` small/base on CPU, clearly recorded as the model actually used. | Large-v3 on CPU is too slow for a live demo. |
| D7 | Multimodal | Gemini Flash-family via `google-genai` SDK. Input: scene-sampled frames **with timestamps** + transcript segments + metadata, requiring structured JSON output validated by Pydantic. Model ID read from env and verified at M7. | Timestamps grounded in our own sampling, so they can be validated against the duration. |
| D8 | OCR | PaddleOCR **deferred behind a flag** (heavy install). In the MVP, Gemini reads on-screen text from the frames, and the findings are labeled `inferred`. | The spec says "where useful". Marked *deferred*, not removed. |
| D9 | Reasoning / agent | Groq GPT-OSS via `ReasoningModel` adapter (verify the model ID and tool-calling support at M10). For M3/M4/M6 semantic synthesis, use Gemini or Groq, whichever is verified first. | |
| D10 | Score fallback | A missing component is set to a **neutral 50**, flagged `missing: true` with a `fallback_reason`, and confidence is downgraded one level per missing component. Formula `scoring_version = "cos-v1"`. Alternative: renormalize weights over the available components. **Needs your choice.** | The spec requires an explicit, documented fallback. |
| D11 | Trend sources | MVP: `TrendSource` interface + "unavailable" adapter → trend_relevance falls back per D10 and the UI says *trends unavailable*. Stretch (M5b): candidates to verify are the YouTube Data API `videos.list chart=mostPopular` (documented, free quota) and the Google Trends API (alpha/limited access, needs verification). No Instagram scraping. | Honest degradation. |
| D12 | Frontend | Next.js App Router, TS, Tailwind, shadcn/ui, TanStack Query, Recharts, `openapi-typescript` for contracts. Package manager: pnpm. | As in spec. |
| D13 | Hosting | Vercel Hobby (frontend, free). API + worker: **Vultr costs money and needs your approval.** Free alternatives to evaluate if not approved: run the API and worker on one small VM you already have, or a free-tier PaaS. Redis: same host. Mongo: Atlas M0 free. | Cost policy. |
| D14 | CI | GitHub Actions (public repo, free minutes): ruff, mypy, pytest, tsc, eslint, next build. Playwright e2e runs locally until it is stable. | |

---

## 3. Milestones

Each milestone is built on branch `feat/mN-<slug>`, ends with a report and user approval, and is then tagged `checkpoint/mN`.

### M0 — Foundation (~3h) · depends on: none
**Scope:** monorepo skeleton (`apps/web`, `apps/api`, `apps/worker`, `packages/contracts`), `.gitignore`, `.env.example` (placeholders), `README.md`, config loading (pydantic-settings), structured logging with request IDs, Mongo connection + `GET /api/v1/health` and `/ready` (ready checks Mongo + Redis), Next.js page showing live API health, OpenAPI → TS type generation script, Makefile or `justfile` dev commands, GitHub Actions CI.
**Acceptance:**
- `make dev` (or equivalent) starts web + api + worker locally. The UI shows real health/readiness, and a red state when Mongo or Redis is down.
- `pytest` (health, config) passes. `ruff`, `mypy`, `tsc`, `eslint`, and `next build` pass. CI is green.
- Mongo option from D3 documented in `docs/known-issues.md`/README.

### M1 — Auth and tenant isolation (~2.5h) · depends on: M0
**Scope:** sign up, sign in, sign out, `GET /auth/me`, session middleware, CSRF for cookie-authenticated mutations, `users` collection, onboarding form (niche, goals, posting constraints, tone/language, connect-vs-import preference), protected routes (web) + `current_user` dependency (api), `OwnerScopedRepository` base, `DELETE /users/me` (cascades over owned collections), audit records.
**Acceptance:** an integration test proves **User A cannot read or write User B's records** via any route. Unauthenticated requests get 401. Onboarding persists. Account deletion removes owned data.

### M2 — Instagram connection / import (~3h MVP; M2b +3–5h) · depends on: M1
**M2a (MVP):** documented CSV/JSON import schema for the creator's own media + media insights + aggregate audience stats. Validation report: schema, dates, numeric ranges, duplicate IDs, missing fields. Ownership/consent checkbox. Records tagged `source: user_import`. **Synthetic demo creator** loader, tagged `is_synthetic: true`, with a persistent "SYNTHETIC DEMO DATA" banner. `instagram_accounts` connection-state model and status endpoint.
**M2b (stretch):** official Meta OAuth (Instagram Login vs Facebook Login decided from *current* docs, recorded in `docs/api-permissions.md`), state/CSRF, encrypted tokens, incremental idempotent sync job, disconnect.
**Acceptance:** importing a valid file creates scoped records and shows coverage. Invalid files return a precise error report. The demo creator loads and is visibly labeled. Live OAuth either works for an authorized tester account or the blocker is documented.

### M3 — Creator intelligence (~3h) · depends on: M2
**Scope:** deterministic Python aggregates (per-format/per-category medians, posting-time distributions, denominators, observation windows, sample-size warnings) as `derived`. LLM classification of topics/formats/hooks/voice as `inferred`, with supporting media IDs. `creator_profiles` versioned. Dashboard sections.
**Acceptance:** every insight shows its sample size, date range, supporting media IDs, and tier. No causal wording (a test checks the template phrases). Unit tests cover the aggregates, including the sparse-data case.

### M4 — Audience-grounded personas (~2.5h) · depends on: M3
**Scope:** `audience_profiles` from imported/API aggregate stats with field-level source and as-of time. Persona generator using observed stats + creator profile. Schema: `observed_evidence`, `inferred_interests`, `likely_motivations`, `content_preferences`, `unknowns`, `confidence`, `data_coverage`, `freshness`, `status: grounded|provisional`. User edits/feedback. Regenerate endpoint.
**Acceptance:** every `observed_evidence` entry maps to a stored stat (validator rejects anything else). With no audience data, the status is `provisional` and the UI explains the basis. A test asserts no segment-to-specific-Reel claims.

### M5 — Trends (MVP fallback ~1h; M5b +3h) · depends on: M1
**M5a:** `TrendSource` interface, `trends` collection with full provenance fields, "unavailable" state wired through to the UI and scoring.
**M5b:** one verified, documented source adapter with recency windows and niche relevance.
**Acceptance:** every displayed trend has a real source URL and timestamp, or the UI shows *trends unavailable*. Nothing is generated from model memory.

### M6 — Content Opportunity Engine (~3h) · depends on: M3, M4, M5a
**Scope:** `scoring/cos_v1.py` pure function + tests (bounds, missing data per D10, rounding, reproducibility). LLM proposes candidate ideas with evidence-linked subscore rationales. Python computes each component's normalized score from defined inputs and the weighted total. Filters (format, effort, persona, recency). Save to planner.
**Acceptance:** scoring unit tests pass. Each idea shows four components, their explanations, missing-data flags, and the "relative heuristic, not virality probability" label. Saved ideas persist per owner.

### M7 — Video processing (~5h) · depends on: M1
**Scope:** signed upload URL (D5), validation (magic bytes/MIME/size/duration via ffprobe), `jobs` lifecycle `queued→processing→completed|failed|cancelled` with progress, RQ worker pipeline: ffprobe → PySceneDetect frame sampling → audio extraction → transcription (D6) → [OCR flag, D8] → Gemini structured analysis (D7) → validated persistence. Timeouts, bounded retries, idempotency key, cleanup/retention of intermediate files.
**Acceptance:** a **real sample Reel** (user-supplied or a license-clear clip) produces a stored analysis with timestamped findings (hook, pacing, clarity, legibility, audio/transcript alignment, CTA, accessibility, confusion risks). The UI polls real progress. A malformed upload is rejected. A missing API key produces a clear `failed: provider_unavailable`. Attention risk is labeled as an estimate.

### M8 — Optimization + persona simulation (~3.5h) · depends on: M4, M7
**Scope:** persona reaction simulator (per-persona reactions, questions, strong/confusing moments with grounded timestamps, disagreement surfaced, labeled SIMULATED). Prioritized edit list (severity, rationale, hypothesized effect, alternatives). Hook rewrites, CTA options, on-screen text fixes, accessibility checks. **Captions in exactly four styles: formal, sarcastic, humorous-tech, humorous-non-tech**, editable and regeneratable. Hashtags split into `source_backed` and `relevance_suggestion`. Saved versions + before/after.
**Acceptance:** all outputs are schema-validated, timestamps ≤ duration, and the four styles are enforced by an enum. "Simulated" labels are present (tested). The chosen caption saves to the planner.

### M9 — Experiments and planner (planner ~1.5h MVP; experiments M9b +2.5h) · depends on: M6, M8
**M9a:** `content_plans` CRUD, statuses `idea|draft|ready|scheduled|published|archived` (`published` only set from a real action or explicit manual confirmation), list + simple calendar view.
**M9b:** A/B experiments with hypothesis, variants, simulated vs observed result fields kept separate, and no significance claims on small n.
**Acceptance:** planner data persists per owner, and status labels reflect real actions. Experiments keep simulated and observed results distinct.

### M10 — Tool-using AI strategist (~4h, post-MVP) · depends on: M3–M9
**Scope:** typed read tools (profile, audience, trends, opportunities, analyses, experiments, planner) + write tools (planner create/update) requiring a server-side approval token. `agent_runs` audit. Groq GPT-OSS function calling (verify first).
**Acceptance:** the agent calls real scoped tools, writes block until approved, and a prompt-injection fixture cannot trigger a write.

### M11 — Publishing and feedback learning (~4h+, post-MVP) · depends on: M2b, M9
**Scope:** publish preview → explicit approval of the exact media, caption, and account → official API if scopes allow it, otherwise a manual handoff/export. Performance sync. Comparison of hypotheses with outcomes, calibrating without rewriting the original predictions. `feedback`, `publishing_records`.
**Acceptance:** nothing is published without approval, blocked permissions are disclosed, and the manual handoff works.

### M12 — Launch readiness (~3h for the hackathon pass) · depends on: the MVP set
**Scope:** deploy (D13), env/secrets setup, seeded demo creator, `docs/demo-runbook.md`, accessibility/security pass, Playwright e2e of the principal journey on synthetic fixtures, README setup.
**Acceptance:** the demo can be repeated from the documented setup on a fresh environment. The e2e passes. There is a fallback if any external API is down.

---

## 4. Implementation order (hackathon)

1. M0 → 2. M1 → 3. M2a → 4. M3 → 5. M4 → 6. M5a → 7. M6 → 8. **first deploy (partial M12)** → 9. M7 → 10. M8 → 11. M9a → 12. M12 final → *(if time)* M5b, M2b, M9b, M10, M11.

M7 could start in parallel with M3–M6 on a team, but this is a solo build, so it stays sequential. If M7 is at risk by T+20h, ship M7 without OCR/scene detection (fixed-interval frame sampling) and document the gap.

## 5. External dependencies to verify (spec §14)

| Item | Needed by | Status |
|---|---|---|
| MongoDB Atlas free cluster URI (or local `mongod`) | M0 | **Needed from user** |
| Gemini API key + current Flash model ID, video/image limits, structured output, free quota | M3/M7 | Unverified |
| Groq API key + Whisper and GPT-OSS model availability, tool calling | M7/M10 | Unverified |
| Meta developer app, Instagram professional test account, Login type, scopes, App Review limits | M2b/M11 | Unverified. Likely restricted to app-role testers without App Review |
| Trend source with permitted access (YouTube Data API key, Google Trends API access) | M5b | Unverified |
| Hosting for API + worker + Redis (Vultr = paid → approval) | M12 | **Decision needed** |
| Vercel account | M12 | Needed from user |
| Sample Reel(s) the user has rights to | M7 | **Needed from user** |

## 6. Risks

| Risk | Impact | Mitigation |
|---|---|---|
| Meta App Review/permissions unavailable during the hackathon | No live IG data | M2a import + labeled synthetic demo (spec-sanctioned) |
| Video pipeline latency (transcription, Gemini) | Slow demo | Groq Whisper; cap the Reel at ≤90s; bounded frame count; show real progress; pre-processed demo analysis stored from a real earlier run (labeled with its run time) |
| Free-tier quota exhaustion | Feature fails live | Cache analyses; explicit `provider_unavailable` UX; rehearse with stored real results |
| No local Mongo/Docker in dev container | Slower M0 | Atlas M0 free cluster |
| Heavy deps (PaddleOCR, torch) | Build time, image size | Deferred behind flags (D8) |
| Solo time budget | Incomplete slice | Cut lines in §1; post-MVP milestones stay *planned* |
