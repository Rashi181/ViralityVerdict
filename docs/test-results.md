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

## M2 Connection/import — 2026-11-13

| Check | Result |
| --- | --- |
| JSON/demo and CSV import tests | Pass: imports are owner-scoped; synthetic imports are labeled; valid CSV is retained as `user_import` |
| Full regression | Pass: 6 API tests, lint, typecheck, and production build passed; one existing third-party warning remains |
| Meta OAuth | Skipped: credentials and app configuration are intentionally absent; UI/API report `not_configured` |

## M3 Creator intelligence — 2026-11-13

| Check | Result |
| --- | --- |
| Owner-scoped summary test | Pass: imported media produces sample size, deterministic formats/caption openings, derived metrics, evidence IDs, and sparse-data limitations |
| Duplicate demo regression | Pass: two imports of the same `media_id` count once in Creator Intelligence; source imports remain retained for auditability |
| Full regression | Pass: 7 API tests, lint, typecheck, and production build passed; one existing third-party FastAPI/Starlette TestClient deprecation warning remains |

## M4 Audience personas — 2026-11-13

| Check | Result |
| --- | --- |
| Provisional fallback test | Pass: no aggregate audience evidence produces a low-confidence provisional persona with empty observed evidence and explicit unknowns |
| Evidence, feedback, and owner-isolation test | Pass: authorized aggregate evidence and feedback persist for one owner; a second owner sees no evidence and remains provisional |
| Full regression | Pass: 9 API tests, lint, typecheck, and production build passed; one existing third-party FastAPI/Starlette TestClient deprecation warning remains |

## M5 Trend intelligence — 2026-11-13

| Check | Result |
| --- | --- |
| Source-unavailable fallback | Pass: no source returns an explicit unavailable state with no claimed current trend |
| Provenance, freshness, and owner isolation | Pass: imported source URL and timestamps persist, freshness is calculated, and another owner cannot read the signal |
| Full regression | Pass: 11 API tests, lint, typecheck, and production build passed; one existing third-party FastAPI/Starlette TestClient deprecation warning remains |

## M6 Opportunities — 2026-11-13

| Check | Result |
| --- | --- |
| Deterministic scoring and ownership | Pass: 80/60/50/90 inputs calculate to 69.5 using the versioned formula; missing source reduces confidence; second owner cannot read the saved opportunity |
| Full regression | Pass: 12 API tests, lint, typecheck, and production build passed; one existing third-party FastAPI/Starlette TestClient deprecation warning remains |

## M7 Video processing — 2026-11-14

| Check | Result |
| --- | --- |
| Real FFmpeg metadata path | Pass: generated 1-second 320×240 MP4 uploaded privately and reached `completed` with measured duration/resolution |
| Full regression | Pass: 13 API tests, lint, typecheck, and production build passed; one existing third-party FastAPI/Starlette TestClient deprecation warning remains |

## M8 Optimization — 2026-11-14

| Check | Result |
| --- | --- |
| Caption-style contract | Pass: exactly formal, sarcastic, humorous-tech, and humorous-non-tech variants are returned |
| Safety fallback | Pass: persona reactions remain empty and timestamped findings are withheld without evidence-backed media analysis |
| Full regression | Pass: 14 API tests, lint, typecheck, and production build passed |

## M9 Planner — 2026-11-14

| Check | Result |
| --- | --- |
| Owner-scoped planning | Pass: one owner can save/list a scheduled plan while a second owner sees no items |
| Full regression | Pass: 15 API tests, lint, typecheck, and production build passed |

## M10 Strategist — 2026-11-14

| Check | Result |
| --- | --- |
| Scoped read-tool contract | Pass: authenticated user receives their own tool counts and an explicit no-model-result limitation |
| Full regression | Pass: 16 API tests, lint, typecheck, and production build passed |

## M11 Publishing — 2026-11-14

