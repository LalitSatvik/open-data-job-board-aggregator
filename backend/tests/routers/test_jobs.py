def _seed_jobs(db):
    from app.models import Job

    db.add_all(
        [
            Job(source="remotive", source_id="1", title="Backend Engineer",
                company="Acme", location="Remote", remote=True,
                salary_min=100000, salary_max=140000, url="https://x.test/1"),
            Job(source="remoteok", source_id="2", title="Sales Rep",
                company="Widget Co", location="New York", remote=False,
                salary_min=60000, salary_max=80000, url="https://x.test/2"),
            Job(source="arbeitnow", source_id="3", title="Backend Developer",
                company="Blueharbor", location="Berlin", remote=True,
                salary_min=90000, salary_max=120000, url="https://x.test/3"),
        ]
    )
    db.commit()


def test_jobs_search_by_query(client):
    from app.database import get_db
    import app.main as main_module

    db = next(main_module.app.dependency_overrides[get_db]())
    _seed_jobs(db)

    response = client.get("/jobs", params={"q": "backend"})
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 2
    assert {item["title"] for item in body["items"]} == {
        "Backend Engineer", "Backend Developer"
    }


def test_jobs_filter_by_remote_and_salary(client):
    from app.database import get_db
    import app.main as main_module

    db = next(main_module.app.dependency_overrides[get_db]())
    _seed_jobs(db)

    response = client.get("/jobs", params={"remote": "true", "salary_min": "100000"})
    body = response.json()
    assert body["total"] == 2
    assert {item["title"] for item in body["items"]} == {
        "Backend Engineer", "Backend Developer"
    }


def test_jobs_filter_salary_range_overlap(client):
    from app.database import get_db
    import app.main as main_module

    db = next(main_module.app.dependency_overrides[get_db]())
    _seed_jobs(db)

    response = client.get("/jobs", params={"salary_min": "100000"})
    body = response.json()
    assert body["total"] == 2
    titles = {item["title"] for item in body["items"]}
    assert "Backend Engineer" in titles
    assert "Backend Developer" in titles
    assert "Sales Rep" not in titles


def test_jobs_pagination(client):
    from app.database import get_db
    import app.main as main_module

    db = next(main_module.app.dependency_overrides[get_db]())
    _seed_jobs(db)

    response = client.get("/jobs", params={"page": 1, "page_size": 2})
    body = response.json()
    assert len(body["items"]) == 2
    assert body["page"] == 1
    assert body["page_size"] == 2
    assert body["total"] == 3
