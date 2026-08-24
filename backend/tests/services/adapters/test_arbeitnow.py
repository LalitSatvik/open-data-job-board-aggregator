from unittest.mock import patch

from app.services.adapters.arbeitnow import fetch_arbeitnow

SAMPLE_RESPONSE = {
    "data": [
        {
            "slug": "backend-engineer-acme-333",
            "title": "Backend Engineer",
            "company_name": "Acme GmbH",
            "location": "Berlin",
            "remote": True,
            "url": "https://www.arbeitnow.com/jobs/backend-engineer-acme-333",
            "description": "Join our team.",
            "created_at": 1722470400,
        }
    ]
}


class FakeResponse:
    def __init__(self, payload, status_code=200):
        self._payload = payload
        self.status_code = status_code

    def json(self):
        return self._payload

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError("http error")


def test_fetch_arbeitnow_normalizes_jobs():
    with patch("app.services.adapters.arbeitnow.httpx.get") as mock_get:
        mock_get.return_value = FakeResponse(SAMPLE_RESPONSE)
        jobs = fetch_arbeitnow()

    assert len(jobs) == 1
    job = jobs[0]
    assert job.source == "arbeitnow"
    assert job.source_id == "backend-engineer-acme-333"
    assert job.title == "Backend Engineer"
    assert job.company == "Acme GmbH"
    assert job.location == "Berlin"
    assert job.remote is True
    assert job.salary_min is None


def test_fetch_arbeitnow_returns_empty_list_on_failure():
    with patch("app.services.adapters.arbeitnow.httpx.get") as mock_get:
        mock_get.side_effect = RuntimeError("network down")
        jobs = fetch_arbeitnow()

    assert jobs == []
