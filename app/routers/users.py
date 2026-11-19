
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db

from app.schemas.user import (
    UserCreate,
    UserResponse,
)

from app.repositories.user_repository import (
    create_user,
    get_user_by_email,
    get_user_by_id,
)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("/", response_model=UserResponse)
def register_user(
    request: UserCreate,
    db: Session = Depends(get_db),
):
    existing_user = get_user_by_email(
        db,
        request.email,
    )

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="User already exists.",
        )

    return create_user(
        db=db,
        email=request.email,
        full_name=request.full_name,
        firebase_uid=request.firebase_uid,
    )


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    user = get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found.",
        )

    return user
