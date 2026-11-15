# Verdict implementation plan

## Status and proposed architecture

M0 Foundation is approved and checkpointed. M1–M12 remain planned only.

### Approved architecture

Use the specified monorepo: `apps/web` (Next.js App Router + TypeScript), `apps/api` (FastAPI + Pydantic v2), `apps/worker` (RQ worker), and `packages/contracts` (generated OpenAPI client/types). MongoDB holds tenant-owned documents and job state; Redis is queue/cache only; S3-compatible storage holds private uploads. The frontend calls versioned API endpoints through typed domain hooks, never embeds backend rules in visual components. Provider adapters isolate Meta, Gemini, Groq, transcription, OCR, trend, and storage integrations.

This is an approved implementation direction, not a scope change. The short path is a full vertical slice through a creator-authorized manual import, deterministic intelligence/personas/opportunities, private draft upload plus real local extraction, provider-backed or clearly unavailable analysis, general caption recommendations, and planner persistence. Meta publishing, live trend access, and production deployment remain roadmap features with honest fallbacks when credentials or approval are absent.

## MVP critical path

`M0 → M1 → M2 authorized manual import fallback → M3 → M4 → M6 → M7 → M8 → M9 → M12`.

M5 can run in parallel only after source authorization is verified. M10 and M11 stay in scope but are post-demo stretch unless the vertical slice is reliable. No feature is removed or represented as implemented before its acceptance tests pass.

## Milestones

| Milestone | Exact components | Dependencies | Acceptance criteria | Testing |
| --- | --- | --- | --- | --- |
| M0 Foundation | pnpm workspace; `apps/web`; `apps/api`; `apps/worker`; contracts; environment templates; Docker/local services; health/ready; CI | Node, Python, MongoDB, Redis availability | Web shows a real API health response; no secrets committed | pytest health test; web lint/typecheck/build; API contract smoke test |
| M1 Auth and isolation | auth/session adapter; onboarding; users; auth dependency; owner-scoped repository base; protected routes | M0; auth provider decision | Two test users cannot read/write each other's objects | API cross-tenant denial tests; session/route E2E |
| M2 Connection/import | Meta OAuth adapter/status/sync/disconnect; CSRF state; CSV/JSON import validator | M1; Meta app or manual schema | Authorized import works, or Meta block is disclosed and manual import works; data origin is labeled | import schema/date/range/duplicate tests; OAuth-state mocks; E2E authorized-import path |
| M3 Creator intelligence | media/insights repositories; deterministic aggregates; semantic-classification adapter; profile service/dashboard | M2 | Insights name media IDs, denominators, dates, source tiers, and limitations | aggregate and sparse-data unit tests; mocked semantic output validation |
| M4 Audience personas | audience ingestion; persona schema/service; observed/inferred split; provisional state and UI | M2, M3; accessible aggregate stats | Every persona cites actual aggregate evidence or says provisional; no unsupported cross-tabs | grounding/provenance tests; unavailable-data E2E. **Implemented; awaiting manual verification on `feat/m4-audience-personas`.** |
| M5 Trends | documented `TrendSource` adapters; freshness rules; attribution store/UI; unavailable/evergreen fallback | M1; approved sources/keys | Every displayed trend has source URL and timestamps; no source means unavailable, not invented | source-parser mocks; stale-source and fallback tests. **Implemented; awaiting manual verification on `feat/m5-trend-intelligence`.** |
| M6 Opportunities | opportunity generator; versioned pure score module; rationale/evidence; filters/save | M3–M5 | Python calculates `0.35/0.30/0.20/0.15` score; components bounded 0–100; missing data reduces confidence | score boundary/rounding/reproducibility tests; persistence/API tests. **Implemented; awaiting manual verification on `feat/m6-opportunities`.** |
| M7 Video processing | presigned/local upload flow; MIME/signature/duration validation; RQ jobs; FFmpeg; scene extraction; transcription/OCR adapters; private references | M1; Redis, storage, FFmpeg; provider credentials optional | Real sample upload reaches an honest terminal job state and stores evidence-linked extraction | malformed/oversize/ownership/job retry/idempotency tests; worker integration test. **Implemented; awaiting manual verification on `feat/m7-video-processing`.** |
| M8 Optimization | structured analysis; persona simulator; timestamp validator; edit suggestions; hooks; exactly four caption styles; version compare | M4, M7 | Findings are timestamp-grounded when possible; reactions say simulated; captions offer formal, sarcastic, humorous-tech, humorous-non-tech | schema/timestamp/label tests; component and E2E tests. **Implemented; awaiting manual verification on `feat/m8-optimization`.** |
| M9 Experiments/planner | experiment and plan repositories/routes; calendar/list UI; statuses; before/after versions | M1, M6, M8 | Items persist per owner and simulated/observed results remain distinct | CRUD/authz tests; planner E2E |
| M10 Agent | typed read tools; server-side scoping; run/audit records; write preview/confirmation endpoints | M1, M3–M9; reasoning provider | Agent invokes real scoped tools; planner writes require confirmation | tool-schema/prompt-injection/authz/approval tests |
| M11 Publishing/learning | publish eligibility checker; preview/approval/audit; Meta publisher; manual export/handoff; later metric sync | M2; current Meta approval/scopes | No API publish without exact approval; unavailable permissions show manual handoff; observed metrics remain observed | approval/token/error/idempotency tests; mock provider integration |
| M12 Launch readiness | deployment config; accessibility/security review; authorized-import runbook; observability | Working M0–M9 slice; approved hosting credentials | Repeatable workflow, disclosed fallbacks, and documented setup/verification | production builds; Playwright path; accessibility scan; security regression. **Implemented on `feat/real-instagram-prep`; awaiting manual verification.** |

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

