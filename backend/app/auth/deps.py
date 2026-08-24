from fastapi import Cookie, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.jwt import decode_access_token
from app.database import get_db
from app.models import User


def get_current_user(
    session: str = Cookie(default=None),
    db: Session = Depends(get_db),
) -> User:
    user_id = decode_access_token(session) if session else None
    if user_id is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    user = db.query(User).filter_by(id=user_id).one_or_none()
    if user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user
