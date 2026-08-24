from app.schemas.job import NormalizedJob


def test_normalized_job_requires_core_fields():
    job = NormalizedJob(
        source="remotive",
        source_id="42",
        title="Backend Engineer",
        company="Acme",
        url="https://example.com/jobs/42",
    )
    assert job.remote is False
    assert job.location is None
    assert job.salary_min is None
    assert job.posted_at is None
