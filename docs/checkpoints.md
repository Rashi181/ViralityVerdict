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

### Mx — name

- Branch and base commit:
- Scope / changed files:
- Dependencies and credentials:
- Acceptance criteria:
- Automated results (pass/fail/skip with commands):
- Manual verification steps and result:
- Known limitations and recovery:
- User approval:
- Commit/tag (only after approval):
