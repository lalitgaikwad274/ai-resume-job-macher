
from pydantic import BaseModel, EmailStr, ConfigDict


class UserCreate(BaseModel):
    email: EmailStr
    full_name: str | None = None
    firebase_uid: str | None = None


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str | None

    model_config = ConfigDict(from_attributes=True)
