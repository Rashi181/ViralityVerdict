# Verdict — Product & Engineering Specification

**Project:** Verdict  
**Tagline:** *Instagram tells creators what happened. Verdict tells them what to create next, why it fits their audience, and how to improve it before publishing.*  
**Context:** HackUMass XIV, November 13–15, 2026; solo-built hackathon MVP with a path to a real multi-tenant SaaS.  
**Document role:** Canonical product requirements and engineering constraints for Codex.  
**Status:** Product specification, **not** a claim that features are implemented or integrations are approved.

---

## 1. Mission and product boundary

Verdict is an AI-powered Instagram creator growth strategist and **pre-publication Reel optimization** platform. It connects authorized creator data, learns from historical performance and available current aggregate audience insights, researches recent relevant trends, recommends evidence-backed content opportunities, analyzes draft Reels, simulates likely persona reactions with explicit uncertainty, proposes improvements, supports controlled experiments and planning, and learns from later performance.

**End-to-end journey:** **Connect → Understand → Research → Recommend → Create → Optimize → Experiment → Publish (creator-approved) → Measure → Learn.**

Verdict is **not** a generic caption generator, follower surveillance product, engagement-bot, guaranteed virality predictor, or an Instagram scraper. It must not promise follower growth, impersonate audience members, invent platform metrics, or claim simulated feedback is actual viewer behavior.

**Explicit exclusion:** Do **not** implement niche switching, niche pivoting, or a niche-switch simulator. This feature was deliberately removed from scope.

### Target users

- Instagram creators with professional (Creator/Business) accounts who want actionable content strategy.
- Small creator teams or solo creators with limited analytics expertise.
- Users without API access who can legally and securely import their own authorized export or structured data, with appropriately reduced functionality.

### Primary value proposition

1. **Personalization:** Recommendations derive from the creator's own available content, audience, goals, and constraints.
2. **Evidence:** Separate platform-observed facts, inferred hypotheses, trend sources, and simulations.
3. **Actionability:** Timestamped Reel feedback, concrete hook alternatives, caption variants, and next-step plans.
4. **Closed loop:** Compare suggestions and experiments with later real performance where data is available.
5. **Trust:** Explainable scoring, explicit approvals, strong data isolation, and honest handling of missing data.

---

## 2. Product principles and non-negotiable rules

1. **No fabricated evidence.** Never invent audience demographics, views, retention curves, engagement counts, trends, API permissions, completed jobs, or test results.
2. **Provenance on every important claim.** Persist the source, timestamp, retrieval method, and confidence/limitations for insights and recommendations.
3. **Audience-grounded personas.** Generate personas from the creator's *currently available actual aggregate Instagram audience statistics* plus their historical content performance. Clearly label what is observed versus inferred. If data is unavailable, use clearly marked provisional personas, not pretend data.
4. **Privacy by design.** Use only data the creator is authorized to provide or access. Never scrape private follower profiles or infer individual follower identities.
5. **Creator control.** No autonomous publishing or account-changing actions without explicit, contextual approval.
6. **Explainability.** Opportunity scores are transparent heuristics, **not** virality probabilities.
7. **Useful failure states.** Missing permissions, sparse history, unavailable trends, failed model calls, and queued video jobs must have clear UX and recovery paths.
8. **Working software over breadth.** Implement a tested end-to-end slice before adding secondary capabilities; never quietly redefine the complete product as the MVP.
9. **Modular frontend.** Build a functional, testable interface now; the user will redesign/polish the frontend using separate tools later. Keep API contracts, data hooks, and business logic independent from visual components.
10. **Cost controls.** Favor free tiers and local development. Do not provision billable infrastructure, enable paid overages, or call costly APIs at scale without explicit user approval.

---

## 3. Product surfaces and user journeys

### 3.1 Landing and authentication

- Landing page communicates the product and distinguishes real analysis from simulated guidance.
- Sign up/sign in/sign out, session management, account settings, and data deletion.
- Authenticated application with route protection and tenant-scoped API access.
- Onboarding collects creator niche, content goals, posting constraints, preferred language/tone, and account connection/import preference.

