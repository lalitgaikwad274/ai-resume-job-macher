import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.ai_resume_assistant import (
    generate_resume_recommendations,
)

logger = logging.getLogger(__name__)

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

    except HTTPException:
        raise

    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        )

    except Exception as exc:
        logger.exception("AI recommendations failed: %s", exc)
        raise HTTPException(
            status_code=502,
            detail=f"Unable to generate AI recommendations: {str(exc)}",
        )
