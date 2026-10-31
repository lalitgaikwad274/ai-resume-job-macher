
from fastapi import APIRouter

from app.schemas.matching import (
    ResumeJobMatchRequest
)

from app.services.job_matcher import (
    compare_skills,
    calculate_match_score
)


router = APIRouter(
    prefix="/matching",
    tags=["Job Matching"]
)


@router.post("/analyze")
async def match_resume(
    request: ResumeJobMatchRequest
):

    comparison = compare_skills(
        request.resume_skills,
        request.job_requirements
    )

    score = calculate_match_score(
        comparison
    )

    return {
        **score,
        **comparison,
        "status": "success"
    }
