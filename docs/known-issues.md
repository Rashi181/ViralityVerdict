# Known Issues and External Limitations

**Last updated:** 2026-11-14

## Environment

| ID | Issue | Impact | Workaround / next step |
|---|---|---|---|
| ENV-1 | The dev container has no Docker daemon and no `mongod` binary | Can't run a local MongoDB via Docker | Use a MongoDB Atlas free cluster URI, or download `mongod` at M0 (decision D3) |
| ENV-2 | Available here: Node 22, pnpm 10, Python 3.13, uv, Redis 7.0, FFmpeg 6.1 | — | Redis and FFmpeg can run locally |

## External integrations (all unverified)

| ID | Integration | Limitation / unknown | Fallback |
|---|---|---|---|
| EXT-1 | Meta Instagram API | Login type, scopes, insights eligibility, App Review, and tester restrictions not yet verified against current docs. No Meta app known to exist. | Manual import (M2a) + labeled synthetic demo |
| EXT-2 | Gemini | Model ID, limits, free quota, data-retention terms unverified. No key configured. | `provider_unavailable` state; no fake analysis |
| EXT-3 | Groq (Whisper, GPT-OSS) | Availability and tool calling unverified. No key configured. | Local faster-whisper for transcription |
| EXT-4 | Trend sources | No verified, permitted source yet | "Trends unavailable" + COS fallback (D10) |
| EXT-5 | Hosting for API/worker (Vultr) | Paid. Needs user approval. | Free alternative TBD |

## Bugs

None yet. There is no code.
