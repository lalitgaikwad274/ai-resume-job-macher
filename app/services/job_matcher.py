
def flatten_skills(skills: dict) -> set:
    """
    Convert categorized skills into a single set.
    """

    result = set()

    for category_skills in skills.values():
        for skill in category_skills:
            result.add(skill.lower().strip())

    return result


def compare_skills(
    resume_skills: dict,
    job_skills: dict
) -> dict:
    """
    Compare resume skills with job skills.
    """

    resume = flatten_skills(resume_skills)
    required = flatten_skills(
        job_skills.get("required_skills", {})
    )
    preferred = flatten_skills(
        job_skills.get("preferred_skills", {})
    )

    # Returns skills present in both sets (intersection).
    matched_required = sorted(resume & required) 

    # Returns skills required by the job but missing from the resume (difference).
    missing_required = sorted(required - resume)

    matched_preferred = sorted(resume & preferred)
    missing_preferred = sorted(preferred - resume)

    return {
        "matched_required": matched_required,
        "missing_required": missing_required,
        "matched_preferred": matched_preferred,
        "missing_preferred": missing_preferred,
        "required_total": len(required),
        "preferred_total": len(preferred),
    }


def calculate_coverage(
    matched: list,
    total: int
) -> float:
    """
    Calculate percentage coverage.
    """

    if total == 0:
        return 0.0

    return round(
        (len(matched) / total) * 100,
        2
    )


def calculate_match_score(
    comparison: dict
) -> dict:
    """
    Calculate weighted match percentage.
    """

    required_coverage = calculate_coverage(
        comparison["matched_required"],
        comparison["required_total"]
    )

    preferred_coverage = calculate_coverage(
        comparison["matched_preferred"],
        comparison["preferred_total"]
    )

    if comparison["required_total"] == 0:
        return {
            "match_score": 0.0,
            "required_coverage": required_coverage,
            "preferred_coverage": preferred_coverage,
        }

    if comparison["preferred_total"] == 0:
        final_score = required_coverage
    else:
        final_score = (
            required_coverage * 0.8
            + preferred_coverage * 0.2
        )

    return {
        "match_score": round(final_score, 2),
        "required_coverage": required_coverage,
        "preferred_coverage": preferred_coverage,
    }
