# Checkpoints

## Current checkpoint

- Date: 2026-11-14
- Branch: `feat/real-instagram-prep`
- Commit: M15 implementation checkpoint `a71a9c6`
- Milestone: M15 Read-only Instagram safety foundation
- Repository state: M15 manually verified and approved; automated regression checks pass
- Approval status: approved by user after manual verification
- Commits/pushes by Codex: M0–M14 checkpointed on their respective feature branches; M15 implementation checkpoint `a71a9c6` is ready to push

### M0 — Foundation

- Branch and base commit: `feat/m0-foundation`, based on `5af463e`
- Scope / changed files: workspace/configuration, Next.js web, FastAPI API, API tests, CI workflow, and checkpoint documentation
- Dependencies and credentials: local Node/pnpm/Python/uv only; no product credentials used. MongoDB is not installed/configured and intentionally is not treated as ready.
- Acceptance criteria: API health response is rendered through the modular web health panel; automated API tests/lint/typecheck/production build pass.
- Automated results: passed; exact commands/results in `docs/test-results.md`.
- Manual verification steps and result: servers were started on `127.0.0.1:8000` and `127.0.0.1:3000`; API returned HTTP 200 health JSON and web returned HTTP 200. User manually verified and approved the milestone.
- Known limitations and recovery: no persistence, auth, database, queue, or credentials are implemented; all belong to later milestones.
- User approval: approved
- Commit/tag (only after approval): `feat: establish M0 foundation` (checkpointed and pushed)

## Milestone checkpoint template

### M1 — Auth and isolation

- Branch and base commit: `feat/m1-auth-isolation`, based on `67ce73b`
- Scope / changed files: FastAPI auth/config/repository/service/schema/routes; Mongo Compose configuration; Next.js auth/onboarding UI; tests; M1 status docs
- Dependencies and credentials: local MongoDB via Docker Compose and a locally generated `VERDICT_SESSION_SECRET`; no external credentials used
- Acceptance criteria: sign-up/sign-in/sign-out and onboarding work; User B cannot read User A or their onboarding data
- Automated results: API tests passed (4); web lint, typecheck, and production build passed
- Manual verification steps and result: user completed the documented local setup and verified the sign-up flow
- Known limitations and recovery: start Docker Desktop then use the documented local environment values; no cloud/production auth provider is configured
- User approval: approved
- Commit/tag (only after approval): checkpoint commit pending as `feat: establish M1 auth and isolation`

### M2 — Connection/import

- Branch and base commit: `feat/m2-connection-import`, based on `609be16`
- Scope: user-authorized JSON/CSV import, demo fixture, import ownership, and Meta status
- Acceptance: imports validate/persist under the user, synthetic data is labeled, and unavailable Meta credentials are disclosed
- Automated results: 6 API tests; web lint/typecheck/production build passed
- Manual verification: user-approved
- User approval: approved
- Commit/tag: checkpoint commit pending as `feat: establish M2 connection and import`

### M3 — Creator intelligence

- Branch and base commit: `feat/m3-creator-intelligence`, based on `51921a3`
- Scope / changed files: owner-scoped imported-history summary, deterministic aggregates, evidence IDs, dates, formats, observed hashtags/caption openings, and UI.
- Dependencies and credentials: M2 imports; no credential required for deterministic analysis. Semantic model integration is intentionally unavailable.
- Acceptance criteria: each insight is based on imported records, reports sample/evidence/date context, treats duplicate media IDs once, and does not claim semantic AI analysis without a configured provider.
- Automated results (pass/fail/skip with commands): pass — `uv run --directory apps/api pytest && pnpm lint && pnpm typecheck && pnpm build`; 7 API tests, lint, typecheck, and production build passed.
- Manual verification steps and result: user verified the onboarding Creator Intelligence card, including repeated demo-import deduplication, on 2026-11-13.
- Known limitations and recovery: no authorized Gemini/model provider is configured, so semantic topics and brand voice remain explicitly unavailable; see `docs/known-issues.md`.
- User approval: approved
- Commit/tag (only after approval): `feat: add creator intelligence`

### M4 — Audience personas

- Branch and base commit: `feat/m4-audience-personas`, based on `1d4f5b5`
- Scope / changed files: owner-scoped aggregate audience evidence repository/API, observed and provisional persona service, persisted user feedback, onboarding UI, and API tests.
- Dependencies and credentials: M1 authentication and M2/M3 creator-history context. No credential is needed for manual authorized aggregate imports; Meta audience-insight permissions remain unavailable.
- Acceptance criteria: personas expose only field-level imported aggregate evidence with source/as-of time; no evidence produces a visibly provisional persona; no demographic-to-content-performance cross-tab claim is made; feedback is owner-scoped and persisted.
- Automated results (pass/fail/skip with commands): pass — `uv run --directory apps/api pytest && pnpm lint && pnpm typecheck && pnpm build`; 9 API tests, lint, typecheck, and production build passed. One existing third-party FastAPI/Starlette TestClient deprecation warning remains.
- Manual verification steps and result: user verified the observed aggregate-evidence persona, provenance labels, explicit unknowns, and persisted feedback on 2026-11-13.
- Known limitations and recovery: live Meta audience statistics are unavailable pending authorized credentials/scopes. Use the clearly labeled manual aggregate import only for creator-authorized data.
- User approval: approved
- Commit/tag (only after approval): `feat: add audience personas`