### 3.2 Creator dashboard

- Connection and sync status, data coverage, last sync time, and permission limitations.
- Historical performance summaries and content-category comparisons with time windows and denominators.
- Current audience overview based on accessible aggregate data; data freshness clearly visible.
- Top content opportunities, latest analyses, saved drafts, experiments, and planned posts.
- Empty states and demo/sample-data mode must be conspicuously labeled.

### 3.3 Creator intelligence

- Analyze historical authorized Reels/posts, captions, hashtags, timestamps, and available aggregate Insights.
- Derive content topics/subtopics, recurring formats, posting patterns, brand voice, hooks, and historically successful content categories.
- Use deterministic Python statistics for numeric aggregates and Gemini for semantic classification/synthesis.
- Avoid causal claims from observational correlations. Adjust for sparse data and differing observation windows.
- Show supporting media IDs, sample sizes, dates, and confidence/limitations.

### 3.4 Current-audience-grounded personas

**Critical requirement:** Personas must not be generic fictional audience archetypes generated only from niche. Build them using the creator's *currently available, actual, aggregate Instagram audience statistics* (such as age bands, geographic distributions, and other fields **only where officially accessible**) together with historical content and performance. Available audience data varies by account type, permissions, eligibility, and API version.

Each persona must contain:
- Name/short label and intended strategic use, explicitly synthetic.
- `observed_evidence`: aggregate stats actually returned by authorized data sources, with field-level source and as-of time.
- `inferred_interests`, `likely_motivations`, `content_preferences`: hypotheses inferred from aggregate audience context and creator history.
- `unknowns`, `confidence`, `data_coverage`, and freshness.
- Suggested hooks, pacing considerations, and CTA preferences, presented as hypotheses.
- **Never** assert that a specific demographic segment watched or liked a specific Reel unless the source explicitly supports that cross-tabulation.

If audience insights are missing, unavailable, or too sparse: show a `provisional` status, state the basis (creator content + user-supplied goals), and avoid implying validation by real audience data. Allow user edits/feedback, and regenerate when fresh authorized stats arrive.

### 3.5 Recent, source-backed trend intelligence

- Retrieve recent niche-relevant topics, formats, search/interest signals, and hashtags from **authorized, documented sources**.
- Persist source URL/title, retrieval timestamp, publication/observation timestamp when available, geographic/niche relevance, and freshness window.
- Never invent current trending hashtags or claim real-time trends from model memory.
- Clearly distinguish sourced signals from AI-suggested creative interpretations.
- Gracefully degrade to historical inspiration or creator-specific evergreen opportunities when live trend sources are unavailable.
- Do not scrape Instagram or circumvent platform access restrictions.

### 3.6 Content Opportunity Engine

- Produce personalized Reel ideas with angle, hook, format, intended audience/persona, trend evidence, creator-history evidence, production feasibility, sample caption direction, and explanation.
- Deterministic scoring formula, inputs normalized to **0–100**:

  `Content Opportunity Score = 0.35 × audience_fit + 0.30 × trend_relevance + 0.20 × novelty + 0.15 × feasibility`

- Calculate final score in Python, not by asking an LLM to output an arbitrary number. Persist component scores, evidence, scoring version, and missing-data handling.
- Explain why each component earned its score. For missing components, use an explicit, documented fallback and reduced confidence; never silently assign certainty.
- Display as a **relative prioritization heuristic**, not probability of virality or guaranteed performance.
- Allow filtering by niche, content format, effort, recency, and persona; save promising ideas to planner.

### 3.7 Draft Reel upload and multimodal analysis

