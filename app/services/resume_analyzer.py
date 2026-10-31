
import re


def extract_experience(text: str) -> list:
    """Find experience duration mentions."""

    patterns = [
        r"(\d+(?:\.\d+)?)\+?\s*years?\s+of\s+experience",
        r"(\d+(?:\.\d+)?)\+?\s*years?\s+experience",
    ]

    matches = []

    for pattern in patterns:
        found = re.findall(
            pattern,
            text,
            re.IGNORECASE
        )
        matches.extend(found)

    return list(dict.fromkeys(matches))


def extract_education(text: str) -> list:
    """Find common education qualifications."""

    qualifications = [
        "bachelor of technology",
        "bachelor of engineering",
        "master of technology",
        "master of computer applications",
        "bachelor of computer applications",
        "bachelor of science",
        "master of science",
        "mba",
        "b.tech",
        "m.tech",
        "b.e.",
        "bca",
        "mca",
        "b.sc",
        "m.sc",
    ]

    normalized_text = text.lower()

    return [
        qualification
        for qualification in qualifications
        if re.search(
            r"(?<![a-z0-9])"
            + re.escape(qualification)
            + r"(?![a-z0-9])",
            normalized_text,
        )
    ]
