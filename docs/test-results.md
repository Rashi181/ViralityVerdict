# Test Results

Actual results only. Each entry records the date, branch, commit, exact command, and verbatim pass/fail/skip counts. Never record expected results here.

## Standard commands (to be finalized in M0)

| Suite | Command (planned) |
|---|---|
| API unit + integration | `cd apps/api && uv run pytest` |
| API lint / types | `cd apps/api && uv run ruff check . && uv run mypy app` |
| Web types / lint / build | `cd apps/web && pnpm tsc --noEmit && pnpm lint && pnpm build` |
| Contracts drift | `pnpm contracts:check` |
| E2E | `pnpm --filter e2e playwright test --trace off` |

## Results log

| Date (UTC) | Branch @ commit | Suite | Result | Notes |
|---|---|---|---|---|
| 2026-11-14 | main (no commits) | — | Not run | No code exists yet |
