import json
import logging

logger = logging.getLogger(__name__)


def repair_truncated_json(raw: str) -> dict:
    """Attempt to parse or salvage valid JSON if the model response was cut off mid-stream."""
    cleaned = raw.strip()

    # 1. Direct parse attempt
    try:
        return json.loads(cleaned)
    except Exception:
        pass

    # 2. Backtrack to the last valid completed object '}' and close open structures
    last_brace = cleaned.rfind("}")
    while last_brace > 0:
        candidate = cleaned[:last_brace + 1]
        open_brackets = candidate.count("[") - candidate.count("]")
        open_braces = candidate.count("{") - candidate.count("}")
        candidate += ("]" * max(0, open_brackets)) + ("}" * max(0, open_braces))
        try:
            return json.loads(candidate)
        except Exception:
            last_brace = cleaned.rfind("}", 0, last_brace)

    # 3. If cut off within the very first string / field before any inner object closed
    if '"' in cleaned:
        candidate = cleaned
        # If odd number of unescaped double quotes, close the quote
        unescaped_quotes = len([m for m in candidate.split('"')]) - 1
        if unescaped_quotes % 2 == 1:
            candidate += '"'
        open_brackets = candidate.count("[") - candidate.count("]")
        open_braces = candidate.count("{") - candidate.count("}")
        candidate += ("]" * max(0, open_brackets)) + ("}" * max(0, open_braces))
        try:
            return json.loads(candidate)
        except Exception:
            pass

    raise ValueError("Could not repair truncated JSON payload.")

