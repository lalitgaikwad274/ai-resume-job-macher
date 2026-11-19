
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
    overall_feedback: str | None = None

    strengths: list[ResumeStrength] = Field(default_factory=list)

    weaknesses: list[ResumeWeakness] = Field(default_factory=list)

    missing_skills: list[SkillRecommendation] = Field(default_factory=list)

    bullet_improvements: list[BulletImprovement] = Field(default_factory=list)

    ats_recommendations: list[str] = Field(default_factory=list)
