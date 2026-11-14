# Feature status

Last audited: 2026-11-13. Source: repository commit `5af463e`.

| Area | Status | Evidence / next gate |
| --- | --- | --- |
| Repository governance | Complete | `PROJECT_SPEC.md` and `AGENTS.md` read in full |
| M0 Foundation | Complete and checkpointed | Versioned FastAPI health/readiness endpoints, Next.js health panel, environment template, API tests, and CI baseline manually verified by user and regression-tested on `feat/m0-foundation` |
| M1 Auth and isolation | Approved; checkpoint commit pending | Password/session APIs, MongoDB repository, onboarding UI, and cross-user authorization tests were manually verified on `feat/m1-auth-isolation` |
| M2–M12 application code | Not started | Planned in the approved implementation plan |
| Architecture plan | Approved | `docs/implementation-plan.md` |
| Product feature coverage | Planned | M0–M12 matrix covers every specified surface; no niche-switch feature included |
| External integrations | Unverified / blocked pending credentials | See implementation plan and known issues |
| M0 test suite | Passed with one third-party deprecation warning | API tests, web lint, TypeScript typecheck, and production build ran; details in `docs/test-results.md` |
| Demo data | Not present | Must be clearly synthetic when created |

Do not change a status to complete without a code location, test result, and manual verification record.
