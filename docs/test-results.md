# Test results

## Pre-M0 audit — 2026-11-13

| Check | Command | Result |
| --- | --- | --- |
| Git state | `git status --short --branch` | Pass: `main` tracks `origin/main`; no local changes before planning docs |
| Repository inventory | `rg --files -g '!node_modules' -g '!dist' -g '!build'` | Pass: only `PROJECT_SPEC.md` and `AGENTS.md` existed before these planning docs |
| Specification/instructions read | `sed -n '1,9999p' PROJECT_SPEC.md; sed -n '1,9999p' AGENTS.md` | Pass: read completely |
| Application tests | N/A | Skipped: no application code or test configuration exists |
| Build/lint/typecheck | N/A | Skipped: no package manifests or application code exists |

Future entries must state the exact command, environment, date, outcome, and relevant failure output. Skipped is not passed.

## M0 Foundation — 2026-11-13

| Check | Command | Result |
| --- | --- | --- |
| API tests | `uv run --directory apps/api pytest` | Pass: 2 tests passed. One third-party FastAPI/Starlette `TestClient` deprecation warning was emitted. |
| Web lint | `pnpm lint` | Pass |
| Web typecheck | `pnpm typecheck` | Pass |
| Web production build | `pnpm build` | Pass; Next.js 16.4.6 generated the `/` route successfully |
| API liveness | `curl --fail --silent http://127.0.0.1:8000/api/v1/health` | Pass: HTTP 200, `status=ok`, `service=verdict-api`, `version=0.1.0` |
| Web server response | `curl --fail --silent http://127.0.0.1:3000` | Pass: HTTP 200 and API connection panel markup present |
| User browser verification | N/A | Pending user approval |

Initial failures corrected during M0: pytest was launched from the repository root and could not import `app`; the script now runs from `apps/api`. ESLint 9 lacked a flat configuration; `apps/web/eslint.config.mjs` now provides it. The initial TypeScript library target did not satisfy Next declaration files; it now targets ES2024 with declaration checking skipped while Verdict source remains checked.

## M0 checkpoint regression — 2026-11-13

| Check | Command | Result |
| --- | --- | --- |
| Full M0 regression | `pnpm lint && pnpm test && pnpm build` | Pass: lint, TypeScript typecheck, 2 API tests, and Next.js production build all passed. The same third-party FastAPI/Starlette deprecation warning remains. |
| Secret-pattern review | `rg -n -i '(api[_-]?key|secret|token|password|private[_-]?key)' ...` | Pass: only empty `.env.example` placeholders and documentation/governance references found. |
| User manual verification | User-confirmed | Pass: M0 approved. |

## M1 Auth and isolation — 2026-11-13

| Check | Command | Result |
| --- | --- | --- |
| API tests | `uv run --directory apps/api pytest` | Pass: 4 tests passed, including sign-out and cross-user read/onboarding denial. One existing third-party warning remains. |
| Web lint/typecheck/build | `pnpm lint && pnpm typecheck && pnpm build` | Pass: all passed; pages `/sign-up`, `/sign-in`, and `/onboarding` built successfully. |
| Local MongoDB integration | `docker compose up -d mongodb && docker compose ps` | Blocked: Docker daemon was not running; no database container was created. |

The first M1 test run failed during collection because `Protocol` was imported from `collections.abc`; it was corrected to `typing.Protocol`. The rerun passed.

| Sign-up configuration/feedback regression | `uv sync --project apps/api --group dev && uv run --directory apps/api pytest && pnpm lint && pnpm typecheck && pnpm build` | Pass: local `.env` loading, localhost CORS support, and visible submit/error feedback added; 4 API tests and all web checks passed. |
