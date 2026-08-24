from unittest.mock import patch

from app.database import SessionLocal
from app.models import Job
from app.schemas.job import NormalizedJob
from app.services.ingest import run_ingest


def _job(source, source_id, title="Engineer"):
    return NormalizedJob(
        source=source, source_id=source_id, title=title, company="Acme",
        url=f"https://example.com/{source}/{source_id}",
    )


def test_run_ingest_upserts_and_dedupes(client):
    from app.database import get_db
    import app.main as main_module

    db = next(main_module.app.dependency_overrides[get_db]())

    with patch(
        "app.services.ingest.fetch_remotive",
        return_value=[_job("remotive", "1"), _job("remotive", "1b")],
    ), patch(
        "app.services.ingest.fetch_remoteok",
        return_value=[_job("remoteok", "2"), _job("remoteok", "2b")],
    ), patch(
        "app.services.ingest.fetch_arbeitnow",
        return_value=[_job("arbeitnow", "3"), _job("arbeitnow", "3b")],
    ):
        result = run_ingest(db)

    assert result["ingested"] == 6
    assert result["sources"]["synthetic"] == 0
    assert db.query(Job).count() == 6

    # Re-running with an updated title should update, not duplicate.
    with patch(
        "app.services.ingest.fetch_remotive",
        return_value=[_job("remotive", "1", title="Updated"), _job("remotive", "1b")],
    ), patch(
        "app.services.ingest.fetch_remoteok",
        return_value=[_job("remoteok", "2"), _job("remoteok", "2b")],
    ), patch(
        "app.services.ingest.fetch_arbeitnow",
        return_value=[_job("arbeitnow", "3"), _job("arbeitnow", "3b")],
    ):
        run_ingest(db)

    assert db.query(Job).count() == 6
    updated = db.query(Job).filter_by(source="remotive", source_id="1").one()
    assert updated.title == "Updated"


def test_run_ingest_falls_back_to_synthetic_when_sparse(client):
    from app.database import get_db
    import app.main as main_module

    db = next(main_module.app.dependency_overrides[get_db]())

    with patch("app.services.ingest.fetch_remotive", return_value=[]), \
         patch("app.services.ingest.fetch_remoteok", return_value=[]), \
         patch("app.services.ingest.fetch_arbeitnow", return_value=[]):
        result = run_ingest(db)

    assert result["sources"]["synthetic"] > 0
    assert result["ingested"] >= 20