- Creator uploads a video through authenticated private upload flow (prefer presigned object-storage URLs).
- Validate file type, MIME/signature, file size, duration, and ownership. Set configurable limits.
- Process asynchronously with Redis/RQ and separate worker; job states `queued`, `processing`, `completed`, `failed`, `cancelled` where supported.
- Pipeline: media validation → FFmpeg metadata/extraction → representative frame/scene sampling (PySceneDetect) → audio extraction → Whisper transcription → OCR (PaddleOCR) where useful → Gemini multimodal interpretation → structured, schema-validated analysis → persistence.
- Model/provider calls must have timeouts, bounded retries, rate limits, idempotency, and clear failure messages. Use configurable provider/model IDs; verify availability before use.
- Return timestamped, evidence-linked findings: opening hook, pacing/scene transitions, clarity, narrative coherence, text legibility, audio/transcript alignment, CTA, accessibility, and potential viewer confusion.
- **Attention risk** is an AI estimate/hypothesis, not actual audience retention. Do not manufacture a retention curve or exact drop-off time.
- Never expose private media through public permanent URLs. Support retention and deletion policies.

### 3.8 Persona reaction simulator

- Evaluate a draft Reel against the creator's evidence-grounded personas.
- Show simulated reactions, likely questions, confusing moments, strong moments, and suggested revisions with timestamps where grounded by media analysis.
- Explain persona basis and uncertainty. Label every reaction **simulated**, not actual follower feedback.
- Surface disagreement across personas instead of fabricating consensus.
- Re-run when the Reel version changes; track model and input versions.

### 3.9 Reel optimizer

- Timestamped, prioritized edit suggestions with severity, rationale, expected *hypothesized* effect, and concrete alternatives.
- Multiple hook rewrites, CTA options, on-screen text improvements, pacing/structure suggestions, and accessibility checks (captions, readability, contrast where assessable, sound-independent comprehension).
- Caption generation in **exactly these four selectable styles**: **formal**, **sarcastic**, **humorous-tech**, **humorous-non-tech**. Allow edits and regeneration.
- Hashtag suggestions should distinguish source-backed trends from semantic/relevance suggestions; never assert an unsourced tag is trending.
- Preserve creator voice and constraints. Support saved versions and before/after comparison.

### 3.10 Experiments and comparisons

- Compare Reel draft A/B, alternate hooks/captions, or publishing variants.
- Distinguish simulated/heuristic evaluations from **actual observed** platform results.
- Track hypothesis, variant, evaluation version, publish status, and metrics when available.
- Avoid unsupported statistical significance claims for tiny samples.

### 3.11 Content planner

- Save ideas, scripts, captions, hashtags, draft references, target persona, planned date, and status (`idea`, `draft`, `ready`, `scheduled`, `published`, `archived`).
- Calendar/list views and editing. Status labels must reflect real actions, not assumed publishing.
- Persist all changes with user ownership.

### 3.12 Tool-using AI strategist

- Conversational strategist that can call **real, typed application tools** for creator profile, audience evidence, recent trends, opportunities, Reel analyses, experiments, and planner items.
- Tool results must be scoped to the authenticated user, schema-validated, logged, and provenance-aware.
- Use a reasoning-capable model (Groq-hosted GPT-OSS or a verified available alternative) for orchestration when appropriate; do not fake tool use with a single text prompt.
- Read-only tools may execute without additional approval; writes to planner and any publishing/account changes require explicit confirmation, with stricter approval for irreversible actions.
- Provide clear action previews, audit logs, and recovery when tools fail.

### 3.13 Publishing and feedback learning

- Official Instagram publishing only if the connected account, granted scopes, app review status, media format, and current Meta API actually support the operation.
- Publishing must require explicit user approval of exact media/caption/account; show API status and outcome. No hidden automatic posting.
- If permissions are unavailable, offer a manual publishing handoff/export instead of pretending it posted.
- Later sync actual accessible performance metrics with timestamps; compare to prior hypotheses and update creator strategy, calibrating rather than retroactively rewriting prior predictions.
- Support opt-out, data deletion, and revocation handling.

---

## 4. Data access and Instagram integration

### 4.1 Official integration only

