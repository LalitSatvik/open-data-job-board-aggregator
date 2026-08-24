import csv
import io
import json

from app.auth.jwt import create_access_token
from app.models import User


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


def test_export_json_includes_history(client):
    import app.main as main_module

    db = _get_db(main_module)
    _login(client, db)
    create = client.post("/applications", json={"status": "saved"})
    app_id = create.json()["id"]
    client.patch(f"/applications/{app_id}", json={"status": "applied"})

    response = client.get("/export", params={"format": "json"})
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")
    data = json.loads(response.content)
    assert len(data) == 1
    assert len(data[0]["history"]) == 2


def test_export_requires_a_session(client):
    assert client.get("/export", params={"format": "json"}).status_code == 401


def test_export_only_includes_the_current_users_applications(client):
    import app.main as main_module

    db = _get_db(main_module)

    _login(client, db, email="a@example.com", google_sub="sub-1")
    client.post("/applications", json={"status": "saved", "notes": "mine"})

    _login(client, db, email="b@example.com", name="B", google_sub="sub-2")
    client.post("/applications", json={"status": "applied", "notes": "theirs"})

    user_a = db.query(User).filter_by(email="a@example.com").one()
    client.cookies.set("session", create_access_token(user_id=user_a.id))

    response = client.get("/export", params={"format": "json"})
    assert response.status_code == 200
    data = json.loads(response.content)
    assert len(data) == 1
    assert data[0]["notes"] == "mine"
    assert "theirs" not in response.content.decode()


def test_export_csv_has_history_column(client):
    import app.main as main_module

    db = _get_db(main_module)
    _login(client, db)
    create = client.post("/applications", json={"status": "saved"})
    app_id = create.json()["id"]
    client.patch(f"/applications/{app_id}", json={"status": "applied"})

    response = client.get("/export", params={"format": "csv"})
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/csv")

    rows = list(csv.DictReader(io.StringIO(response.content.decode())))
    assert len(rows) == 1
    assert "saved" in rows[0]["history"]
    assert "applied" in rows[0]["history"]