## Post-M12 product evolution

| Milestone | Exact components | Dependencies | Acceptance criteria | Testing |
| --- | --- | --- | --- | --- |
| M13 Guided workspace and Caption & Hashtag Studio | Shared modular workspace shell; focused dashboard/connect/insights/ideas/analyze/studio/planner/strategist/publish routes; general caption recommendations; optional creator refinement prompt; source-labeled hashtag suggestions | M1 auth; M8 optimizer; no model credential required for deterministic fallback | A creator can follow a clear page-by-page path; Studio does not force tone categories; suggestions identify their evidence/source and do not claim unsourced tags are trending | API contract test; lint/typecheck/production build; manual navigation and Studio check. **Implemented on `feat/real-instagram-prep`; awaiting manual verification.** |
| M14 Reel-analysis foundation | Private FFmpeg hybrid frame sampling (dense opening, regular body, scene-change frames); owner-scoped analysis endpoint; Reel Readiness UI; explicit unavailable/pending analysis states | M7 private upload; FFmpeg; no provider credential required for extraction | A completed private video exposes only measured metadata/frame-sampling evidence; no readiness score, attention risk, or persona reaction is fabricated without Gemini/transcript/OCR/persona inputs | Private upload/analysis API test; lint/typecheck/production build. **Implemented on `feat/real-instagram-prep`; awaiting manual verification.** |
| M15 Read-only Instagram safety foundation | Permanent read-only scope/method policy; encrypted token vault; tenant-scoped connection/audit repositories; local disconnect; safety UI; observed caption-keyword extraction | M1 auth; standards-based encryption library; no Meta credentials needed until OAuth enablement | Publishing/comment/message/write scopes and non-GET adapter methods are rejected; stored token ciphertext is not exposed; disconnect/audit are owner-scoped; creator intelligence shows observed words from captions separately from hashtags | Policy/vault/owner-isolation test; full regression. **Implemented on `feat/real-instagram-prep`; awaiting manual verification.** |
| M16 Interactive experience and visual system | Full-viewport isolated Framer Motion tunnel hero; local creator-supplied hero imagery; landing product overview/workflow/features/safety sections; polished three-card lanyard persona carousel; interactive six-stage workflow orbit; contact-form-inspired sign-in/sign-up surfaces; persistent light/dark theme with a click-originating WebGL ink spill; 3D card sequence, pointer parallax, wheel/trackpad interaction, animated illustrations, mobile sizing, and reduced-motion behavior | Existing Next.js landing and auth routes; `framer-motion`, `gsap`, and `html2canvas`; no API, account, or credential required | `/` clearly explains Verdict, routes returning/new creators to the correct access flows, renders landing-only simulated persona examples, uses the creator-supplied local hero image set, fills the viewport at desktop widths, offers a legible persona preview and explains the end-to-end workflow without claiming unavailable account data; auth keeps its API contracts while offering a guided, branded form; the selected light/dark preference persists; motion is reduced when the OS preference requests it | Web lint/typecheck/production build; manual desktop pointer/wheel/persona carousel/workflow stage/auth submission/ink persistence and mobile/reduced-motion verification. **Implemented; awaiting manual verification.** |
| M17 Official read-only Meta OAuth and first history sync | OAuth start/callback with CSRF state and redirect validation; Facebook Login configuration; encrypted per-owner token persistence; a GET-only Meta client; initial authorized profile/media import; connection status and error UI; local disconnect/audit records; regression and mocked-provider tests | A Meta app with Facebook Login for Business configured, a Professional Instagram test account linked to a Facebook Page, local App ID/Secret/encryption key, and no publishing/message/comment scopes | A creator can explicitly authorize the narrow read-only scope set through Meta, receive only a redacted connection status, sync only their own eligible observed media data, and disconnect. The client rejects every non-GET request and every publishing/message/comment scope. No token, password, or raw provider response appears in UI/audit/log output. Aggregate audience-insight mapping and documented remote revocation remain follow-on work. | OAuth state/redirect/error tests; scope/method negative tests; tenant-isolation/sync-mapping tests; full API/web regression; manual local test with the account owner. **Implemented; awaiting local Meta credential/manual verification.** |
| M18 Provider-backed strategic Reel analysis | Explicit creator-triggered provider analysis of one private draft; JSON-schema findings; hook-first/scene-change prompt; remote Gemini-file cleanup; owner-scoped persistence and feedback UI | M14 private video flow; Gemini or Groq key/model access; creator-owned test Reel | Gemini receives a private video only after the creator presses Analyze. The temporary Groq fallback receives no more than three locally extracted strategic stills. Neither path invents per-viewer stats, retention curves, or persona results. | Fake-provider success/owner-isolation tests; API/web regression; manual creator-key test. **Implemented; awaiting a real-key/manual verification.** |
| M19 Workspace clarity and responsive density | Full-width workspace content grid; consistent page header; user-facing Meta connection and safety flow; a minimal Creator intelligence page that shows only creator history and actually available audience evidence; removal of visible CSV/raw audience/raw trend import forms from the primary demo journey; human-facing private-upload/evidence wording | M13–M18 UI | Wide desktop screens use the available product canvas; the primary journey does not expose developer-style manual import/test forms, raw media IDs, speculative personas, or empty “none” lists; no API endpoints or authorization boundaries are removed. | API/web regression; desktop and mobile manual visual check. **Implemented; awaiting manual verification.** |