| Check | Result |
| --- | --- |
| Manual-handoff safety | Pass: no Meta config returns ineligible/manual-handoff status and explicitly says nothing was published |
| Full regression | Pass: 17 API tests, lint, typecheck, and production build passed |

## M12 Launch readiness — 2026-11-14

| Check | Command | Result |
| --- | --- | --- |
| API/security regression | `pnpm test:api` | Pass: 19 tests passed, including configured-origin CORS, standard security headers, and secure-session-cookie behavior. One existing third-party FastAPI/Starlette TestClient deprecation warning remains. |
| Web lint and typecheck | `pnpm lint && pnpm typecheck` | Pass |
| Web production build | `pnpm build` | Pass: Next.js 16.4.6 generated `/`, `/sign-in`, `/sign-up`, and `/onboarding`. |
| Playwright / automated accessibility scan | Not configured | Skipped, not passed. Manual keyboard verification remains required. |

## M13 Guided workspace and Caption & Hashtag Studio — 2026-11-14

| Check | Command | Result |
| --- | --- | --- |
| API contract regression | `pnpm test:api` | Pass: 19 tests passed. Caption Studio returns general caption structures and creator-provided-keyword hashtag labels; it does not claim those tags are trending. One existing third-party FastAPI/Starlette TestClient deprecation warning remains. |
| Web lint and typecheck | `pnpm lint && pnpm typecheck` | Pass |
| Web production build | `pnpm build` | Pass: Next.js generated the 14 focused routes, including dashboard, connect, insights, ideas, analyze, studio, planner, strategist, and publish. |
| Synthetic-import removal regression | Pass: `pnpm test:api && pnpm lint && pnpm typecheck && pnpm build` | 19 API tests passed, including a 404 assertion for the removed endpoint; lint, typecheck, and 14-page production build passed. |
| Final navigation/usability build | `pnpm lint && pnpm typecheck && pnpm build` | Pass: compact workspace headings and pre-import sign-in guidance compiled into the same 14-page production build. |

## M14 Reel-analysis foundation — 2026-11-14

| Check | Command | Result |
| --- | --- | --- |
| Private video evidence / analysis contract | `pnpm test:api` | Pass: 19 tests. A real generated MP4 produced measured metadata and an owner-scoped `awaiting_ai_analysis` response with no score or fabricated attention/persona result. One existing third-party FastAPI/Starlette TestClient deprecation warning remains. |
| Web verification | `pnpm lint && pnpm typecheck && pnpm build` | Pass: Reel Readiness UI compiled into the Analyze Reel page; production build generated 14 routes. |
| Generated Next output cleanup | Removed four stale duplicate `.next/types/* 2.ts` files | Pass: generated artifacts only; source code and user data untouched. |
| Hybrid frame sampling | `pnpm test:api && pnpm lint && pnpm typecheck && pnpm build` | Pass: FFmpeg samples the first 5 seconds every 0.5 seconds, the remaining body every 3 seconds, and up to 12 detected scene changes; all 19 API tests, lint, typecheck, and the 14-page production build passed. |

## M15 Read-only Instagram safety foundation — 2026-11-14

| Check | Command | Result |
| --- | --- | --- |
| Safety policy, encrypted vault, disconnect, and tenant isolation | `pnpm test:api` | Pass: 20 tests. The policy permits only `instagram_business_basic` and GET; a publishing scope and POST method are rejected; Fernet ciphertext differs from the raw token; owner disconnect/audit is isolated and does not expose the raw token. One existing third-party FastAPI/Starlette TestClient deprecation warning remains. |
| Dependency lock / full web regression | `uv lock --project apps/api && pnpm lint && pnpm typecheck && pnpm build` | Pass: `cryptography` 45.0.7 is locked; lint, typecheck, and 14-page production build passed. |
| Live Meta OAuth and remote revocation | No credentials or approved Meta app configuration | Skipped, not passed. OAuth remains disabled. |

