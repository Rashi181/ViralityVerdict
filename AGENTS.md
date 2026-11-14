# Verdict — Codex Engineering Instructions

Read `PROJECT_SPEC.md` before planning or implementing any feature. It is the authoritative product specification. This file governs working practices, not product scope.

## Scope and implementation
- Build Verdict as a real, multi-tenant Instagram creator intelligence and pre-publication Reel optimization platform. Preserve every feature in the full roadmap, even if deferred beyond the hackathon MVP.
- Do not implement niche switching or niche pivot simulation.
- Work in small, testable milestones M0–M12. Start by inspecting the repository and preparing `docs/implementation-plan.md`; do not begin M0 until the user approves the plan.
- Prefer straightforward, maintainable implementations, but never simplify away required capabilities, validation, authz, error handling, reliability, privacy, or tests.
- Keep the frontend modular for a later visual redesign; preserve API contracts.
- Use real, authorized data where available. Label demo fixtures, inferences, and simulated persona reactions. Never fabricate audience statistics, trend sources, video retention curves, API responses, or test results.
- Check current provider permissions, model IDs, API limits, and pricing before implementation. If blocked, document the blocker and use a clearly labeled, permitted fallback.

## Repository safety
- Inspect `git status` and existing files before editing. Preserve user changes. Work on a feature branch/worktree for major changes.
- Never use force push, `git reset --hard`, destructive cleanup, or unrelated rewrites without explicit approval.
- Do not commit, push, merge, delete user data, or provision paid infrastructure without explicit approval.
- Never expose or commit credentials. Use `.env.example` with placeholders and local ignored environment files for secrets.

## Milestone definition of done
1. State scope, affected files, acceptance criteria, dependencies, and blockers.
2. Implement backend, frontend, persistence, and tests as required by that milestone.
3. Run applicable Python tests, TypeScript typecheck, lint, production build, integration and E2E tests. Report actual pass/fail/skip; do not claim unrun tests passed.
4. Provide exact local run and manual verification instructions.
5. Update `docs/implementation-plan.md`, `docs/feature-status.md`, `docs/checkpoints.md`, `docs/test-results.md`, `docs/known-issues.md`.
6. Stop at milestone boundaries for the user's verification and approval before checkpoint/next milestone.

## New session handoff
Read `PROJECT_SPEC.md`, this file, and the docs above. Check git status. Summarize completed milestones, blockers, failing tests, and the next smallest task. Do not repeat completed work or assume unverified functionality works.
