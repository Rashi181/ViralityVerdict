# Feature status

Last audited: 2026-11-13. Source: repository commit `5af463e`.

| Area | Status | Evidence / next gate |
| --- | --- | --- |
| Repository governance | Complete | `PROJECT_SPEC.md` and `AGENTS.md` read in full |
| M0 Foundation | Complete and checkpointed | Versioned FastAPI health/readiness endpoints, Next.js health panel, environment template, API tests, and CI baseline manually verified by user and regression-tested on `feat/m0-foundation` |
| M1 Auth and isolation | Approved; checkpoint commit pending | Password/session APIs, MongoDB repository, onboarding UI, and cross-user authorization tests were manually verified on `feat/m1-auth-isolation` |
| M2 Connection/import | Approved; checkpoint commit pending | Owner-scoped JSON/CSV imports, synthetic demo import, and honest Meta status were manually verified on `feat/m2-connection-import` |
| M3 Creator intelligence | Approved; checkpointed | Deterministic imported-history summary, evidence IDs, sparse-data limitations, and UI manually verified on `feat/m3-creator-intelligence` |
| M4 Audience personas | Approved; checkpointed | Owner-scoped aggregate-audience evidence import, observed/provisional persona states, persisted feedback, and onboarding UI manually verified on `feat/m4-audience-personas` |
| M5 Trend intelligence | Approved; checkpointed | Owner-scoped attributed trend observations, freshness labels, and a source-unavailable fallback manually verified on `feat/m5-trend-intelligence` |
| M6 Opportunities | Approved; checkpointed | Deterministic weighted score, owner-scoped opportunity persistence/API, evidence fields, reduced-confidence state, and UI manually verified on `feat/m6-opportunities` |
| M7 Video processing | Approved; checkpointed | Private local upload, signature/size validation, owner-scoped persisted jobs, real FFmpeg metadata extraction, and honest limitations manually verified on `feat/m7-video-processing` |
| M8 Optimization | Approved; checkpointed | User-text-grounded local caption variants, explicit safe limitations, and optimizer UI manually verified on `feat/m8-optimization` |
| M9 Planner | Approved; checkpointed | Owner-scoped plan persistence, explicit planning statuses, and planner UI manually verified on `feat/m9-planner-experiments` |
| M10–M12 application code | Not started | Planned in the approved implementation plan |
| Architecture plan | Approved | `docs/implementation-plan.md` |
| Product feature coverage | Planned | M0–M12 matrix covers every specified surface; no niche-switch feature included |
| External integrations | Unverified / blocked pending credentials | See implementation plan and known issues |
| M0 test suite | Passed with one third-party deprecation warning | API tests, web lint, TypeScript typecheck, and production build ran; details in `docs/test-results.md` |
| Demo data | Not present | Must be clearly synthetic when created |

Do not change a status to complete without a code location, test result, and manual verification record.
