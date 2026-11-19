
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ResumeResponse(BaseModel):
    id: int
    user_id: int
    filename: str
    file_type: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ResumeUpdate(BaseModel):
    filename: str | None = None
