import logging
import os

from dotenv import load_dotenv
from fastapi import HTTPException

from app.schemas.ai_recommendation import ResumeRecommendation
from app.services.ai_gemini import generate_gemini_recommendations
from app.services.ai_openai import generate_openai_recommendations
from app.services.ai_openrouter import generate_openrouter_recommendations

load_dotenv()
logger = logging.getLogger(__name__)


def get_default_provider() -> str:
    """Determine the active AI provider based on environment variables.

    Priority:
    1. AI_PROVIDER environment variable ('gemini', 'openai', 'openrouter')
    2. Available API keys (OPEN_ROUTER_API_KEY -> GEMINI_API_KEY -> OPENAI_API_KEY)
    3. Defaults to 'gemini'
    """
    configured = os.getenv("AI_PROVIDER", "").strip().lower()
    if configured:
        return configured

    if os.getenv("OPEN_ROUTER_API_KEY"):
        return "openrouter"
    if os.getenv("GEMINI_API_KEY"):
        return "gemini"
    if os.getenv("OPENAI_API_KEY"):
        return "openai"

    return "openrouter"


async def generate_resume_recommendations(
    resume_text: str,
    job_description: str,
    provider: str | None = None,
) -> ResumeRecommendation:
    """Generate structured resume recommendations using the chosen AI provider.

    Args:
        resume_text: Text extracted from the candidate's resume.
        job_description: Target job description text.
        provider: Optional provider name ('gemini', 'openai', 'openrouter').
                  If omitted, defaults to AI_PROVIDER or auto-detects from active API keys.

    Returns:
        ResumeRecommendation structured Pydantic object.
    """
    if not resume_text or not resume_text.strip():
        raise ValueError("Resume text cannot be empty.")

    if not job_description or not job_description.strip():
        raise ValueError("Job description cannot be empty.")

    if len(resume_text) > 15000:
        raise ValueError("Resume text is too long (max 15000 characters).")

    if len(job_description) > 15000:
        raise ValueError("Job description is too long (max 15000 characters).")

    selected_provider = "gemini"# (provider or get_default_provider()).strip().lower()

    logger.info("Using AI provider: %s", selected_provider)
    print("=============== ",selected_provider)
    if selected_provider in {"gemini", "google"}:
        return await generate_gemini_recommendations(
            resume_text=resume_text,
            job_description=job_description,
        )

    if selected_provider in {"openai", "gpt"}:
        return await generate_openai_recommendations(
            resume_text=resume_text,
            job_description=job_description,
        )

    if selected_provider in {"openrouter", "open_router"}:
        return await generate_openrouter_recommendations(
            resume_text=resume_text,
            job_description=job_description,
        )

    raise HTTPException(
        status_code=400,
        detail=(
            f"Unsupported AI provider '{selected_provider}'. "
            "Supported providers: 'gemini', 'openai', 'openrouter'."
        ),
    )


__all__ = [
    "generate_resume_recommendations",
    "generate_gemini_recommendations",
    "generate_openai_recommendations",
    "generate_openrouter_recommendations",
    "get_default_provider",
]
