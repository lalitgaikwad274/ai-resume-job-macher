
from pydantic import BaseModel, Field


class ResumeStrength(BaseModel):
    title: str
    explanation: str


class ResumeWeakness(BaseModel):
    title: str
    explanation: str
    improvement: str


class BulletImprovement(BaseModel):
    original: str
    improved: str
    explanation: str


class SkillRecommendation(BaseModel):
    skill: str
    reason: str
    priority: str


class ResumeRecommendation(BaseModel):
    overall_feedback: str

    strengths: list[ResumeStrength]

    weaknesses: list[ResumeWeakness]

    missing_skills: list[SkillRecommendation]

    bullet_improvements: list[BulletImprovement]

    ats_recommendations: list[str]