## M18 Provider-backed strategic Reel analysis — 2026-11-15

| Check | Command | Result |
| --- | --- | --- |
| Private video / fake provider analysis | `pnpm test:api` | Pass: 23 tests. A generated private MP4 is analyzed only through a fake adapter; result findings persist per owner and another owner receives 404. No real provider request or key is used by this automated test. |
| Web lint, typecheck, and build | `pnpm lint && pnpm typecheck && pnpm build` | Pass: the final production build generated 15 application routes. |
| Diff safety | `git diff --check` | Pass |
| Real Gemini analysis | Creator-provided `GEMINI_API_KEY` and a creator-owned draft | Blocked: provider returned `RESOURCE_EXHAUSTED` because the selected Gemini project has no prepaid credit. No result was saved. |
| Real Groq strategic-frame analysis | Valid `GROQ_API_KEY`, `VERDICT_REEL_ANALYSIS_PROVIDER=groq`, and a newly uploaded creator-owned draft | Pending manual verification; Groq only receives up to three local strategic stills, not the whole video or audio. |

## Public-to-workspace navigation — 2026-11-15

| Check | Command | Result |
| --- | --- | --- |
| Landing, authentication, onboarding, workspace navigation | `pnpm lint && pnpm typecheck && pnpm build && git diff --check` | Pass: public actions preserve a safe requested destination, new accounts proceed to onboarding then dashboard, and the workspace exposes Home and Sign out. |

## M19 Workspace clarity and responsive density — 2026-11-15

| Check | Command | Result |
| --- | --- | --- |
| API regression | `pnpm test:api` | Pass: 23 API tests passed. Existing owner isolation, import validation, and safety-policy coverage remains intact. |
| Web regression | `pnpm lint && pnpm typecheck && pnpm build && git diff --check` | Pass: lint and typecheck passed; Next.js built all 15 routes; the working-tree diff has no whitespace errors. The focused Creator intelligence UI compiles against the existing creator/audience contracts, and the immediate ink-bloom theme toggle plus compact horizontal Limelight-inspired five-item navigation build cleanly. |
| Desktop visual review | In-app browser accessibility-tree review | Pass for structure: dashboard loaded with the full workspace header, connection card, and creator summary. Final subjective desktop/mobile visual review remains with the user. |

## M16 Interactive landing experience — 2026-11-14

