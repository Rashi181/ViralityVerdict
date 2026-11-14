# Known issues and blockers

| ID | Severity | Status | Issue / impact | Resolution or honest fallback |
| --- | --- | --- | --- | --- |
| KI-M3-01 | Low | Open | Semantic topic/subtopic and brand-voice classification needs an authorized model provider; no provider credential has been supplied. | M3 shows only deterministic imported formats, hashtags, and caption openings and explicitly labels semantic classification unavailable. |
| KI-M4-01 | Medium | Open | Current Meta audience-insight scopes and account eligibility are unavailable, so Verdict cannot claim API-observed audience statistics. | M4 accepts creator-authorized aggregate imports with field-level provenance and otherwise renders a provisional persona with explicit unknowns. |
| KI-M5-01 | Medium | Open | No approved live trend-source credential is configured; Google Trends API access is currently alpha/application-based. | M5 displays no trend until the creator imports an attributable, authorized source observation; otherwise it shows an explicit unavailable fallback. |
| KI-M7-01 | Medium | Open | M7 has local FFmpeg metadata only; private object storage, RQ worker, transcription, OCR, and model providers are not configured. | Uploaded drafts receive real metadata or an explicit failure; unsupported analysis stages are clearly unavailable and never fabricated. |
| KI-M8-01 | Medium | Open | No evidence-grounded transcript, scene analysis, or model provider is configured for detailed Reel optimization. | M8 produces only deterministic variants from user-supplied text and explicitly withholds persona reactions and timestamped findings. |
| EXT-001 | High | Open | Meta app, OAuth settings, account eligibility, current scopes, and App Review status are unknown | Validate current official documentation and credentials; manual authorized import and labeled demo fixture |
| EXT-002 | High | Open | No Gemini, Groq, storage, MongoDB, Redis, hosting, or trend-source credentials are in the repository | Do not claim provider results; use adapters and explicit unavailable states |
| EXT-003 | Medium | Resolved | Local toolchain was previously unconfirmed | Node 24, pnpm 10, Python 3.12, uv, Docker, and Redis were verified during M0 |
| EXT-004 | Medium | Open | Video processing dependencies and CPU/GPU latency are unverified | Test bounded sample pipeline; queue work and surface failure states |
| EXT-005 | Medium | Open | Current provider pricing/limits may change and paid access is not authorized | Re-check before implementation; retain free/local path and budget caps |
| DEV-001 | Low | Open | MongoDB daemon is not installed locally | M0 intentionally does not initialize persistence; establish the documented local or free-tier database path before M1 |
| DEV-002 | Low | Open | FastAPI test client emitted a third-party deprecation warning | Track upstream FastAPI/Starlette/httpx compatibility; tests pass and no product behavior is affected |
| DEV-003 | Medium | Open | Docker Compose is installed but the Docker daemon is not running, preventing local MongoDB verification | Start Docker Desktop, then run `docker compose up -d mongodb` before M1 manual verification |
| EXT-006 | High | Open | Meta app credentials, OAuth configuration, permissions, and app review are not supplied | M2 exposes `not_configured` status and supports authorized import/demo fallback; do not claim a live connection |
| M12-001 | Medium | Open | No deployed HTTPS environment, production persistence/storage/queue, monitoring, Playwright suite, or automated accessibility scan is configured. | M12 provides local runbook and security regression only; perform a staging deployment and the documented deployment checklist before any real account connection. |
| GOV-001 | Low | Resolved | Initial workspace was empty | Main branch pulled; specification and instructions now present |
