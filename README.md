# Open Data Job Board Aggregator + Application Tracker

A searchable job board built from free public job APIs, with a personal
application tracker (kanban, status history) and CSV/JSON export.

## Structure

- `backend/` — FastAPI API
- `frontend/` — Next.js app

See `backend/README.md` and `frontend/README.md` for setup once those
exist (added in later tasks).

## Scheduled ingest

`.github/workflows/ingest.yml` runs hourly and can be triggered manually
from the Actions tab. It requires two repository secrets:

- `RENDER_API_URL` — the deployed backend's base URL
- `INGEST_SECRET` — must match the backend's `INGEST_SECRET` env var

Set both under Settings → Secrets and variables → Actions. Neither value
is ever committed to this repo.

## Deployment

1. **Neon** — create a free Postgres project, copy its connection string.
2. **Render** — new Web Service from this repo's `backend/` directory,
   using `backend/render.yaml`. Fill in `DATABASE_URL` (from Neon),
   `GOOGLE_CLIENT_ID`/`GOOGLE_CLIENT_SECRET` (from a Google Cloud OAuth
   client with the callback URL
   `https://<render-service>.onrender.com/auth/google/callback`),
   `JWT_SECRET`/`INGEST_SECRET` (any long random strings), and
   `FRONTEND_URL` (the Vercel URL from step 3 — update after step 3).
   After the first deploy, run `alembic upgrade head` once (Render shell
   or a one-off job) to create the tables, then trigger `/ingest` once
   manually so the board isn't empty.
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
