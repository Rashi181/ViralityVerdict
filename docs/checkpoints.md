# Checkpoints

## Current checkpoint

- Date: 2026-11-13
- Branch: `feat/m2-connection-import`
- Commit: based on M1 checkpoint `609be16`; M2 is uncommitted
- Milestone: M2 Connection/import
- Repository state: M2 implementation verified locally; checkpoint commit pending
- Approval status: approved by user after manual verification
- Commits/pushes by Codex: M0 and M1 pushed on their feature branches

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
