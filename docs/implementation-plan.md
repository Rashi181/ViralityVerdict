# Verdict implementation plan

## Status and proposed architecture

M0 Foundation is approved and checkpointed. M1–M12 remain planned only.

### Approved architecture

Use the specified monorepo: `apps/web` (Next.js App Router + TypeScript), `apps/api` (FastAPI + Pydantic v2), `apps/worker` (RQ worker), and `packages/contracts` (generated OpenAPI client/types). MongoDB holds tenant-owned documents and job state; Redis is queue/cache only; S3-compatible storage holds private uploads. The frontend calls versioned API endpoints through typed domain hooks, never embeds backend rules in visual components. Provider adapters isolate Meta, Gemini, Groq, transcription, OCR, trend, and storage integrations.

This is an approved implementation direction, not a scope change. The short demo path is a full vertical slice through an explicitly labeled local/synthetic creator import, deterministic intelligence/personas/opportunities, private draft upload plus real local extraction, provider-backed or clearly unavailable analysis, four caption styles, and planner persistence. Meta publishing, live trend access, and production deployment remain roadmap features with honest fallbacks when credentials or approval are absent.

## MVP critical path

`M0 → M1 → M2 manual import/demo fallback → M3 → M4 → M6 → M7 → M8 → M9 → M12 demo`.

M5 can run in parallel only after source authorization is verified. M10 and M11 stay in scope but are post-demo stretch unless the vertical slice is reliable. No feature is removed or represented as implemented before its acceptance tests pass.

## Milestones

| Milestone | Exact components | Dependencies | Acceptance criteria | Testing |
| --- | --- | --- | --- | --- |
| M0 Foundation | pnpm workspace; `apps/web`; `apps/api`; `apps/worker`; contracts; environment templates; Docker/local services; health/ready; CI | Node, Python, MongoDB, Redis availability | Web shows a real API health response; no secrets committed | pytest health test; web lint/typecheck/build; API contract smoke test |
| M1 Auth and isolation | auth/session adapter; onboarding; users; auth dependency; owner-scoped repository base; protected routes | M0; auth provider decision | Two test users cannot read/write each other's objects | API cross-tenant denial tests; session/route E2E |
| M2 Connection/import | Meta OAuth adapter/status/sync/disconnect; CSRF state; CSV/JSON import validator; demo fixtures | M1; Meta app or manual schema | Authorized import works, or Meta block is disclosed and manual import works; data origin is labeled | import schema/date/range/duplicate tests; OAuth-state mocks; E2E fixture import |
| M3 Creator intelligence | media/insights repositories; deterministic aggregates; semantic-classification adapter; profile service/dashboard | M2 | Insights name media IDs, denominators, dates, source tiers, and limitations | aggregate and sparse-data unit tests; mocked semantic output validation |
| M4 Audience personas | audience ingestion; persona schema/service; observed/inferred split; provisional state and UI | M2, M3; accessible aggregate stats | Every persona cites actual aggregate evidence or says provisional; no unsupported cross-tabs | grounding/provenance tests; unavailable-data E2E |
| M5 Trends | documented `TrendSource` adapters; freshness rules; attribution store/UI; unavailable/evergreen fallback | M1; approved sources/keys | Every displayed trend has source URL and timestamps; no source means unavailable, not invented | source-parser mocks; stale-source and fallback tests |
| M6 Opportunities | opportunity generator; versioned pure score module; rationale/evidence; filters/save | M3–M5 | Python calculates `0.35/0.30/0.20/0.15` score; components bounded 0–100; missing data reduces confidence | score boundary/rounding/reproducibility tests; persistence/API tests |
| M7 Video processing | presigned/local upload flow; MIME/signature/duration validation; RQ jobs; FFmpeg; scene extraction; transcription/OCR adapters; private references | M1; Redis, storage, FFmpeg; provider credentials optional | Real sample upload reaches an honest terminal job state and stores evidence-linked extraction | malformed/oversize/ownership/job retry/idempotency tests; worker integration test |
| M8 Optimization | structured analysis; persona simulator; timestamp validator; edit suggestions; hooks; exactly four caption styles; version compare | M4, M7 | Findings are timestamp-grounded when possible; reactions say simulated; captions offer formal, sarcastic, humorous-tech, humorous-non-tech | schema/timestamp/label tests; component and E2E tests |
| M9 Experiments/planner | experiment and plan repositories/routes; calendar/list UI; statuses; before/after versions | M1, M6, M8 | Items persist per owner and simulated/observed results remain distinct | CRUD/authz tests; planner E2E |
| M10 Agent | typed read tools; server-side scoping; run/audit records; write preview/confirmation endpoints | M1, M3–M9; reasoning provider | Agent invokes real scoped tools; planner writes require confirmation | tool-schema/prompt-injection/authz/approval tests |
| M11 Publishing/learning | publish eligibility checker; preview/approval/audit; Meta publisher; manual export/handoff; later metric sync | M2; current Meta approval/scopes | No API publish without exact approval; unavailable permissions show manual handoff; observed metrics remain observed | approval/token/error/idempotency tests; mock provider integration |
| M12 Launch readiness | deployment config; accessibility/security review; fixture demo; runbook; observability | Working M0–M9 slice; approved hosting credentials | Repeatable demo, disclosed fallbacks, and documented setup/verification | production builds; Playwright path; accessibility scan; security regression |

