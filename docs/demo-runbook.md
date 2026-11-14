# Verdict demo and launch runbook

## Scope and safety boundary

Verdict currently supports local authenticated use, creator-authorized CSV/JSON imports, a clearly labeled synthetic demo, private local video metadata extraction, planning, and a manual publishing handoff. It does **not** connect to Instagram yet, publish content, edit an Instagram account, or claim live platform metrics.

Never put a password, Meta access token, app secret, or database URI in chat, source code, a screenshot, or a commit. Put local values only in the ignored repository-root `.env` file.

## Local startup

1. Copy `.env.example` to `.env`; set a unique `VERDICT_SESSION_SECRET` of at least 32 characters. Keep `VERDICT_COOKIE_SECURE=false` for local HTTP.
2. Start the API in terminal one:

   ```bash
   cd /Users/rashijain/Documents/ChatGPT/ViralityVerdict
   uv run --directory apps/api uvicorn app.main:app --reload --port 8000
   ```

3. Start the web app in terminal two:

   ```bash
   cd /Users/rashijain/Documents/ChatGPT/ViralityVerdict
   pnpm dev:web
   ```

4. Open `http://localhost:3000`, create an account, and continue to onboarding.

## Repeatable demo path

1. In onboarding, confirm that Instagram says it is not configured. This is correct until official OAuth is implemented and configured.
2. Click **Load synthetic demo**. It creates labeled, non-Instagram fixture data only.
3. Check **Creator intelligence**. It should show one imported item, an observed/derived summary, and sparse-history limitations.
4. Add only authorized aggregate audience evidence, or leave it blank to see the explicitly provisional persona state.
5. Upload a small MP4/WebM draft. The displayed duration and dimensions are measured locally by FFmpeg; it must not receive a public link.
6. Save a plan. Its `scheduled` state means a plan, not an Instagram post.
7. Open publishing eligibility. It must say **manual handoff required** and must not show a publish button.

## Before a real deployment

- Use HTTPS and set `VERDICT_COOKIE_SECURE=true`.
- Set `VERDICT_WEB_ORIGINS` to the exact deployed web origin(s), never `*`.
- Configure durable MongoDB, private object storage, Redis/worker, backups, retention/deletion behavior, and production error monitoring.
- Use a distinct, least-privilege Meta OAuth configuration; store tokens encrypted and never log them.
- Test only with the account owner’s explicit consent. Do not request Instagram passwords. Do not request or implement publishing scope.
- Run the verification commands below and resolve failures before deployment.

## Verification commands

```bash
pnpm lint
pnpm typecheck
pnpm test:api
pnpm build
```

## Incident response

If an account/token may be exposed: immediately revoke the connection in Meta, rotate the Meta app secret and affected tokens, remove access from the affected account, inspect access logs, and notify the account owner. Do not attempt a live sync until the issue is understood.
