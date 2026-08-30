# Open Data Job Board Aggregator + Application Tracker

A searchable job board built from free public job APIs, with a personal
application tracker (kanban, status history) and CSV/JSON export.

## Structure

- `backend/` — FastAPI API
- `frontend/` — Next.js app
- `render.yaml` — Render Blueprint for the backend service

## Local setup

Prerequisites: Python 3.11+ and Node 18+.

### Backend

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Fill in `.env`:

- `DATABASE_URL` — leave empty to use the local SQLite default
  (`sqlite:///./dev.db`), or paste a Postgres connection string.
- `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET` — from a Google Cloud OAuth
  client with `http://localhost:8000/auth/google/callback` as an
  authorized redirect URI.
- `JWT_SECRET` / `INGEST_SECRET` — any long random strings. The app
  refuses to start with the built-in development defaults unless
  `FRONTEND_URL` points at localhost.
- `FRONTEND_URL` — `http://localhost:3000` for local development.

Create the tables and start the API:

```bash
alembic upgrade head
uvicorn app.main:app --reload
```

Seed some listings so the board isn't empty (uses your `INGEST_SECRET`):

```bash
curl -X POST http://localhost:8000/ingest -H "X-Ingest-Secret: <your secret>"
```

Run the tests from `backend/`:

```bash
pytest
```

### Frontend

```bash
cd frontend
npm install
cp .env.local.example .env.local   # set NEXT_PUBLIC_API_URL=http://localhost:8000
npm run dev
```

The app is then on `http://localhost:3000`.

## Scheduled ingest

`.github/workflows/ingest.yml` runs hourly and can be triggered manually
from the Actions tab. It requires two repository secrets:

- `RENDER_API_URL` — the deployed backend's base URL
- `INGEST_SECRET` — must match the backend's `INGEST_SECRET` env var

Set both under Settings → Secrets and variables → Actions. Neither value
is ever committed to this repo.

## Deployment

1. **Neon** — create a free Postgres project, copy its connection string.
2. **Render** — New → Blueprint, point it at this repository. Render picks
   up `render.yaml` at the repo root, which builds and runs the service
   from `backend/` and applies migrations (`alembic upgrade head`) before
   each deploy. Fill in the env vars it prompts for: `DATABASE_URL` (from
   Neon), `GOOGLE_CLIENT_ID`/`GOOGLE_CLIENT_SECRET` (from a Google Cloud
   OAuth client with the callback URL
   `https://<render-service>.onrender.com/auth/google/callback`),
   `JWT_SECRET`/`INGEST_SECRET` (any long random strings — the app refuses
   to boot on the development defaults), and `FRONTEND_URL` (the Vercel
   URL from step 3 — update after step 3). Pre-deploy commands need a paid
   instance type; on the free plan drop `preDeployCommand` from
   `render.yaml` and run `alembic upgrade head` once from the Render
   shell instead. After the first deploy, trigger `/ingest` once manually
   so the board isn't empty.
3. **Vercel** — import `frontend/` as the project root, set
   `NEXT_PUBLIC_API_URL` to the Render URL from step 2.
4. Update Render's `FRONTEND_URL` to the real Vercel URL and redeploy the
   backend so OAuth redirects and CORS point at the live frontend.
5. Add the `RENDER_API_URL`/`INGEST_SECRET` GitHub Actions secrets
   described above so the hourly ingest cron runs against production.

## Demo script (under 2 minutes)

1. Open the Vercel URL, click "Sign in with Google".
2. On the job board, search a keyword and toggle "Remote only".
3. Click "Track this job" on two or three listings.
4. Go to the tracker, drag a card from Saved → Applied → Interviewing.
5. Click a card to show its status-history timeline and add a note.
6. Click "Export CSV" (and/or "Export JSON") to show the downloaded
   pipeline, including the history trail.

## License

[MIT](LICENSE)
