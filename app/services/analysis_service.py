
from app.services.resume_section_extractor import extract_resume_sections
from app.services.resume_parser import extract_resume_text

from app.services.skill_extractor import (
    extract_skills,
    get_total_skills,
)

from app.services.resume_analyzer import (
    extract_experience,
    extract_education,
)

from app.services.job_analyzer import (
    analyze_job_description,
)

from app.services.job_matcher import (
    compare_skills,
    calculate_match_score,
)

from app.services.text_similarity import (
    calculate_text_similarity,
)

from app.services.ai_resume_assistant import (
    generate_resume_recommendations,
)


async def analyze_complete_resume(
    filename: str,
    file_bytes: bytes,
    job_title: str,
    job_description: str,
    include_ai: bool = True,
) -> dict:

    # STEP 1: Extract resume text
    resume_text = extract_resume_text(
        filename,
        file_bytes,
    )

    resume_sections = extract_resume_sections(
        resume_text
    )
    print(resume_sections["education"], resume_sections["experience"])
    if not resume_text:
        raise ValueError("No readable resume text found.")

    # STEP 2: Extract candidate information
    candidate_skills = extract_skills(
        resume_text
    )

    experience = extract_experience(
        resume_sections["experience"]
    )
    print("experience",experience)
    education = extract_education(
        resume_sections["education"]
    )
    print("education", education)
    # STEP 3: Analyze job description
    job_analysis = analyze_job_description(
        job_description
    )

    # STEP 4: Compare candidate and job skills
    comparison = compare_skills(
        candidate_skills,
        job_analysis,
    )

    match_score = calculate_match_score(
        comparison
    )

    # STEP 5: Calculate text similarity
    text_similarity = calculate_text_similarity(
        resume_text,
        job_description,
    )

    # STEP 6: Generate AI recommendations
    ai_recommendations = None

    if include_ai:
        ai_result = await generate_resume_recommendations(
            resume_text=resume_text,
            job_description=job_description,
        )

        ai_recommendations = ai_result.model_dump()

    # STEP 7: Return complete report
    return {
        "job_title": job_title,

        "resume_analysis": {
            "filename": filename,
            "word_count": len(resume_text.split()),
            "character_count": len(resume_text),
            "skills": candidate_skills,
            "total_skills": get_total_skills(
                candidate_skills
            ),
            "experience_mentions": experience,
            "education": education,
        },

        "job_analysis": job_analysis,

        "match_analysis": {
            **match_score,
            **comparison,
        },

        "text_similarity": text_similarity,

        "ai_recommendations": ai_recommendations,

        "status": "success",
    }
