
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.ai_resume_assistant import (
    generate_resume_recommendations,
)

router = APIRouter(
    prefix="/ai",
    tags=["AI Recommendations"],
)


class AIRecommendationRequest(BaseModel):
    resume_text: str = Field(
        min_length=50,
        max_length=15000,
    )

    job_description: str = Field(
        min_length=30,
        max_length=15000,
    )


@router.post("/recommendations")
async def get_recommendations(
    request: AIRecommendationRequest,
):
    try:
        result = await generate_resume_recommendations(
            resume_text=request.resume_text,
            job_description=request.job_description,
        )
    
        return {
            "status": "success",
            "recommendations": result.model_dump(),
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        )

    except Exception:
        raise HTTPException(
            status_code=502,
            detail="Unable to generate AI recommendations.",
        )
