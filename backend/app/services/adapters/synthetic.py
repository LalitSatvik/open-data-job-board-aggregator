from datetime import datetime, timedelta, timezone
from typing import List

from app.schemas.job import NormalizedJob

TITLES = [
    "Backend Engineer",
    "Frontend Engineer",
    "Full Stack Developer",
    "Data Engineer",
    "DevOps Engineer",
    "Product Manager",
    "QA Engineer",
    "Mobile Engineer",
]
COMPANIES = [
    "Northwind Systems",
    "Blueharbor Labs",
    "Cedar Analytics",
    "Fieldstone Software",
    "Vantage Point Co",
]
LOCATIONS = ["Remote", "New York, NY", "Austin, TX", "Berlin, DE", "London, UK"]


def generate_synthetic_jobs(n: int) -> List[NormalizedJob]:
    jobs = []
    now = datetime.now(timezone.utc)
    for i in range(n):
        title = TITLES[i % len(TITLES)]
        company = COMPANIES[i % len(COMPANIES)]
        location = LOCATIONS[i % len(LOCATIONS)]
        base_salary = 70000 + (i % 10) * 8000
        jobs.append(
            NormalizedJob(
                source="synthetic",
                source_id=f"synthetic-{i}",
                title=title,
                company=company,
                location=location,
                remote=(location == "Remote"),
                salary_min=base_salary,
                salary_max=base_salary + 25000,
                url=f"https://example.com/jobs/synthetic-{i}",
                description=f"{title} role at {company}. Sample listing for demo purposes.",
                posted_at=now - timedelta(days=i % 14),
            )
        )
    return jobs
