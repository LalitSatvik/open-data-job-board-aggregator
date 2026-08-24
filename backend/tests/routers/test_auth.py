from app.auth.jwt import create_access_token
from app.models import User


def _create_user(db):
    user = User(email="a@example.com", name="A", google_sub="sub-1")
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def test_me_requires_session_cookie(client):
    response = client.get("/auth/me")
    assert response.status_code == 401


def test_me_returns_current_user(client):
    from app.database import get_db
    import app.main as main_module

    db = next(main_module.app.dependency_overrides[get_db]())
    user = _create_user(db)
    token = create_access_token(user_id=user.id)

    client.cookies.set("session", token)
    response = client.get("/auth/me")

    assert response.status_code == 200
    assert response.json()["email"] == "a@example.com"


def test_logout_clears_cookie(client):
    response = client.post("/auth/logout", follow_redirects=False)
    assert response.status_code in (302, 307)
    assert "session=" in response.headers.get("set-cookie", "")
