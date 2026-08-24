from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class NormalizedJob(BaseModel):
    source: str
    source_id: str
    title: str
    company: str
    location: Optional[str] = None
    remote: bool = False
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    url: str
    description: Optional[str] = None
    posted_at: Optional[datetime] = None
