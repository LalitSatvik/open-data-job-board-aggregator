import logging
from datetime import datetime, timezone
from typing import List

import httpx

from app.schemas.job import NormalizedJob

logger = logging.getLogger(__name__)

ARBEITNOW_URL = "https://www.arbeitnow.com/api/job-board-api"


def fetch_arbeitnow() -> List[NormalizedJob]:
    try:
        response = httpx.get(ARBEITNOW_URL, timeout=10)
        response.raise_for_status()
        payload = response.json()
        results = []
        for raw in payload.get("data", []):
            created_at = raw.get("created_at")
            posted_at = (
                datetime.fromtimestamp(created_at, tz=timezone.utc)
                if isinstance(created_at, (int, float))
                else None
            )
            results.append(
                NormalizedJob(
                    source="arbeitnow",
                    source_id=raw["slug"],
                    title=raw["title"],
                    company=raw["company_name"],
                    location=raw.get("location"),
                    remote=bool(raw.get("remote", False)),
                    salary_min=None,
                    salary_max=None,
                    url=raw["url"],
                    description=raw.get("description"),
                    posted_at=posted_at,
                )
            )
        return results
    except Exception:
        logger.exception("Failed to fetch jobs from Arbeitnow")
        return []
