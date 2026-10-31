
from pydantic import BaseModel, Field


class JobDescriptionRequest(BaseModel):
    job_title: str = Field(
        min_length=2,
        max_length=150
    )

    description: str = Field(
        min_length=30,
        max_length=20000
    )


class JobAnalysisResponse(BaseModel):
    job_title: str

    required_skills: dict[str, list[str]]

    preferred_skills: dict[str, list[str]]

    experience_years: float | None

    total_required_skills: int

    total_preferred_skills: int

    status: str
