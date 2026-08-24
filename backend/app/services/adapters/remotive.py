import logging
import re
from typing import List, Optional

import httpx

from app.schemas.job import NormalizedJob

logger = logging.getLogger(__name__)

REMOTIVE_URL = "https://remotive.com/api/remote-jobs"


def _parse_salary(raw: Optional[str]):
    if not raw:
        return None, None
    numbers = [int(n.replace(",", "")) for n in re.findall(r"[\d,]{3,}", raw)]
    if not numbers:
        return None, None
    if len(numbers) == 1:
        return numbers[0], numbers[0]
    return min(numbers), max(numbers)


def fetch_remotive() -> List[NormalizedJob]:
    try:
        response = httpx.get(REMOTIVE_URL, timeout=10)
        response.raise_for_status()
        payload = response.json()
        results = []
        for raw in payload.get("jobs", []):
            salary_min, salary_max = _parse_salary(raw.get("salary"))
            results.append(
                NormalizedJob(
                    source="remotive",
                    source_id=str(raw["id"]),
                    title=raw["title"],
                    company=raw["company_name"],
                    location=raw.get("candidate_required_location"),
                    remote=True,
                    salary_min=salary_min,
                    salary_max=salary_max,
                    url=raw["url"],
                    description=raw.get("description"),
                    posted_at=raw.get("publication_date"),
                )
            )
        return results
    except Exception:
        logger.exception("Failed to fetch jobs from Remotive")
        return []