## Feature completeness matrix

All product surfaces in the specification are represented: landing/auth (M0–M1); dashboard (M3–M6/M9); intelligence (M3); personas (M4); sourced trends (M5); opportunities (M6); upload and analysis (M7); simulator/optimizer (M8); experiments/planner (M9); typed strategist (M10); publishing/learning (M11); deployment/readiness (M12). Niche switching is explicitly excluded.

## External integration register

| Integration | Needed permission/credential | Demo risk and fallback | Cost control |
| --- | --- | --- | --- |
| Meta Instagram | Meta app, OAuth redirect URI, eligible professional test account, approved scopes/app review as required | High: current Instagram Login and Facebook Login differ; use validated creator CSV/JSON and synthetic labeled fixture when unavailable | No paid provisioning; rate-limit and incremental sync |
| Gemini | API key, verified supported model/video limits, structured-output capability | Medium: block analysis visibly if absent; retain real local extraction and never fabricate model output | Single-file caps, bounded retries, manual approval before paid tier |
| Groq | API key, current model availability | Medium: no strategist/model claims without key; validate schemas server-side | Low volume; use budget caps; do not assume strict structured output and tool use together |
| MongoDB | local URI or Atlas credentials/IP/network access | Low: local MongoDB for development; Atlas free tier only after approval | Prefer local/free tier; no automatic paid upgrade |
| Redis/RQ | local Redis or managed endpoint | Low: local service for demo; show unavailable queue state honestly | Local first |
| S3-compatible storage | bucket, restricted credentials, CORS, encryption/presign policy | Medium: private local-development storage adapter only if documented; no public links | Lifecycle deletion; short-lived URLs |
| FFmpeg/PySceneDetect/PaddleOCR/Whisper | local binaries/models or verified hosted service | Medium/high latency and platform installs; processing controls and terminal failure UX required | Limits, queues, local sample clips; no GPU spend without approval |
| Trend sources | documented permitted source/API keys and attribution terms | High: show source-unavailable/evergreen creator-history fallback | Avoid scraping and paid feeds unless approved |
| Hosting | Vercel/Vultr credentials, domain/redirect URIs, secrets | Medium: local repeatable demo before hosting | Do not provision or enable overages without approval |

## Decisions required before M1

1. Choose the initial authentication approach (recommended: Auth.js/NextAuth-compatible web session with FastAPI JWT verification) and whether local Docker services are acceptable.
2. Confirm whether development may use local MongoDB/Redis and filesystem-backed private storage adapters until cloud credentials are supplied.

## Completion protocol

At each milestone: branch, state scope/files/dependencies/blockers, implement only that milestone, run its tests, record actual outcomes in status/test/checkpoint/issue docs, provide manual steps, then stop for approval. No commit, push, merge, paid provisioning, or external account mutation without explicit approval.

## M0 checkpoint: approved

Scope: credential-free monorepo foundation, versioned API health/readiness endpoints, modular web health panel, environment placeholders, API smoke tests, and CI baseline. MongoDB and Redis are not initialized in M0: the service exposes liveness/readiness only, while M1+ introduce dependencies through tested adapters. The user manually verified the milestone; regression checks pass.

## Active milestone: M1

Scope: MongoDB user repository, Argon2 password hashing, signed HttpOnly sessions, sign-up/sign-in/sign-out/current-user APIs, owner-scoped onboarding, route-level UI flows, and cross-user denial tests. M1 does not use an external authentication provider or cloud credentials. The local MongoDB verification path is `compose.yaml`; the Docker daemon must be running. Acceptance requires User B to receive 403 when requesting User A and to receive no User A onboarding record.