| Check | Command | Result |
| --- | --- | --- |
| Web lint and typecheck | `pnpm lint && pnpm typecheck` | Pass |
| Landing-route production build | `pnpm build` | Pass: Next.js 16.4.6 generated `/` plus all 13 existing product routes after the hero, overview, and lanyard components were added. |
| Theme and landing regression | `pnpm lint && pnpm typecheck && pnpm build && git diff --check` | Pass: the full-viewport landing layout, floating landing control, startup-race protection, WebGL ink renderer with 2D canvas fallback, and all 14 routes compile cleanly. Four stale `.next/types/* 2.ts` generated files were removed before typecheck; no source files were removed. |
| Ink and tunnel readability refinement | `pnpm lint && pnpm typecheck && pnpm build && git diff --check` | Pass: the WebGL spill now has a slower 2.35-second animation, broader noise and 28 leading droplets; tunnel cards are larger, closer to square, and use larger high-contrast labels. Visual fidelity remains pending user verification. |
| Persona and workflow landing surfaces | `pnpm lint && pnpm typecheck && pnpm build && git diff --check` | Pass: the three-visible-card persona carousel and interactive six-stage creator-workflow orbit compile with the existing landing route and all product routes. Visual/readability verification remains pending user review. |
| Auth visual redesign and contract regression | `pnpm lint && pnpm typecheck && pnpm build && git diff --check` | Pass: `/sign-in` and `/sign-up` compile with the guided branded form layout while retaining the existing auth endpoints, field names, redirect behavior, validation, and error handling. Manual submission verification remains pending. |
| Reel feedback-board regression | `pnpm lint && pnpm typecheck && pnpm build && git diff --check` | Pass: `/analyze` compiles with owner-scoped video analysis, existing audience-persona and trend reads, and clear unavailable states. No attention, persona, or trend claim is rendered if the underlying authorized evidence is absent. Manual upload/inspect verification remains pending. |
| Local hero imagery | `pnpm lint && pnpm typecheck && pnpm build && git diff --check` | Pass: the 3D tunnel now references nine locally packaged creator-supplied images, with no external 21st.dev card image URL. |
| Hero return-to-top recovery | `pnpm lint && pnpm typecheck && pnpm build && git diff --check` | Pass: returning the document scroll position to the top resets the tunnel from its final hidden frame to its opening frame, preventing a blank hero after exploring the landing page. Manual browser verification remains pending. |
| Full functional regression after visual work | `pnpm test:api && pnpm lint && pnpm typecheck && pnpm build && git diff --check` | Pass: 20 API tests passed, including tenant isolation, imports, audience/persona evidence handling, opportunities, captions, planning, manual-publish gating, video evidence, and Instagram safety policy; web lint, typecheck, and all 14 product routes built successfully. One existing third-party FastAPI/Starlette TestClient deprecation warning remains. |
| M17 OAuth and first-history-sync regression | `pnpm test:api && pnpm lint && pnpm typecheck && pnpm build && git diff --check`; post-live-scope correction: `uv run --directory apps/api pytest tests/test_instagram_safety.py && pnpm typecheck && git diff --check` | Pass: 21 API tests passed in the full regression; after correcting the requested Facebook Login scopes, 2 focused API tests and TypeScript typecheck passed. A fake Meta provider verifies a single-use OAuth state, code exchange, encrypted per-owner token storage, owner-scoped first media sync, and no cross-owner sync. The first live Meta attempt was rejected before consent because the app had not enabled the required permission group; no account access was granted. One existing third-party FastAPI/Starlette TestClient deprecation warning remains. |
| Manual interaction/accessibility check | Pending user verification | Not yet run. Verify that the floating control remains in the top-right while scrolling; it switches both directions and persists after refresh; then verify desktop pointer parallax, wheel/trackpad motion, product-section readability, Log in/Sign up routes, lanyard badge flip via click/Enter/Escape, animated illustrations, mobile layout, and operating-system reduced-motion behavior. |

## M20 Isolated synthetic demonstration dataset — 2026-11-15

| Check | Command | Result |
| --- | --- | --- |
| Fixture raw-data/provenance/tenant isolation | `uv run --directory apps/api pytest tests/test_demo_fixture.py tests/test_audience.py tests/test_creator.py` | Pass: 5 tests. The fixture loader ignores supplied personas, classifications, recommendation cases, and interest estimates; it produces only tenant-scoped synthetic records and deterministic hypotheses. |
| Full API/web regression | Pending | Not run yet for M20. |

## xAI Grok strategic-frame configuration — 2026-11-15

| Check | Command | Result |
| --- | --- | --- |
| xAI-provider regression | `uv run --directory apps/api pytest tests/test_videos.py tests/test_demo_fixture.py` | Pass: 4 tests. The new xAI selection preserves the existing private-upload and no-write boundary. No real xAI request or API key was used by automated tests. |
| Web typecheck | `pnpm --dir apps/web typecheck && git diff --check` | Pass. A stale generated duplicate Next type file was removed before the check; application source was unchanged by that cleanup. |
| xAI descriptive-response normalization | `uv run --directory apps/api pytest tests/test_xai_reel.py tests/test_videos.py tests/test_demo_fixture.py` | Pass: 5 tests. Grok's descriptive focus labels (for example, “Hook promise”) are mapped into Verdict's fixed evidence taxonomy, and a single limitation string is stored as a list without inventing any findings or recommendation content. |
