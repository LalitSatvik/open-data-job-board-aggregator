import logging

import httpx

from app.schemas.job import NormalizedJob

logger = logging.getLogger(__name__)

REMOTEOK_URL = "https://remoteok.com/api"
# RemoteOK rejects requests without a realistic User-Agent.
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; JobBoardAggregator/1.0)"}


def fetch_remoteok() -> list[NormalizedJob]:
    try:
        response = httpx.get(REMOTEOK_URL, headers=HEADERS, timeout=10)
        response.raise_for_status()
        payload = response.json()
        results = []
        for raw in payload:
            # The first element is a legend/metadata object, not a job.
            if "id" not in raw or "position" not in raw:
                continue
            results.append(
                NormalizedJob(
                    source="remoteok",
                    source_id=str(raw["id"]),
                    title=raw["position"],
                    company=raw.get("company", "Unknown"),
                    location=raw.get("location"),
                    remote=True,
                    salary_min=raw.get("salary_min"),
                    salary_max=raw.get("salary_max"),
                    url=raw.get("url", f"https://remoteok.com/remote-jobs/{raw['id']}"),
                    description=raw.get("description"),
                    posted_at=raw.get("date"),
                )
            )
        return results
    except Exception:
        logger.exception("Failed to fetch jobs from RemoteOK")
        return []
