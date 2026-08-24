from app.models import Application, ApplicationStatus, Job, StatusHistory, User


def test_create_user_job_application_history(client):
    from app.database import SessionLocal  # noqa: F401 (ensures import works)
    import app.main as main_module
    from app.database import get_db

    db = next(main_module.app.dependency_overrides[get_db]())

    user = User(email="a@example.com", name="A", google_sub="sub-1")
    db.add(user)
    db.commit()
    db.refresh(user)

    job = Job(
        source="remotive",
        source_id="123",
        title="Engineer",
        company="Acme",
        remote=True,
        url="https://example.com/job/123",
    )
    db.add(job)
    db.commit()
    db.refresh(job)

    application = Application(
        user_id=user.id, job_id=job.id, status=ApplicationStatus.SAVED.value
    )
    db.add(application)
    db.commit()
    db.refresh(application)

    history = StatusHistory(
        application_id=application.id,
        from_status=None,
        to_status=ApplicationStatus.SAVED.value,
    )
    db.add(history)
    db.commit()

    assert application.user_id == user.id
    assert application.job_id == job.id
    assert application.status == "saved"
    assert db.query(StatusHistory).count() == 1