### M5 — Trend intelligence

- Branch and base commit: `feat/m5-trend-intelligence`, based on `76d2523`
- Scope / changed files: owner-scoped source-observation persistence/API, freshness evaluation, attributed trend UI, source-unavailable fallback, and tests.
- Dependencies and credentials: no source credential used. Google Trends API is currently alpha/application-based; M5 only accepts creator-authorized, attributable source observations until an approved provider integration exists.
- Acceptance criteria: every displayed signal contains source URL, observed/retrieved timestamps, geography/niche relevance, and freshness; no source yields an explicit unavailable state rather than invented trends.
- Automated results: pass — `uv run --directory apps/api pytest && pnpm lint && pnpm typecheck && pnpm build`; 11 API tests, lint, typecheck, and production build passed. One existing third-party FastAPI/Starlette TestClient deprecation warning remains.
- Manual verification steps and result: user verified the unavailable fallback and an attributed source observation on 2026-11-13.
- Known limitations and recovery: no live provider connector is configured. Import a documented, authorized observation with its original source URL; do not treat it as an Instagram performance claim.
- User approval: approved
- Commit/tag (only after approval): `feat: add trend intelligence`

### M6 — Opportunities

- Branch and base commit: `feat/m6-opportunities`, based on `976595a`
- Scope: deterministic score service, opportunity persistence/API, evidence/reduced-confidence fields, and read UI.
- Acceptance: Python calculates `0.35 × audience_fit + 0.30 × trend_relevance + 0.20 × novelty + 0.15 × feasibility`; components are bounded 0–100, evidence is required, and missing components reduce confidence.
- Automated results: pass — 12 API tests, lint, typecheck, and production build.
- Manual verification: user verified the deterministic opportunity score and reduced-confidence handling on 2026-11-14.
- User approval: approved
- Commit/tag: `feat: add opportunity scoring`

### M7 — Video processing

- Branch and base commit: `feat/m7-video-processing`, based on `7ce2641`
- Scope: private local development upload, MIME/signature/size validation, owner-scoped persisted jobs, and real FFmpeg metadata extraction.
- Acceptance: an authorized MP4/WebM up to 25 MB is never given a public URL and reaches an honest terminal state with real metadata or an explicit failure.
- Automated results: pass — 13 API tests, lint, typecheck, and production build.
- Manual verification: user verified private draft upload and the honest local FFmpeg processing result on 2026-11-14.
- Limitations: only FFmpeg metadata runs. RQ/Redis workers, scene extraction, transcript, OCR, model analysis, and object storage are not configured; no result is fabricated.
- User approval: approved
- Commit/tag: `feat: add private video processing`

### M8 — Optimization

- Branch: `feat/m8-optimization`, based on `dfbcd98`
- Scope: user-text-grounded local caption variants and safe optimizer UI.
- Acceptance: exactly four caption styles exist; simulated reactions and timestamped findings are not fabricated without grounding.
- Automated results: pass — 14 API tests, lint, typecheck, production build.
- Manual verification: user verified all four caption styles and the safe limitation labels on 2026-11-14.
- User approval: approved
- Commit/tag: `feat: add safe reel optimization`

### M9 — Planner

- Branch: `feat/m9-planner-experiments`, based on `7671d61`
- Scope: owner-scoped content plan persistence, statuses, planned dates, and UI.
- Acceptance: status means planning state only and never implies publishing; records are tenant-isolated.
- Automated results: pass — 15 API tests, lint, typecheck, production build.
- Manual verification: user verified saving a scheduled planner item and the non-publishing status disclosure on 2026-11-14.
- User approval: approved
- Commit/tag: `feat: add content planner`

### M10 — Strategist

- Branch: `feat/m10-strategist`, based on `fa687bb`
- Scope: authenticated read-tool inventory and provider-unavailable strategist state.
- Acceptance: tools return only authenticated user data; no model/tool-use response or planner write is falsely claimed.
- Automated results: pass — 16 API tests, lint, typecheck, production build.
- Manual verification: user verified authenticated read-tool counts and provider-unavailable disclosure on 2026-11-14.
- User approval: approved
- Commit/tag: `feat: add scoped strategist tools`

### M11 — Publishing

- Branch: `feat/m11-publishing-learning`, based on `d977e83`
- Scope: publishing eligibility gate and manual handoff.
- Acceptance: no API publishing claim without verified Meta status; creator approval/manual steps are explicit.
- Automated results: pass — 17 API tests, lint, typecheck, production build.
- Manual verification: user verified manual-handoff-required status and the no-publish disclosure on 2026-11-14.
- User approval: approved
- Commit/tag: `feat: add publishing eligibility gate`

