from unittest.mock import patch

from app.services.adapters.remoteok import fetch_remoteok

SAMPLE_RESPONSE = [
    {"legal": "https://remoteok.com/legal"},
    {
        "id": "222",
        "position": "Frontend Engineer",
        "company": "Widget Inc",
        "location": "Worldwide",
        "salary_min": 90000,
        "salary_max": 110000,
        "url": "https://remoteok.com/remote-jobs/222",
        "description": "Build UI.",
        "date": "2026-08-02T00:00:00",
    },
]


class FakeResponse:
    def __init__(self, payload, status_code=200):
        self._payload = payload
        self.status_code = status_code

    def json(self):
        return self._payload

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError("http error")


def test_fetch_remoteok_skips_legend_and_normalizes():
    with patch("app.services.adapters.remoteok.httpx.get") as mock_get:
        mock_get.return_value = FakeResponse(SAMPLE_RESPONSE)
        jobs = fetch_remoteok()

    assert len(jobs) == 1
    job = jobs[0]
    assert job.source == "remoteok"
    assert job.source_id == "222"
    assert job.title == "Frontend Engineer"
    assert job.company == "Widget Inc"
    assert job.remote is True
    assert job.salary_min == 90000
    assert job.salary_max == 110000


def test_fetch_remoteok_returns_empty_list_on_failure():
    with patch("app.services.adapters.remoteok.httpx.get") as mock_get:
        mock_get.side_effect = RuntimeError("network down")
        jobs = fetch_remoteok()

    assert jobs == []
