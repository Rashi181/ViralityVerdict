# Known issues and blockers

| ID | Severity | Status | Issue / impact | Resolution or honest fallback |
| --- | --- | --- | --- | --- |
| EXT-001 | High | Open | Meta app, OAuth settings, account eligibility, current scopes, and App Review status are unknown | Validate current official documentation and credentials; manual authorized import and labeled demo fixture |
| EXT-002 | High | Open | No Gemini, Groq, storage, MongoDB, Redis, hosting, or trend-source credentials are in the repository | Do not claim provider results; use adapters and explicit unavailable states |
| EXT-003 | Medium | Resolved | Local toolchain was previously unconfirmed | Node 24, pnpm 10, Python 3.12, uv, Docker, and Redis were verified during M0 |
| EXT-004 | Medium | Open | Video processing dependencies and CPU/GPU latency are unverified | Test bounded sample pipeline; queue work and surface failure states |
| EXT-005 | Medium | Open | Current provider pricing/limits may change and paid access is not authorized | Re-check before implementation; retain free/local path and budget caps |
| DEV-001 | Low | Open | MongoDB daemon is not installed locally | M0 intentionally does not initialize persistence; establish the documented local or free-tier database path before M1 |
| DEV-002 | Low | Open | FastAPI test client emitted a third-party deprecation warning | Track upstream FastAPI/Starlette/httpx compatibility; tests pass and no product behavior is affected |
| GOV-001 | Low | Resolved | Initial workspace was empty | Main branch pulled; specification and instructions now present |
