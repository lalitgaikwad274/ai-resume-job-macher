
import re

from app.data.skills import SKILLS_DATABASE


def extract_job_skills(text: str) -> dict:
    """Extract known skills from job description."""

    normalized_text = text.lower()

    extracted = {}

    for category, skills in SKILLS_DATABASE.items():

        matched = []

        for skill in skills:

            pattern = (
                r"(?<![a-z0-9])"
                + re.escape(skill)
                + r"(?![a-z0-9])"
            )

            if re.search(pattern, normalized_text):
                matched.append(skill)

        if matched:
            extracted[category] = matched

    return extracted


def extract_experience_requirement(
    text: str
) -> float | None:
    """Extract years of experience required."""

    patterns = [
        r"(\d+(?:\.\d+)?)\+?\s*years?\s+of\s+experience",
        r"(\d+(?:\.\d+)?)\+?\s*years?\s+experience",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            return float(match.group(1))

    return None


def extract_preferred_section(text: str) -> str:
    """Extract the preferred skills section."""

    match = re.search(
        r"(?:preferred|nice to have|good to have|bonus skills)"
        r"\s*:?\s*(.*?)(?=\n\s*(?:responsibilities|"
        r"what you will do|about us|benefits|education)\s*:|$)",
        text,
        re.IGNORECASE | re.DOTALL,
    )

    if match:
        return match.group(1)

    return ""


def analyze_job_description(text: str) -> dict:
    """Analyze required and preferred skills."""

    preferred_text = extract_preferred_section(text)

    all_skills = extract_job_skills(text)

    preferred_skills = extract_job_skills(
        preferred_text
    )

    required_skills = {}

    for category, skills in all_skills.items():

        preferred = preferred_skills.get(
            category,
            []
        )

        required = [
            skill
            for skill in skills
            if skill not in preferred
        ]

        if required:
            required_skills[category] = required

    total_required = sum(
        len(skills)
        for skills in required_skills.values()
    )

    total_preferred = sum(
        len(skills)
        for skills in preferred_skills.values()
    )

    return {
        "required_skills": required_skills,
        "preferred_skills": preferred_skills,
        "experience_years": (
            extract_experience_requirement(text)
        ),
        "total_required_skills": total_required,
        "total_preferred_skills": total_preferred,
    }
