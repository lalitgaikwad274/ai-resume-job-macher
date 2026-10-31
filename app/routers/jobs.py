
from fastapi import APIRouter

from app.schemas.job import (
    JobDescriptionRequest,
)

from app.services.job_analyzer import (
    analyze_job_description,
)

router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"],
)


@router.post("/analyze")
async def analyze_job(
    request: JobDescriptionRequest
):

    analysis = analyze_job_description(
        request.description
    )

    return {
        "job_title": request.job_title,
        **analysis,
        "status": "success",
    }
