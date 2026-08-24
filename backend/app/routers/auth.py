from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.auth.deps import get_current_user
from app.auth.jwt import create_access_token
from app.auth.oauth import oauth
from app.config import settings
from app.database import get_db
from app.models import User

router = APIRouter(prefix="/auth")

COOKIE_MAX_AGE_SECONDS = 7 * 24 * 60 * 60


def session_cookie_attributes() -> dict:
    """Cookie flags for the session cookie.

    Deployed, the frontend and the backend sit on different registrable
    domains, so every authenticated call is a cross-site subresource request:
    the cookie only travels with SameSite=None, which browsers accept only
    alongside Secure. Locally both halves share localhost, where Lax works and
    Secure would stop the cookie being stored over plain http.
    """
    local = settings.is_local_frontend
    return {
        "samesite": "lax" if local else "none",
        "secure": not local,
    }


@router.get("/google/login")
async def google_login(request: Request):
    redirect_uri = str(request.url_for("google_callback"))
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/google/callback", name="google_callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):
    token = await oauth.google.authorize_access_token(request)
    profile = token.get("userinfo") or await oauth.google.parse_id_token(request, token)

    google_sub = profile["sub"]
    user = db.query(User).filter_by(google_sub=google_sub).one_or_none()
    if user is None:
        user = User(
            email=profile["email"], name=profile.get("name", ""), google_sub=google_sub
        )
        db.add(user)
    else:
        user.email = profile["email"]
        user.name = profile.get("name", user.name)
    db.commit()
    db.refresh(user)

    access_token = create_access_token(user_id=user.id)
    response = RedirectResponse(url=settings.frontend_url)
    response.set_cookie(
        key="session",
        value=access_token,
        httponly=True,
        max_age=COOKIE_MAX_AGE_SECONDS,
        **session_cookie_attributes(),
    )
    return response


@router.get("/me")
def me(user: User = Depends(get_current_user)):
    return {"id": user.id, "email": user.email, "name": user.name}


@router.post("/logout")
def logout():
    response = RedirectResponse(url=settings.frontend_url)
    # Browsers only drop a cookie when the clearing attributes match the ones
    # it was set with, so reuse the same samesite/secure pair here.
    response.delete_cookie(
        "session", httponly=True, **session_cookie_attributes()
    )
    return response
