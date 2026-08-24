from app.services.adapters.synthetic import generate_synthetic_jobs


def test_generate_synthetic_jobs_returns_requested_count():
    jobs = generate_synthetic_jobs(5)
    assert len(jobs) == 5
    assert all(job.source == "synthetic" for job in jobs)
    assert len({job.source_id for job in jobs}) == 5


def test_generate_synthetic_jobs_have_required_fields():
    jobs = generate_synthetic_jobs(3)
    for job in jobs:
        assert job.title
        assert job.company
        assert job.url.startswith("https://")
        assert job.salary_min is not None
        assert job.salary_max is not None
        assert job.salary_max >= job.salary_min
