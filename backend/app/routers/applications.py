from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.auth.deps import get_current_user
from app.database import get_db
from app.models import Application, ApplicationStatus, Job, StatusHistory, User

router = APIRouter()


class ApplicationCreate(BaseModel):
    job_id: Optional[int] = None
    status: ApplicationStatus = ApplicationStatus.SAVED
    notes: Optional[str] = None


class ApplicationUpdate(BaseModel):
    status: Optional[ApplicationStatus] = None
    notes: Optional[str] = None


def _serialize_job(job: Optional[Job]) -> Optional[dict]:
    if job is None:
        return None
    return {
        "id": job.id,
        "title": job.title,
        "company": job.company,
        "url": job.url,
    }


def serialize_application(application: Application, db: Session) -> dict:
    history = (
        db.query(StatusHistory)
        .filter_by(application_id=application.id)
        .order_by(StatusHistory.changed_at.asc())
        .all()
    )
    return {
        "id": application.id,
        "job": _serialize_job(application.job),
        "job_id": application.job_id,
        "status": application.status,
        "notes": application.notes,
        "created_at": application.created_at,
        "updated_at": application.updated_at,
        "history": [
            {
                "from_status": h.from_status,
                "to_status": h.to_status,
                "changed_at": h.changed_at,
            }
            for h in history
        ],
    }


def _get_owned_application(
    application_id: int, user: User, db: Session
) -> Application:
    application = (
        db.query(Application)
        .filter_by(id=application_id, user_id=user.id)
        .one_or_none()
    )
    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return application


@router.get("/applications")
def list_applications(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    applications = (
        db.query(Application)
        .filter_by(user_id=user.id)
        .order_by(Application.updated_at.desc())
        .all()
    )
    return [serialize_application(a, db) for a in applications]


@router.post("/applications", status_code=201)
def create_application(
    payload: ApplicationCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    application = Application(
        user_id=user.id,
        job_id=payload.job_id,
        status=payload.status.value,
        notes=payload.notes,
    )
    db.add(application)
    # Flush (not commit) so the application gets its id while the initial
    # history row still lands in the same transaction: an application without
    # its opening history row would break the whole history feature.
    db.flush()

    db.add(
        StatusHistory(
            application_id=application.id,
            from_status=None,
            to_status=payload.status.value,
        )
    )
    db.commit()
    db.refresh(application)

    return serialize_application(application, db)


@router.patch("/applications/{application_id}")
def update_application(
    application_id: int,
    payload: ApplicationUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    application = _get_owned_application(application_id, user, db)

    if payload.notes is not None:
        application.notes = payload.notes

    if payload.status is not None and payload.status.value != application.status:
        db.add(
            StatusHistory(
                application_id=application.id,
                from_status=application.status,
                to_status=payload.status.value,
            )
        )
        application.status = payload.status.value

    db.commit()
    db.refresh(application)
    return serialize_application(application, db)


@router.delete("/applications/{application_id}", status_code=204)
def delete_application(
    application_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    application = _get_owned_application(application_id, user, db)
    db.query(StatusHistory).filter_by(application_id=application.id).delete()
    db.delete(application)
    db.commit()
    return None
