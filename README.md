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
