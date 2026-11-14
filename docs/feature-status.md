# Feature status

Last audited: 2026-11-14. Source: repository commit `eb39602`.

| Area | Status | Evidence / next gate |
| --- | --- | --- |
| Repository governance | Complete | `PROJECT_SPEC.md` and `AGENTS.md` read in full |
| M0 Foundation | Complete and checkpointed | Versioned FastAPI health/readiness endpoints, Next.js health panel, environment template, API tests, and CI baseline manually verified by user and regression-tested on `feat/m0-foundation` |
| M1 Auth and isolation | Approved; checkpoint commit pending | Password/session APIs, MongoDB repository, onboarding UI, and cross-user authorization tests were manually verified on `feat/m1-auth-isolation` |
| M2 Connection/import | Approved; checkpointed | Owner-scoped creator-authorized JSON/CSV imports and honest Meta status are retained; the exposed synthetic demo was removed from the active product branch |
| M3 Creator intelligence | Approved; checkpointed | Deterministic imported-history summary, evidence IDs, sparse-data limitations, and UI manually verified on `feat/m3-creator-intelligence` |
| M4 Audience personas | Approved; checkpointed | Owner-scoped aggregate-audience evidence import, observed/provisional persona states, persisted feedback, and onboarding UI manually verified on `feat/m4-audience-personas` |
| M5 Trend intelligence | Approved; checkpointed | Owner-scoped attributed trend observations, freshness labels, and a source-unavailable fallback manually verified on `feat/m5-trend-intelligence` |
| M6 Opportunities | Approved; checkpointed | Deterministic weighted score, owner-scoped opportunity persistence/API, evidence fields, reduced-confidence state, and UI manually verified on `feat/m6-opportunities` |
| M7 Video processing | Approved; checkpointed | Private local upload, signature/size validation, owner-scoped persisted jobs, real FFmpeg metadata extraction, and honest limitations manually verified on `feat/m7-video-processing` |
| M8 Optimization | Approved; checkpointed | User-text-grounded local caption variants, explicit safe limitations, and optimizer UI manually verified on `feat/m8-optimization` |
| M9 Planner | Approved; checkpointed | Owner-scoped plan persistence, explicit planning statuses, and planner UI manually verified on `feat/m9-planner-experiments` |
| M10 Strategist | Approved; checkpointed | Authenticated read-tool inventory and explicit provider-unavailable state manually verified on `feat/m10-strategist` |
| M11 Publishing | Approved; checkpointed | Eligibility gate, explicit manual handoff, and no-publish disclosure manually verified on `feat/m11-publishing-learning` |
| M12 Launch readiness | Approved; checkpointed | Security headers, production cookie/origin configuration, accessibility baseline, repeatable demo runbook, and security regression tests manually approved and committed on `feat/real-instagram-prep` |
| M13 Guided workspace and Caption & Hashtag Studio | Approved; checkpointed | Focused product pages, shared navigation shell, general caption options, free-text refinement prompt, source-labeled deterministic hashtag suggestions, and no exposed synthetic imports on `feat/real-instagram-prep` |
| M14 Reel-analysis foundation | Approved; checkpointed | Private hybrid FFmpeg frame sampling, owner-scoped evidence endpoint, and Reel Readiness UI with honest AI-analysis-pending state on `feat/real-instagram-prep` |
| Architecture plan | Approved | `docs/implementation-plan.md` |
| Product feature coverage | Planned | M0–M12 matrix covers every specified surface; no niche-switch feature included |
| External integrations | Unverified / blocked pending credentials | See implementation plan and known issues |
| M0 test suite | Passed with one third-party deprecation warning | API tests, web lint, TypeScript typecheck, and production build ran; details in `docs/test-results.md` |
| Synthetic creator import | Removed from product | Only creator-authorized manual import is exposed; private automated test data does not appear in the UI or API |

Do not change a status to complete without a code location, test result, and manual verification record.
