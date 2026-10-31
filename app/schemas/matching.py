
from pydantic import BaseModel, Field


class ResumeJobMatchRequest(BaseModel):

    resume_skills: dict[str, list[str]]

    job_requirements: dict = Field(
        description="Required and preferred job skills"
    )
