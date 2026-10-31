
import re

from app.data.skills import SKILLS_DATABASE


def normalize_text(text: str) -> str:
    """Normalize resume text."""

    text = text.lower()
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def extract_skills(text: str) -> dict:
    """Extract known skills from resume text."""

    normalized_text = normalize_text(text)

    extracted_skills = {}

    for category, skills in SKILLS_DATABASE.items():

        matched_skills = []

        for skill in skills:

            pattern = (
                r"(?<![a-z0-9])"
                + re.escape(skill)
                + r"(?![a-z0-9])"
            )

            if re.search(pattern, normalized_text):
                matched_skills.append(skill)

        if matched_skills:
            extracted_skills[category] = matched_skills

    return extracted_skills


def get_total_skills(extracted_skills: dict) -> int:
    """Count all extracted skills."""

    return sum(
        len(skills)
        for skills in extracted_skills.values()
    )
