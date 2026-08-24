import hmac

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.services.ingest import run_ingest

router = APIRouter()


@router.post("/ingest")
def ingest(
    db: Session = Depends(get_db),
    x_ingest_secret: str = Header(default=""),
):
    if not hmac.compare_digest(
        x_ingest_secret.encode("utf-8"), settings.ingest_secret.encode("utf-8")
    ):
        raise HTTPException(status_code=401, detail="Invalid ingest secret")
    return run_ingest(db)
