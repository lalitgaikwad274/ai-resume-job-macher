
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class JobDescriptionRequest(BaseModel):
    job_title: str = Field(
        min_length=2,
        max_length=150
    )

    description: str = Field(
        min_length=30,
        max_length=20000
    )

class JobCreate(BaseModel):
    title: str = Field(min_length=2, max_length=150)
    description: str = Field(min_length=30, max_length=20000)


class JobResponse(BaseModel):
    id: int
    user_id: int
    title: str
    description: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
