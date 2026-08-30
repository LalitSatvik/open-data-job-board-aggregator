
from fastapi import APIRouter, Depends, Query
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Job

router = APIRouter()

MAX_PAGE_SIZE = 100


def _serialize(job: Job) -> dict:
    return {
        "id": job.id,
        "source": job.source,
        "title": job.title,
        "company": job.company,
        "location": job.location,
        "remote": job.remote,
        "salary_min": job.salary_min,
        "salary_max": job.salary_max,
        "url": job.url,
        "description": job.description,
        "posted_at": job.posted_at,
    }


@router.get("/jobs")
def list_jobs(
    q: str | None = None,
    location: str | None = None,
    remote: bool | None = None,
    salary_min: int | None = None,
    salary_max: int | None = None,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=MAX_PAGE_SIZE),
    db: Session = Depends(get_db),
):
    query = db.query(Job)

    if q:
        like = f"%{q}%"
        query = query.filter(or_(Job.title.ilike(like), Job.company.ilike(like)))
    if location:
        query = query.filter(Job.location.ilike(f"%{location}%"))
    if remote is not None:
        query = query.filter(Job.remote == remote)
    if salary_min is not None:
        query = query.filter(
            or_(Job.salary_max.is_(None), Job.salary_max >= salary_min)
        )
    if salary_max is not None:
        query = query.filter(
            or_(Job.salary_min.is_(None), Job.salary_min <= salary_max)
        )

    total = query.count()
    items = (
        query.order_by(Job.posted_at.desc().nullslast(), Job.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    return {
        "items": [_serialize(job) for job in items],
        "total": total,
        "page": page,
        "page_size": page_size,
    }
