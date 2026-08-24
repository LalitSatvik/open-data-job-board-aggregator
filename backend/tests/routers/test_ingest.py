from unittest.mock import patch


def test_ingest_requires_correct_secret(client):
    response = client.post("/ingest", headers={"X-Ingest-Secret": "wrong"})
    assert response.status_code == 401


def test_ingest_runs_with_correct_secret(client):
    with patch("app.routers.ingest.run_ingest", return_value={"ingested": 0, "sources": {}}):
        response = client.post(
            "/ingest", headers={"X-Ingest-Secret": "dev-ingest-secret"}
        )
    assert response.status_code == 200
    assert response.json() == {"ingested": 0, "sources": {}}