- Support authorized Meta Instagram professional account flows. Determine whether **Instagram Login** or **Facebook Login** is appropriate based on the *current* Meta documentation, supported permissions, and available insights/publishing endpoints. These flows have different requirements.
- Use OAuth state/CSRF protection, secure redirect validation, least-privilege scopes, encrypted token storage, token expiry/refresh handling where supported, disconnect/revocation, and informative errors.
- App Review, business verification, test users, and platform eligibility may restrict access. **Do not claim these are approved.**
- Do not assume arbitrary public accounts, private followers, personal account analytics, or per-viewer engagement are available.
- Design sync jobs to be incremental, rate-limit aware, idempotent, and resilient to partial failures.

### 4.2 Manual authorized import fallback

- Allow the creator to upload permitted exports or a documented CSV/JSON schema for their own media/aggregate insights.
- Validate schema, dates, numeric ranges, duplicate IDs, and ownership/consent; display which fields are missing.
- Mark imported metrics as `user_import` and retain provenance. Do not label them API-verified.
- Provide a **clearly labeled synthetic demo dataset** for judging/demo when live Meta access is blocked. Demo data must never appear as a real creator's data.

### 4.3 Source-of-truth tiers

1. **Observed:** Authorized platform response or user-supplied data, labeled with origin.
2. **Derived:** Reproducible deterministic calculations from observed data.
3. **Inferred:** Model-generated interpretation grounded in observed/derived context.
4. **Simulated:** Hypothetical persona reactions, predictions, and suggestions.
5. **Unknown:** Data not available or not reliable enough to assert.

Expose these distinctions in backend schemas and UI labels.

---

## 5. Proposed technical stack

**Frontend:** Next.js App Router, TypeScript, Tailwind CSS, shadcn/ui, TanStack Query, Recharts, generated OpenAPI types, reusable domain hooks, responsive accessible components. Functional baseline first; final visual design later.

**Backend:** Python FastAPI, Pydantic v2, typed service layer, async endpoints where appropriate, explicit authorization dependencies, OpenAPI schema.

**Persistence:** MongoDB Atlas (development-compatible local MongoDB option), indexed collections and tenant-scoped repository layer. MongoDB Atlas Vector Search is optional and must have a clear use case before adding it.

**Background jobs:** Redis + RQ workers for sync, video processing, and long-running analyses. Job status persisted in MongoDB.

**Private media:** S3-compatible object storage, presigned uploads/downloads, short-lived access, server-side validation, retention/deletion.

**Media/AI:** FFmpeg, PySceneDetect, Whisper Large-v3 Turbo or verified equivalent, PaddleOCR where appropriate, Gemini Flash-family multimodal model, Groq GPT-OSS reasoning model or verified alternative. BGE-M3 embeddings optional. **All model IDs, provider capabilities, limits, and pricing must be checked before hardcoding.** Use provider adapters and structured output validation. No fabricated success when an API key is absent.

**Deployment target:** Vercel frontend; Vultr API and worker where suitable; MongoDB Atlas database; managed or self-hosted Redis and private object storage according to verified availability and cost. Deployment choices can change if they block a reliable demo.

**Observability:** Structured logs with request/job IDs, error reporting, basic metrics, health/readiness checks, audit records for sensitive actions. Never log tokens, passwords, or private media contents unnecessarily.

---

## 6. Repository structure

Suggested monorepo (adapt only with documented rationale):

```text
verdict/
├── PROJECT_SPEC.md
├── AGENTS.md
├── README.md
├── .gitignore
├── .env.example
├── apps/
│   ├── web/
│   │   ├── app/
│   │   ├── components/
│   │   ├── features/
│   │   ├── hooks/
│   │   ├── lib/
│   │   └── tests/
│   ├── api/
│   │   ├── app/
│   │   │   ├── main.py
│   │   │   ├── core/
│   │   │   ├── routes/
│   │   │   ├── schemas/
│   │   │   ├── services/
│   │   │   ├── integrations/
│   │   │   ├── db/
│   │   │   ├── repositories/
│   │   │   └── jobs/
│   │   └── tests/
│   └── worker/
├── packages/
│   └── contracts/
├── tests/
│   ├── integration/
│   └── e2e/
├── infra/
└── docs/
    ├── implementation-plan.md
    ├── feature-status.md
    ├── checkpoints.md
    ├── test-results.md
    ├── known-issues.md
    ├── architecture.md
    ├── data-provenance.md
    ├── api-permissions.md
    └── demo-runbook.md
```