## M0 checkpoint: approved

Scope: credential-free monorepo foundation, versioned API health/readiness endpoints, modular web health panel, environment placeholders, API smoke tests, and CI baseline. MongoDB and Redis are not initialized in M0: the service exposes liveness/readiness only, while M1+ introduce dependencies through tested adapters. The user manually verified the milestone; regression checks pass.

## M1 checkpoint: approved

Scope: MongoDB user repository, Argon2 password hashing, signed HttpOnly sessions, sign-up/sign-in/sign-out/current-user APIs, owner-scoped onboarding, route-level UI flows, and cross-user denial tests. M1 does not use an external authentication provider or cloud credentials. The local MongoDB verification path is `compose.yaml`; the Docker daemon must be running. Acceptance requires User B to receive 403 when requesting User A and to receive no User A onboarding record.

## Active milestone: M2

Scope: authenticated JSON/CSV creator-data imports, duplicate/range/schema validation, owner-scoped persistence, explicit `user_import` provenance, a synthetic-only demo import, and Meta connection status. Meta OAuth and sync are deliberately unavailable until actual Meta configuration and permissions are supplied; the UI reports that state instead of simulating a connection.

## M20 checkpoint: isolated synthetic demonstration dataset

Scope: a judge-demo-only local fixture is available only when `VERDICT_DEMO_MODE=true` and `VERDICT_DEMO_FIXTURE_PATH` are configured. The loader uses raw posts, captions, keywords, hashtags, engagement metrics, and aggregate demographic facts. It explicitly ignores pre-authored personas, taxonomy, recommendation cases, and interest-affinity estimates. The same creator-summary and audience-hypothesis services consume the normalized data used by other ingestion sources.

Acceptance criteria: the fixture is not copied into the repository or enabled by default; it is tenant-scoped, visibly fictional/non-OAuth, and cannot expose a supplied persona or recommendation. Planning output separates stored evidence from hypotheses. Focused API coverage passes; full regression and manual local verification remain pending.
