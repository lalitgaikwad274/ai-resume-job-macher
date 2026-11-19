
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db

from app.schemas.job import (
    JobCreate,
    JobResponse,
)

from app.repositories.job_repository import (
    create_job,
    get_user_jobs,
    get_job_by_id,
    delete_job,
)

router = APIRouter(
    prefix="/saved-jobs",
    tags=["Saved Jobs"],
)


@router.post("/", response_model=JobResponse)
def save_job(
    request: JobCreate,
    user_id: int,
    db: Session = Depends(get_db),
):
    return create_job(
        db,
        user_id,
        request.title,
        request.description,
    )


@router.get("/", response_model=list[JobResponse])
def list_jobs(
    user_id: int,
    db: Session = Depends(get_db),
):
    return get_user_jobs(db, user_id)


@router.delete("/{job_id}")
def remove_job(
    job_id: int,
    user_id: int,
    db: Session = Depends(get_db),
):
    job = get_job_by_id(
        db,
        job_id,
        user_id,
    )

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found.",
        )

    delete_job(db, job)

    return {
        "message": "Job deleted successfully.",
        "status": "success",
    }