Keep shared API types generated from FastAPI OpenAPI where feasible. Avoid duplicating business logic in frontend components.

---

## 7. MongoDB data model

Core collections (names may be refined in implementation plan, but preserve functionality):

| Collection | Purpose / minimum fields |
|---|---|
| `users` | User ID, auth provider subject, preferences, created/updated timestamps |
| `instagram_accounts` | Owner ID, platform account ID, scopes, token reference/encrypted token, expiry, connection status, sync state |
| `media` | Owner/account IDs, platform/import IDs, media type, timestamps, caption, hashtags, storage reference, provenance |
| `media_insights` | Media ID, owner ID, metric name/value, observation window, source, retrieved time |
| `creator_profiles` | Owner ID, niche/subtopics, voice, historical summaries, evidence, version |
| `audience_profiles` | Owner ID, aggregate audience stats, source, as-of time, availability/coverage |
| `personas` | Owner ID, observed evidence, inferred traits, confidence, provisional status, version |
| `trends` | Topic/tag/format, source URLs, observation/published/retrieved times, niche relevance, freshness |
| `opportunities` | Owner ID, idea, evidence, four component scores, weighted total, score version |
| `analyses` | Owner ID, media/draft version, job ID, transcript/frames references, findings, model versions |
| `experiments` | Owner ID, hypothesis, variants, simulated results, observed results, status |
| `jobs` | Owner ID, type, status, progress, retries, timestamps, error codes, idempotency key |
| `content_plans` | Owner ID, idea/script/caption, scheduled date, status, associated assets |
| `feedback` | Owner ID, suggestion/action, user feedback, observed later outcomes, timestamps |
| `publishing_records` | Owner ID, account/media/caption, approval, API response/status, audit timestamps |
| `agent_runs` | Owner ID, user request, tool invocations/results metadata, approvals, outcome, timestamps |

**Cross-cutting requirements:**
- Every creator-owned record has an immutable `owner_id` (or tenant ID) and timestamps.
- All reads/writes enforce owner scoping in repositories and service boundaries, not just UI filtering.
- Appropriate compound indexes for owner + creation time, account + media ID, job status, and deduplication.
- Schema versioning/migrations, validation, pagination, and retention/deletion semantics.
- Encrypt sensitive tokens at rest; never store secrets in client-visible payloads.
- Store evidence/provenance alongside claims or through stable references.

---

## 8. API contract — proposed route groups

Version APIs under `/api/v1`. Final method/path details should be recorded in OpenAPI and contract tests. Minimum functionality:

| Domain | Example endpoints |
|---|---|
| Health | `GET /health`, `GET /ready` |
| Auth/users | `GET /auth/me`, auth callbacks/session operations, `DELETE /users/me` |
| Instagram | `GET /instagram/connect`, `GET /instagram/callback`, `POST /instagram/sync`, `GET /instagram/status`, `POST /instagram/disconnect` |
| Import | `POST /imports`, `GET /imports/{id}`, validation/report routes |
| Creator | `GET /creator/profile`, `POST /creator/analyze` |
| Audience | `GET /audience/summary`, `GET /audience/personas`, `POST /audience/personas/regenerate` |
| Trends | `GET /trends`, `POST /trends/refresh` |
| Opportunities | `GET /opportunities`, `POST /opportunities/generate`, `POST /opportunities/{id}/save` |
| Upload/jobs | `POST /uploads/presign`, `POST /analyses`, `GET /jobs/{id}`, `GET /analyses/{id}` |
| Optimization | `POST /analyses/{id}/optimize`, caption/hook variant routes |
| Experiments | `GET/POST /experiments`, `GET/PATCH /experiments/{id}` |
| Planner | `GET/POST /planner`, `GET/PATCH/DELETE /planner/{id}` |
| Agent | `POST /agent/runs`, `GET /agent/runs/{id}`, approval endpoint |
| Publishing | `POST /publishing/preview`, `POST /publishing/approve`, `GET /publishing/{id}` |
| Feedback | `POST /feedback`, `POST /performance/sync`, performance reports |

