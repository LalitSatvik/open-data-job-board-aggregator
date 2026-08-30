from datetime import datetime

from pydantic import BaseModel


class NormalizedJob(BaseModel):
    source: str
    source_id: str
    title: str
    company: str
    location: str | None = None
    remote: bool = False
    salary_min: int | None = None
    salary_max: int | None = None
    url: str
    description: str | None = None
    posted_at: datetime | None = None
