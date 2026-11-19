import logging
import os

from dotenv import load_dotenv
from fastapi import HTTPException
from openai import (
    APIConnectionError,
    APIStatusError,
    AsyncOpenAI,
    RateLimitError,
)

from app.schemas.ai_recommendation import ResumeRecommendation
from app.services.promt import get_promt

load_dotenv()
logger = logging.getLogger(__name__)


def get_openai_client() -> AsyncOpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="OPENAI_API_KEY is not configured.",
        )
    return AsyncOpenAI(api_key=api_key)


async def generate_openai_recommendations(
    resume_text: str,
    job_description: str,
) -> ResumeRecommendation:
    """Generate recommendations using OpenAI."""
    client = get_openai_client()
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", "4000"))

    system_prompt, user_prompt = get_promt(resume_text, job_description)

    try:
        response = await client.beta.chat.completions.parse(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            response_format=ResumeRecommendation,
            temperature=0.1,
            max_tokens=max_tokens,
        )

        message = response.choices[0].message

        if message.refusal:
            raise HTTPException(
                status_code=422,
                detail=f"OpenAI refused request: {message.refusal}",
            )

        if message.parsed is None:
            raise HTTPException(
                status_code=502,
                detail="OpenAI returned an empty response.",
            )

        return message.parsed

    except HTTPException:
        raise

    except RateLimitError as exc:
        logger.exception("OpenAI rate limit error: %s", exc)
        raise HTTPException(
            status_code=429,
            detail="OpenAI rate limit exceeded. Please try again later.",
        )

    except APIStatusError as exc:
        logger.exception("OpenAI API status error: status=%s message=%s", exc.status_code, exc.message)
        raise HTTPException(
            status_code=502,
            detail=f"OpenAI request failed with status {exc.status_code}.",
        )

    except APIConnectionError as exc:
        logger.exception("OpenAI connection error: %s", exc)
        raise HTTPException(
            status_code=503,
            detail="Could not connect to OpenAI service.",
        )

    except Exception as exc:
        logger.exception("OpenAI recommendation generation failed: %s", exc)
        raise HTTPException(
            status_code=500,
            detail="Failed to generate resume recommendations via OpenAI.",
        )

