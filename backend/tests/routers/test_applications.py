from app.auth.jwt import create_access_token
from app.models import Job, User


def _login(client, db, email="a@example.com", name="A", google_sub="sub-1"):
    user = User(email=email, name=name, google_sub=google_sub)
    db.add(user)
    db.commit()
    db.refresh(user)
    client.cookies.set("session", create_access_token(user_id=user.id))
    return user


def _get_db(main_module):
    from app.database import get_db

    return next(main_module.app.dependency_overrides[get_db]())


def test_create_and_list_applications(client):
    import app.main as main_module

    db = _get_db(main_module)
    _login(client, db)

    job = Job(source="remotive", source_id="1", title="Engineer",
              company="Acme", url="https://x.test/1")
    db.add(job)
    db.commit()
    db.refresh(job)

    response = client.post("/applications", json={"job_id": job.id, "status": "saved"})
    assert response.status_code == 201
    body = response.json()
    assert body["status"] == "saved"
    assert len(body["history"]) == 1
    assert body["history"][0]["from_status"] is None
    assert body["history"][0]["to_status"] == "saved"

    response = client.get("/applications")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_patch_status_appends_history(client):
    import app.main as main_module

    db = _get_db(main_module)
    _login(client, db)

    create = client.post("/applications", json={"status": "saved", "notes": "n/a"})
    app_id = create.json()["id"]

    response = client.patch(f"/applications/{app_id}", json={"status": "applied"})
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "applied"
    assert len(body["history"]) == 2
    assert body["history"][-1]["from_status"] == "saved"
    assert body["history"][-1]["to_status"] == "applied"


def test_cannot_access_another_users_application(client):
    import app.main as main_module

    db = _get_db(main_module)
    _login(client, db)
    create = client.post("/applications", json={"status": "saved"})
    app_id = create.json()["id"]

    other = User(email="b@example.com", name="B", google_sub="sub-2")
    db.add(other)
    db.commit()
    db.refresh(other)
    client.cookies.set("session", create_access_token(user_id=other.id))

    response = client.patch(f"/applications/{app_id}", json={"status": "applied"})
    assert response.status_code == 404


def test_list_only_returns_the_current_users_applications(client):
    import app.main as main_module

    db = _get_db(main_module)

    _login(client, db, email="a@example.com", google_sub="sub-1")
    client.post("/applications", json={"status": "saved", "notes": "mine"})

    _login(client, db, email="b@example.com", name="B", google_sub="sub-2")
    client.post("/applications", json={"status": "applied", "notes": "theirs"})

    # Back to user A: their list must not leak user B's application.
    user_a = db.query(User).filter_by(email="a@example.com").one()
    client.cookies.set("session", create_access_token(user_id=user_a.id))

    body = client.get("/applications").json()
    assert len(body) == 1
    assert body[0]["notes"] == "mine"


def test_applications_require_a_session(client):
    assert client.get("/applications").status_code == 401


def test_create_rejects_an_invalid_status(client):
    import app.main as main_module

    db = _get_db(main_module)
    _login(client, db)

    response = client.post("/applications", json={"status": "ghosted"})
    assert response.status_code == 422


def test_patch_rejects_an_invalid_status(client):
    import app.main as main_module

    db = _get_db(main_module)
    _login(client, db)
    app_id = client.post("/applications", json={"status": "saved"}).json()["id"]

    response = client.patch(f"/applications/{app_id}", json={"status": "ghosted"})
    assert response.status_code == 422


def test_delete_application(client):
    import app.main as main_module

    db = _get_db(main_module)
    _login(client, db)
    create = client.post("/applications", json={"status": "saved"})
    app_id = create.json()["id"]

    response = client.delete(f"/applications/{app_id}")
    assert response.status_code == 204
    assert client.get("/applications").json() == []
