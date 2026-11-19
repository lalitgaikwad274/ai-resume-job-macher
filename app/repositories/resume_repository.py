
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.resume import Resume


def create_resume(
    db: Session,
    user_id: int,
    filename: str,
    file_type: str,
    extracted_text: str,
):
    resume = Resume(
        user_id=user_id,
        filename=filename,
        file_type=file_type,
        extracted_text=extracted_text,
    )

    db.add(resume)
    db.commit()
    db.refresh(resume)

    return resume


def get_resume_by_id(
    db: Session,
    resume_id: int,
    user_id: int,
):
    statement = select(Resume).where(
        Resume.id == resume_id,
        Resume.user_id == user_id,
    )

    return db.scalar(statement)


def get_user_resumes(
    db: Session,
    user_id: int,
):
    statement = (
        select(Resume)
        .where(Resume.user_id == user_id)
        .order_by(Resume.created_at.desc())
    )

    return list(db.scalars(statement).all())


def update_resume(
    db: Session,
    resume: Resume,
    filename: str,
):
    resume.filename = filename

    db.commit()
    db.refresh(resume)

    return resume


def delete_resume(
    db: Session,
    resume: Resume,
):
    db.delete(resume)
    db.commit()