### M12 — Launch readiness

- Branch and base commit: `feat/real-instagram-prep`, based on `8e1d32a`
- Scope / changed files: deployment-safe cookie/origin configuration, API security response headers, a security regression suite, keyboard skip links/focus indicators, and `docs/demo-runbook.md`.
- Dependencies and credentials: no external credentials or deployment access used. Real Meta OAuth, durable cloud services, and production monitoring remain separate blocked work.
- Acceptance criteria: local demo path is documented; API security headers and configured-origin CORS are tested; HTTPS deployments can opt into secure session cookies; UI has a keyboard skip link; no live Instagram capability is claimed.
- Automated results (pass/fail/skip with commands): pass — `pnpm test:api && pnpm lint && pnpm typecheck && pnpm build`; 19 API tests, lint, typecheck, and production build passed. One existing third-party FastAPI/Starlette TestClient deprecation warning remains. Playwright, a deployed environment, and an automated accessibility scanner were not configured, so they were not run.
- Manual verification: user approved M12 on 2026-11-14.
- Known limitations and recovery: read `docs/demo-runbook.md`; deployment and Meta OAuth must remain disabled until their credentials and review are ready.
- User approval: approved
- Commit/tag: `dfdfe6e feat: add launch readiness safeguards`

### M13 — Guided workspace and Caption & Hashtag Studio

- Branch and base commit: `feat/real-instagram-prep`, based on `dfdfe6e`
- Scope / changed files: shared modular workspace navigation, focused routes for each product stage, simplified onboarding, Caption & Hashtag Studio API/UI, removal of exposed synthetic imports, pre-import sign-in guidance, compact workspace headings, product-spec update, and regression test update.
- Dependencies and credentials: existing authenticated optimizer; no model or Instagram credential used. The deterministic fallback uses only creator-provided words and explicitly does not interpret a tone request or claim tags are trending.
- Acceptance criteria: clear guided page flow; three general caption structures rather than fixed tone variants; optional refinement prompt; hashtag source/explanation shown; only creator-authorized manual imports are exposed; no live/provider result is invented.
- Automated results: pass — `pnpm test:api && pnpm lint && pnpm typecheck && pnpm build`; 19 API tests, lint, typecheck, and the 14-page production build passed. One existing third-party FastAPI/Starlette TestClient deprecation warning remains.
- Manual verification: user approved M13 on 2026-11-14.
- User approval: approved
- Commit/tag: `ae5ec86 feat: add guided creator workspace`

### M14 — Reel-analysis foundation

- Branch and base commit: `feat/real-instagram-prep`, based on `e9cb2d2`
- Scope / changed files: owner-scoped private hybrid frame sampling after upload (dense opening, regular body, scene changes), analysis-evidence schema/endpoint, Reel Readiness UI, and regression coverage.
- Dependencies and credentials: existing private local upload and FFmpeg. No Gemini, transcript/OCR provider, audience persona evidence, storage, or background worker credential is used.
- Acceptance criteria: completed private uploads return measured duration/resolution, hybrid sampling strategy, and private sampled-frame count only; analysis returns an explicit pending state with no score, attention-risk claim, or persona reaction until supported inputs/providers exist.
- Automated results: pass — `pnpm test:api && pnpm lint && pnpm typecheck && pnpm build`; 19 API tests, lint, typecheck, and 14-page production build passed. One existing third-party FastAPI/Starlette TestClient deprecation warning remains.
- Manual verification: user approved M14 on 2026-11-14.
- User approval: approved
- Commit/tag: `eb39602 feat: add hybrid reel evidence sampling`

### M15 — Read-only Instagram safety foundation

- Branch and base commit: `feat/real-instagram-prep`, based on `7c50063`
- Scope / changed files: permanent Meta read-only policy, encrypted token-vault service, connection/audit repositories, local disconnect/audit APIs, connection safety UI, and deterministic caption-keyword evidence.
- Dependencies and credentials: `cryptography` 45.0.7 was added for Fernet encryption. No Meta app secret, user password, access token, or live API call was used.
- Acceptance criteria: `instagram_business_basic` is the sole allowed scope; publishing/comment/message/write scopes and non-GET methods are rejected; encrypted tokens never appear in API audit output; a user can disconnect only their own stored connection; caption keywords are derived from authorized history separately from hashtags.
- Automated results: pass — `uv lock --project apps/api && pnpm test:api && pnpm lint && pnpm typecheck && pnpm build`; 20 API tests, lint, typecheck, and 14-page production build passed. One existing third-party FastAPI/Starlette TestClient deprecation warning remains.
- Manual verification: user approved M15 on 2026-11-14.
- Current blocker: live OAuth state/CSRF callback, remote token revocation, real sync, and deletion choices for future API-synced records must be completed and tested only after the approved Meta configuration exists. OAuth remains disabled.
- User approval: approved
- Commit/tag: `a71a9c6 feat: add read-only instagram safety controls`
