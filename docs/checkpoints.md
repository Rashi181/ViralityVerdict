# Checkpoints

## Current checkpoint

- Date: 2026-11-13
- Branch: `feat/m0-foundation`
- Commit: `5af463e`
- Milestone: M0 Foundation
- Repository state: M0 implementation verified and committed locally; push pending
- Approval status: approved by user after manual verification
- Commits/pushes by Codex: none

### M0 — Foundation

- Branch and base commit: `feat/m0-foundation`, based on `5af463e`
- Scope / changed files: workspace/configuration, Next.js web, FastAPI API, API tests, CI workflow, and checkpoint documentation
- Dependencies and credentials: local Node/pnpm/Python/uv only; no product credentials used. MongoDB is not installed/configured and intentionally is not treated as ready.
- Acceptance criteria: API health response is rendered through the modular web health panel; automated API tests/lint/typecheck/production build pass.
- Automated results: passed; exact commands/results in `docs/test-results.md`.
- Manual verification steps and result: servers were started on `127.0.0.1:8000` and `127.0.0.1:3000`; API returned HTTP 200 health JSON and web returned HTTP 200. User manually verified and approved the milestone.
- Known limitations and recovery: no persistence, auth, database, queue, or credentials are implemented; all belong to later milestones.
- User approval: approved
- Commit/tag (only after approval): `feat: establish M0 foundation` (checkpointed; push pending)

## Milestone checkpoint template

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
