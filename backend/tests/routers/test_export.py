import csv
import io
import json

from app.auth.jwt import create_access_token
from app.models import User


def _login(client, db):
    user = User(email="a@example.com", name="A", google_sub="sub-1")
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
