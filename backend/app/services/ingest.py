from typing import List

from sqlalchemy.orm import Session

from app.models import Job
from app.schemas.job import NormalizedJob
from app.services.adapters.arbeitnow import fetch_arbeitnow
from app.services.adapters.remoteok import fetch_remoteok
from app.services.adapters.remotive import fetch_remotive
from app.services.adapters.synthetic import generate_synthetic_jobs

MIN_TOTAL_BEFORE_FALLBACK = 5
FALLBACK_TARGET_TOTAL = 20


def _upsert(db: Session, jobs: List[NormalizedJob]) -> int:
    count = 0
    for job in jobs:
        existing = (
            db.query(Job)
            .filter_by(source=job.source, source_id=job.source_id)
            .one_or_none()
        )
        data = job.model_dump()
        if existing:
            for key, value in data.items():
                setattr(existing, key, value)
        else:
            db.add(Job(**data))
        count += 1
    db.commit()
    return count


def run_ingest(db: Session) -> dict:
    remotive_jobs = fetch_remotive()
    remoteok_jobs = fetch_remoteok()
    arbeitnow_jobs = fetch_arbeitnow()

    combined = remotive_jobs + remoteok_jobs + arbeitnow_jobs
    synthetic_jobs: List[NormalizedJob] = []
    if len(combined) < MIN_TOTAL_BEFORE_FALLBACK:
        needed = max(FALLBACK_TARGET_TOTAL - len(combined), 0)
        synthetic_jobs = generate_synthetic_jobs(needed)
        combined = combined + synthetic_jobs

    ingested = _upsert(db, combined)

    return {
        "ingested": ingested,
        "sources": {
            "remotive": len(remotive_jobs),
            "remoteok": len(remoteok_jobs),
            "arbeitnow": len(arbeitnow_jobs),
            "synthetic": len(synthetic_jobs),
        },
    }
