from fastapi import APIRouter, Depends, Query
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.auth.deps import get_current_user
from app.database import get_db
from app.models import Application, User
from app.routers.applications import serialize_application
from app.services.export import to_csv, to_json

router = APIRouter()


@router.get("/export")
def export_applications(
    format: str = Query(default="json", pattern="^(json|csv)$"),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    applications = (
        db.query(Application)
        .filter_by(user_id=user.id)
        .order_by(Application.updated_at.desc())
        .all()
    )
    serialized = [serialize_application(a, db) for a in applications]

    if format == "csv":
        body = to_csv(serialized)
        media_type = "text/csv"
        filename = "applications.csv"
    else:
        body = to_json(serialized)
        media_type = "application/json"
        filename = "applications.json"

    return Response(
        content=body,
        media_type=media_type,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
