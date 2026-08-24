from unittest.mock import patch

from app.services.adapters.remotive import fetch_remotive

SAMPLE_RESPONSE = {
    "jobs": [
        {
            "id": 111,
            "title": "Senior Backend Engineer",
            "company_name": "Acme Corp",
            "candidate_required_location": "USA",
            "salary": "$120,000 - $150,000",
            "url": "https://remotive.com/remote-jobs/111",
            "description": "<p>Build things.</p>",
            "publication_date": "2026-08-01T00:00:00",
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


def test_fetch_remotive_normalizes_jobs():
    with patch("app.services.adapters.remotive.httpx.get") as mock_get:
        mock_get.return_value = FakeResponse(SAMPLE_RESPONSE)
        jobs = fetch_remotive()

    assert len(jobs) == 1
    job = jobs[0]
    assert job.source == "remotive"
    assert job.source_id == "111"
    assert job.title == "Senior Backend Engineer"
    assert job.company == "Acme Corp"
    assert job.remote is True
    assert job.salary_min == 120000
    assert job.salary_max == 150000
    assert job.url == "https://remotive.com/remote-jobs/111"


def test_fetch_remotive_returns_empty_list_on_failure():
    with patch("app.services.adapters.remotive.httpx.get") as mock_get:
        mock_get.side_effect = RuntimeError("network down")
        jobs = fetch_remotive()

    assert jobs == []
