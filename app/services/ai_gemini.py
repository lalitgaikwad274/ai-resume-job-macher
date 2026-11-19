import logging
import os

from dotenv import load_dotenv
from fastapi import HTTPException
from google import genai
from google.genai import types
from google.genai.errors import APIError, ServerError

from app.schemas.ai_recommendation import ResumeRecommendation
from app.services.json_utils import repair_truncated_json
from app.services.promt import get_promt

load_dotenv()
logger = logging.getLogger(__name__)


def get_gemini_client() -> genai.Client:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="GEMINI_API_KEY is not configured.",
        )
    return genai.Client(
        api_key=api_key,
        http_options=types.HttpOptions(
            api_version="v1beta"
        )
    )


async def generate_gemini_recommendations(
    resume_text: str,
    job_description: str,
) -> ResumeRecommendation:
    """Generate recommendations using Google Gemini."""
    client = get_gemini_client()
    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    max_output_tokens = int(os.getenv("GEMINI_MAX_OUTPUT_TOKENS", "8192"))

    system_prompt, user_prompt = get_promt(resume_text, job_description)

    try:
        response = await client.aio.models.generate_content(
            model=model,
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                response_mime_type="application/json",
                response_schema=ResumeRecommendation,
                temperature=0.1,
                max_output_tokens=max_output_tokens,
            ),
        )

        if response.parsed is not None:
            if isinstance(response.parsed, ResumeRecommendation):
                return response.parsed
            return ResumeRecommendation.model_validate(response.parsed)

        if not response.text:
            raise HTTPException(
                status_code=502,
                detail="Gemini returned an empty response.",
            )

        try:
            return ResumeRecommendation.model_validate_json(response.text)
        except Exception as parse_err:
            logger.warning("Standard JSON validation failed on Gemini response, attempting repair: %s", parse_err)
            repaired = repair_truncated_json(response.text)
            return ResumeRecommendation.model_validate(repaired)

    except HTTPException:
        raise

    except ServerError as exc:
        logger.exception("Gemini server error: %s", exc)
        if exc.code == 503:
            raise HTTPException(
                status_code=503,
                detail="Gemini service is temporarily busy. Please try again shortly.",
            )
        raise HTTPException(
            status_code=502,
            detail="Gemini service encountered a server error.",
        )

    except APIError as exc:
        logger.exception("Gemini API error: %s", exc)
        raise HTTPException(
            status_code=502,
            detail="Gemini API request failed.",
        )

    except Exception as exc:
        logger.exception("Gemini recommendation generation failed: %s", exc)
        raise HTTPException(
            status_code=500,
            detail="Failed to generate resume recommendations via Gemini.",
        )

