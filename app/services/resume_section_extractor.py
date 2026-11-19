import re
from typing import Dict


SECTION_ALIASES = {
    "contact": [
        "contact",
        "contact information",
        "personal details",
    ],
    "summary": [
        "summary",
        "professional summary",
        "profile",
        "objective",
    ],
    "skills": [
        "skills",
        "technical skills",
        "ai & llm",
        "backend",
        "tools",
        "also",
    ],
    "education": [
        "education",
        "academic qualification",
        "educational background",
    ],
    "experience": [
        "work experience",
        "professional experience",
        "employment history",
        "experience",
    ],
    "projects": [
        "projects",
        "personal projects",
        "key projects",
    ],
    "certifications": [
        "certifications",
        "awards & certificates",
        "awards and certificates",
        "achievements",
    ],
}


def normalize_heading(text: str) -> str | None:
    """Identify whether a line is a resume section heading."""

    cleaned = text.strip().lower()

    for section, aliases in SECTION_ALIASES.items():
        if cleaned in aliases:
            return section

    return None


def extract_resume_sections(text: str) -> Dict[str, str]:
    """
    Extract resume content section by section.
    """

    sections = {}
    current_section = "other"

    for line in text.splitlines():

        line = line.strip()

        if not line:
            continue

        heading = normalize_heading(line)

        if heading:
            current_section = heading

            if current_section not in sections:
                sections[current_section] = ""

            continue

        sections.setdefault(current_section, "")

        sections[current_section] += line + "\n"

    return {
        section: content.strip()
        for section, content in sections.items()
    }