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

### M16 — Interactive landing experience

- Branch and base commit: `feat/real-instagram-prep`, based on M15 checkpoint `399caff`
- Scope / changed files: full-viewport `PerspectiveTunnelHero`, `LandingOverview`, `CreatorJourney`, polished three-visible-card `PersonaLanyardRail`, and persistent `ThemeProvider`/`ThemeToggle` client components; nine creator-supplied hero images stored locally under `apps/web/public/hero`; a viewport-fixed landing theme control with startup-race protection and a click-originating WebGL noise/droplet ink overlay; landing route/workspace-shell composition; scoped landing/theme CSS; and Framer Motion, GSAP, and html2canvas dependency locks.
- Dependencies and credentials: `framer-motion` was added; no backend, Meta, creator-data, or model credential was used.
- Acceptance criteria: the landing route explains Verdict's scope, capabilities, workflow, safety boundary, and access actions; it preserves the supplied reference components' 3D card corridor, pointer parallax, wheel/trackpad progression, card hover behavior, lanyard badge swing/flip, and minimal animated persona illustrations; the full-width hero fills the desktop viewport; the theme setting persists and uses a click-originating native View Transition with an irregular ink-spill contour, with an accessibility-safe immediate switch for reduced motion; examples remain clearly simulated; mobile behavior and sign-up/sign-in links work.
- Automated results: pass — `pnpm lint && pnpm typecheck && pnpm build && git diff --check`; lint and typecheck passed, and Next.js produced all 14 existing application routes. Returning to the document top now resets the tunnel from its final hidden frame to its opening frame, preventing a blank hero after exploration. Four stale duplicate files under `.next/types/` were removed before an earlier typecheck; these were generated artifacts, not source files.
- Manual verification: pending.
- Known limitations and recovery: the supplied creator images are now packaged locally, so the landing tunnel has no runtime dependency on 21st.dev art URLs. Confirm the creator owns or is authorized to use them before public deployment.
- User approval: pending.
- Commit/tag: pending approval.

### M17 — Official read-only Meta OAuth and first history sync

- Branch and base commit: `feat/real-instagram-prep`, following the uncommitted M16 visual work.
- Scope / changed files: CSRF-state-protected Facebook Login redirect/callback; encrypted, owner-scoped token persistence; a GET-only Meta client; initial authorized Professional-account media sync; connection/sync status UI; audit records; policy expansion for the needed read-only scopes; and fake-provider regression coverage.
- Dependencies and credentials: no App ID, App Secret, access token, or real account was used. The local implementation becomes connectable only after the owner inserts credentials into ignored `.env` and registers the exact callback URI.
- Acceptance criteria: the client may request only `instagram_basic`, `pages_read_engagement`, and `pages_show_list`; it rejects publishing, messages, comments, write methods, and cross-owner use. Tokens are encrypted/redacted. First sync stores only fields Meta returns. Aggregate demographic mapping, `instagram_manage_insights`, and remote provider revocation are explicitly deferred.
- Automated results: pass — `pnpm test:api && pnpm lint && pnpm typecheck && pnpm build && git diff --check`; 21 API tests, lint, typecheck, and the 14-route production build passed. One existing third-party FastAPI/Starlette TestClient deprecation warning remains.
- Manual verification: pending local Meta credential setup and account-owner consent. No live Meta operation has been attempted.
- User approval: approved to implement on 2026-11-14; awaiting manual verification/commit approval.
- Commit/tag: pending approval.

### M18 — Provider-backed strategic Reel analysis

- Scope / changed files: provider adapter, configured model/key settings, explicit owner-scoped analysis endpoint, JSON-schema-validated timestamped findings, remote Gemini-file deletion, persisted analysis output, and Reel Readiness UI action. Groq provides a temporary vision fallback over up to three locally extracted strategic stills.
- Safety boundary: no Meta write action, no public media URL, no per-viewer data, no retention curve, and no persona reaction unless separately grounded in current authorized aggregate audience data.
- Strategic review behavior: Gemini is prompted to inspect the opening and then sample sparse material changes; Groq is explicitly limited to an opening, hook-end, and one later/scene-change still. Neither path claims full frame-by-frame viewing when it has not occurred.
- Dependency / blocker: a valid provider key, remaining provider credit, and one creator-owned short Reel are required for a live test. API keys stay in ignored `.env`; they must never be pasted into chat or committed. Gemini's configured project returned credit exhaustion during the owner-controlled test; no Gemini result was saved.
- Automated results: pass — `pnpm test:api && pnpm lint && pnpm typecheck && pnpm build && git diff --check`; 23 API tests passed; web lint, typecheck, and the 15-route production build passed. Provider calls remain unverified until a user-controlled Groq request succeeds.
- Manual verification: pending.
- Commit/tag: pending user verification and approval.

### M20 — Isolated synthetic demonstration dataset

- Scope / changed files: environment-gated local fixture loader/API endpoints, `synthetic_demo` provenance, deterministic creator/audience synthesis, source-labeled UI, and fixture/owner-isolation tests.
- Safety boundary: the fixture stays outside the repository and is disabled by default. The loader does not read prebuilt personas, taxonomy, interest scores, or recommendations.
- Acceptance criteria: no output can present demo records as Meta/OAuth data; each owner sees only their own demo records; derived planning claims remain hypotheses.
- Automated results: focused API regression passed — 5 tests (`test_demo_fixture.py`, creator, audience). Full API/web regression and manual local verification remain pending.
- Persona synthesis update: raw aggregate age/location distributions now deterministically derive up to two visible planning lenses. The Reel feedback board can display those lenses alongside a real strategic finding as a simulated strategic check; it never claims that an individual viewer reacted.
- Commit/tag: pending user verification and approval.

### M19 — Workspace clarity and responsive density

- Scope / changed files: full-width workspace shell and content grid; immediate, persistent theme switch at the top-right; compact horizontal five-item Limelight-inspired core navigation; responsive two-column desktop composition for the Reel and audience surfaces; user-facing upload/evidence wording; a minimal Creator intelligence surface limited to observed creator history and available audience evidence; removal of Home, Planner, Strategist, and Publish & learn navigation controls plus CSV, raw aggregate-audience, raw trend-import, trend-feed, and persona-feedback forms from the primary workspace pages.
- Safety boundary: no fallback API, creator data, account setting, or external service was deleted or modified. The visible Meta connection and read-only safety disclosure remain.
- Acceptance criteria: wide screens no longer reserve a large unused right column; primary user flows use product-oriented labels rather than internal job/FFmpeg terms; manual authorized-import endpoints remain available for supported fallback use without being promoted in the demo UI.
- Automated results: pass — `pnpm test:api && pnpm lint && pnpm typecheck && pnpm build && git diff --check`; 23 API tests, web lint, typecheck, and the 15-route production build passed.
- Manual verification: pending user desktop/mobile visual check.
- Commit/tag: pending user verification and approval.