For every endpoint: authenticated identity where required; object-level authorization; validated request/response schemas; consistent error codes; rate limiting; pagination for lists; idempotency for side-effecting/long-running requests; documented status codes. Never expose one user's records to another user.

---

## 9. AI system design

### 9.1 Provider adapters

Use interfaces for `MultimodalAnalyzer`, `Transcriber`, `ReasoningModel`, `EmbeddingProvider` (optional), and `TrendSource`. Record provider/model/version, latency, usage/cost where available, and errors. Keep provider-specific code out of core business services.

### 9.2 Structured outputs

Use Pydantic models/JSON schema for persona, trend, opportunity, analysis, optimization, and agent tool outputs. Validate timestamps against media duration, component scores within 0–100, required evidence references, and enum values. Reject or safely repair malformed model outputs with bounded retries; do not silently accept fabricated fields.

### 9.3 Prompting and safety

- Supply only minimum necessary creator context to external providers.
- Treat imported captions, transcripts, OCR, external trend pages, and tool results as **untrusted content**, not instructions.
- Do not let model-generated text authorize tool actions or publishing.
- Enforce tool permissions server-side, not only in prompts.
- Document external AI data processing and retention considerations.
- Make outputs editable; provide explicit caveats where estimates are subjective.

### 9.4 Scoring

Implement the opportunity score as a deterministic pure function with unit tests, including bounds, missing data, rounding, and reproducibility. Keep the scoring formula in one versioned module. LLMs may propose candidate ideas and evidence-linked subscore rationales, but Python owns the final weighted calculation.

### 9.5 Evaluation

Create a small, documented evaluation set with labeled demo creator histories, known Reel issues, persona grounding checks, prompt-injection cases, and unsupported-claim checks. Evaluate usefulness, evidence quality, schema validity, hallucinations, and latency. Do not present self-generated benchmark numbers as externally validated.

---

## 10. Security, privacy, reliability, and accessibility

### Security

- Secure auth sessions/cookies and CSRF protection where applicable.
- OAuth state validation, scoped permissions, token encryption and rotation strategy.
- Backend ownership checks for every record, upload, job, and agent tool.
- Presigned object storage with short expiry and restricted paths; validate actual uploaded media.
- Restrict CORS, configure security headers, prevent SSRF in URL ingestion, and sanitize rendered untrusted text.
- Validate file formats/sizes and resource budgets; bound FFmpeg and model workloads.
- Secret management via environment variables/secrets service; `.env.example` only contains placeholders.
- Rate limits, abuse protection, retry backoff, idempotency, and job deduplication.
- Audit publishing, account connections, deletions, and agent writes.

### Privacy and compliance

- Transparent consent and privacy explanation for Instagram data and third-party AI processing.
- Minimal data collection; creator export/deletion and account disconnect.
- Defined retention for uploads, extracted frames/audio, transcripts, and logs.
- Respect Meta platform terms and applicable laws; document unresolved compliance requirements before launch.
- No individual follower profiling, unauthorized scraping, or private-message ingestion.

### Reliability and UX

- Meaningful loading/progress/error states and resumable user workflows.
- Graceful degradation when external integrations are unavailable.
- Accessible keyboard navigation, focus states, labels, semantic markup, readable contrast, and captions/transcripts where possible.
- Responsive baseline for desktop and mobile; no UI-only mock buttons claiming success.

---

## 11. Testing and acceptance strategy

