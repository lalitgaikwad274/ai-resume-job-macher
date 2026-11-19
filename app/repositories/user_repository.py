
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


def create_user(
    db: Session,
    email: str,
    full_name: str | None = None,
    firebase_uid: str | None = None,
):
    user = User(
        email=email,
        full_name=full_name,
        firebase_uid=firebase_uid,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def get_user_by_id(
    db: Session,
    user_id: int,
):
    statement = select(User).where(
        User.id == user_id
    )

    return db.scalar(statement)


def get_user_by_email(
    db: Session,
    email: str,
):
    statement = select(User).where(
        User.email == email
    )

    return db.scalar(statement)
