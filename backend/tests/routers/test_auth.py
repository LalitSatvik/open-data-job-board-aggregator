from app.auth.jwt import create_access_token
from app.models import User
from app.routers.auth import session_cookie_attributes


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
    import app.main as main_module
    from app.database import get_db

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


def test_local_cookie_is_lax_and_insecure(monkeypatch):
    from app.routers import auth as auth_module

    monkeypatch.setattr(
        auth_module.settings, "frontend_url", "http://localhost:3000"
    )
    assert session_cookie_attributes() == {"samesite": "lax", "secure": False}


def test_deployed_cookie_is_samesite_none_and_secure(monkeypatch):
    from app.routers import auth as auth_module

    monkeypatch.setattr(
        auth_module.settings, "frontend_url", "https://job-board.vercel.app"
    )
    assert session_cookie_attributes() == {"samesite": "none", "secure": True}


def test_logout_cookie_matches_the_attributes_it_was_set_with(client, monkeypatch):
    from app.routers import auth as auth_module

    monkeypatch.setattr(
        auth_module.settings, "frontend_url", "https://job-board.vercel.app"
    )
    response = client.post("/auth/logout", follow_redirects=False)
    set_cookie = response.headers.get("set-cookie", "").lower()
    assert "samesite=none" in set_cookie
    assert "secure" in set_cookie
