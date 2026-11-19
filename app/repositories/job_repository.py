
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.job_description import JobDescription


def create_job(
    db: Session,
    user_id: int,
    title: str,
    description: str,
):
    job = JobDescription(
        user_id=user_id,
        title=title,
        description=description,
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return job


def get_user_jobs(
    db: Session,
    user_id: int,
):
    statement = (
        select(JobDescription)
        .where(JobDescription.user_id == user_id)
        .order_by(JobDescription.created_at.desc())
    )

    return list(db.scalars(statement).all())


def get_job_by_id(
    db: Session,
    job_id: int,
    user_id: int,
):
    statement = select(JobDescription).where(
        JobDescription.id == job_id,
        JobDescription.user_id == user_id,
    )

    return db.scalar(statement)


def delete_job(
    db: Session,
    job: JobDescription,
):
    db.delete(job)
    db.commit()
