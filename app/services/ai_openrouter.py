import json
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
from app.services.json_utils import repair_truncated_json
from app.services.promt import get_promt

load_dotenv()
logger = logging.getLogger(__name__)


def get_openrouter_client() -> AsyncOpenAI:
    api_key = os.getenv("OPEN_ROUTER_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="OPEN_ROUTER_API_KEY is not configured.",
        )
    return AsyncOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )


async def generate_openrouter_recommendations(
    resume_text: str,
    job_description: str,
) -> ResumeRecommendation:
    """Generate recommendations using OpenRouter."""
    client = get_openrouter_client()
    model = os.getenv("OPEN_ROUTER_MODEL", "meta-llama/llama-3.3-70b-instruct:free")
    max_tokens = int(os.getenv("OPEN_ROUTER_MAX_TOKENS", "4000"))

    system_prompt, user_prompt = get_promt(resume_text, job_description)

    try:
        response = await client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0.1,
            max_tokens=max_tokens,
            stream=False,
        )

        choice = response.choices[0]
        content = choice.message.content

        logger.info(
            "OpenRouter model=%s finish_reason=%s",
            response.model,
            choice.finish_reason,
        )

        if not content:
            raise HTTPException(
                status_code=502,
                detail="OpenRouter returned an empty response.",
            )
    
        if choice.finish_reason == "length":
            logger.warning("OpenRouter model hit token output limit (finish_reason='length'). Attempting salvage.")

        try:
            return ResumeRecommendation.model_validate_json(content)
        except Exception as parse_err:
            logger.warning("Standard JSON validation failed, attempting repair: %s", parse_err)
            repaired_data = repair_truncated_json(content)
            return ResumeRecommendation.model_validate(repaired_data)

    except HTTPException:
        raise

    except RateLimitError as exc:
        logger.exception("OpenRouter rate limit error: %s", exc)
        raise HTTPException(
            status_code=429,
            detail="OpenRouter rate limit exceeded. Please try again later.",
        )

    except APIStatusError as exc:
        logger.exception("OpenRouter API error: status=%s message=%s", exc.status_code, str(exc))
        raise HTTPException(
            status_code=502,
            detail=f"OpenRouter request failed with status {exc.status_code}.",
        )

    except APIConnectionError as exc:
        logger.exception("Could not connect to OpenRouter: %s", exc)
        raise HTTPException(
            status_code=503,
            detail="Could not connect to OpenRouter AI service.",
        )

    except Exception as exc:
        logger.exception("OpenRouter recommendation generation failed: %s", exc)
        raise HTTPException(
            status_code=500,
            detail="Failed to generate resume recommendations via OpenRouter.",
        )