**Automated tests:**
- Python `pytest` unit tests for scoring, provenance, persona grounding, permissions, data validation, and services.
- API integration tests with test database and mocked external services; test OAuth state handling and cross-user access denial.
- Worker/job tests for queue states, idempotency, retries, malformed uploads, and partial failures.
- TypeScript type checking, linting, component tests where useful, and Next.js production build.
- Playwright end-to-end tests for the principal creator journey using **clearly labeled synthetic fixture data** and authorized test accounts where available.
- Contract tests for OpenAPI types and frontend/backend compatibility.
- Security-focused tests for cross-tenant access, prompt injection, unauthorized publishing, and secret leakage.

**Manual verification:** At the end of each major milestone, provide exact commands, local URLs, expected screens, expected database/job state, and failure cases to try. Do not claim a feature works merely because code compiles.

**Definition of Done for a milestone:**
1. Implementation integrated with actual backend/frontend/database as relevant.
2. Relevant automated tests and builds run, with results reported accurately.
3. Missing credentials or platform approvals explicitly documented, not masked by fabricated success.
4. Manual verification instructions provided; user confirms acceptance.
5. Docs updated; approved Git commit/checkpoint created.

---

## 12. Development milestones and checkpoints

**Codex is the sole implementation assistant working directly in this repository.** Work incrementally; never attempt the entire platform in one giant change.

| Milestone | Scope | Acceptance gate |
|---|---|---|
| **M0 — Foundation** | Monorepo, Next.js/FastAPI skeleton, environment templates, MongoDB connectivity, health check, frontend→backend call, tests, CI baseline | App starts locally; API health visible in UI; tests/build pass |
| **M1 — Auth and isolation** | Login/session, onboarding, user records, owner-scoped services | User A cannot read/write User B data |
| **M2 — Instagram connection/import** | Official OAuth where available, connection state, sync, validated manual import, labeled demo fixtures | Real authorized data imports or documented permission block + working manual fallback |
| **M3 — Creator intelligence** | Historical aggregates, content classification, creator profile | Evidence-backed insights with dates/sample sizes |
| **M4 — Audience personas** | Current available aggregate audience ingestion, observed/inferred split, provisional fallback | Personas cite real available stats; no invented demographics |
| **M5 — Trends** | Authorized source adapters, recency/provenance, graceful fallback | Each claimed trend has real source/timestamp |
| **M6 — Opportunities** | Personalized ideas, deterministic weighted scoring, explanations | Score formula and missing-data tests pass; saved ideas persist |
| **M7 — Video processing** | Private upload, job queue, FFmpeg, transcript, scene/OCR extraction, multimodal report | Real uploaded sample produces stored analysis with job lifecycle |
| **M8 — Optimization** | Persona simulations, timestamped edits, hooks, four caption styles, accessibility | Reports are editable, grounded, and clearly labeled as estimates |
| **M9 — Experiments/planner** | A/B versions, hypothesis tracking, content calendar | Data persists and simulated vs observed results are distinct |
| **M10 — Agent** | Typed tool calls, evidence-aware responses, approval workflow | Agent executes real scoped tools and requires approval for writes |
| **M11 — Publishing/learning** | Official API publishing if permitted, manual handoff fallback, metrics sync, feedback | No publishing without approval; blocked permissions disclosed |
| **M12 — Launch readiness** | Deploy, polish UI, accessibility/security checks, demo flow, docs | Demo can be repeated from documented setup and fixtures |

### Checkpoint protocol

For **each** milestone:

1. Inspect current repo, existing implementation, open issues, and latest checkpoint.
2. Present a short plan with exact files, dependencies, acceptance tests, and blockers.
3. Use a dedicated feature branch (e.g. `feat/m4-audience-personas`); keep `main` stable.
4. Implement in small cohesive changes; run targeted tests as work progresses.
5. Run applicable full regression suite, lint/typecheck, production build, and Playwright checks.
6. Report actual pass/fail/skip results and provide exact manual verification steps.
7. **Stop and wait for the user's approval** at milestone boundary.
8. Only with approval, commit/tag verified checkpoint; request permission before pushing/merging if not already granted.
9. Update `docs/implementation-plan.md`, `docs/feature-status.md`, `docs/checkpoints.md`, `docs/test-results.md`, and `docs/known-issues.md`.
10. Never use destructive Git commands (`reset --hard`, force push) without explicit informed approval. Never commit secrets.

**Session continuity:** Read `PROJECT_SPEC.md`, `AGENTS.md`, and checkpoint docs at the beginning of each new Codex session. Summarize current status and propose only the next uncompleted task.

---

## 13. Hackathon MVP versus full product

**MVP means a genuinely working vertical slice, not a claim that every roadmap feature is complete.** Prioritize:

1. User enters a working app and connects authorized creator data **or** imports their own structured data. For judge demonstrations, a clearly labeled synthetic sample creator is acceptable.
2. Dashboard displays historically grounded creator insights and audience personas with observed/inferred distinctions.
3. User sees niche-relevant opportunities with transparent scores; any trends are source-backed or clearly marked unavailable.
4. User uploads a real sample Reel, sees actual processing progress, and receives timestamped multimodal feedback.
5. User gets concrete hook/caption/CTA suggestions, including all four caption styles, and saves a revised idea to the planner.
6. App is deployed and demonstrable with a repeatable fallback when Meta approval, API quotas, or cloud services are unavailable.

**Stretch after the working slice:** polished experiment comparisons, richer agent orchestration, production publishing, continuous feedback learning, advanced embeddings, additional trend sources, elaborate UI animation. These remain in the **full product scope** but must be honestly marked incomplete until implemented.

### Demo narrative

- Creator's problem: analytics describe past performance but do not prescribe the next Reel or help before publishing.
- Show evidence from imported creator history and available audience aggregates.
- Explain one personalized opportunity and its four component scores.
- Upload a Reel and display timestamped improvements and persona simulations with clear uncertainty.
- Generate four caption tones and save a chosen version to planner.
- Show how future real performance would close the loop; do not pretend unavailable publishing/feedback already happened.

### Award positioning (not guaranteed)

Emphasize functioning software, usable UI, explainable and impactful AI, Gemini multimodal integration, MongoDB Atlas data design, Vultr deployment if actually used, and agentic capabilities if genuinely implemented. Verify current hackathon categories and eligibility rather than asserting prizes or sponsorship benefits.

---

## 14. External dependencies and decisions to verify early

Before promising any integration, document:

- Current Meta Instagram Login/Facebook Login flow, permission names, eligible accounts, Insights availability, App Review/testing restrictions, and publishing support.
- Gemini model IDs, video limits, structured output, quotas, costs, and data handling.
- Groq-hosted model availability and tool-calling/structured-output support.
- Whisper transcription runtime/hosting, FFmpeg/PySceneDetect/PaddleOCR installation, video processing latency, and CPU/GPU budget.
- Trend sources with permitted access, attribution, update frequency, and price.
- MongoDB Atlas, Redis, object storage, Vercel, and Vultr credentials/free-tier limitations.
- Authentication provider choice, deployment secrets, domain/redirect URIs, and privacy disclosures.

If an integration cannot be used during the hackathon, document the blocker and implement an honest fallback that does not counterfeit a successful external action.

---

## 15. Initial instructions to Codex

On first launch:

1. Read this specification in full.
2. Inspect the actual repository; do not assume files already exist.
3. Create `AGENTS.md` containing stable engineering rules and links back to this specification.
4. Draft `docs/implementation-plan.md` with dependencies, acceptance criteria, MVP critical path, time/cost risks, and blocked external integrations.
5. Create the remaining checkpoint/status documentation templates.
6. Explain any proposed deviation from this specification and obtain approval before changing product scope.
7. **Do not implement M0 until the user approves the plan.**

**Never:** claim untested features are complete; invent creator data or trend sources; conflate simulated feedback with real viewers; silently implement niche switching; publish without approval; bypass security to make the demo work; spend money without approval; or overwrite working code without checking its current state.

**Success criterion:** A real, secure, testable creator workflow with a persuasive hackathon demo and an honest, well-structured path to the complete Verdict SaaS.
