
from datetime import datetime

from sqlalchemy import (
    Integer,
    Float,
    String,
    JSON,
    DateTime,
    ForeignKey,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class ResumeAnalysis(Base):

    __tablename__ = "resume_analyses"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    resume_id: Mapped[int] = mapped_column(
        ForeignKey("resumes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    job_description_id: Mapped[int] = mapped_column(
        ForeignKey(
            "job_descriptions.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    match_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    text_similarity: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    report: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="completed",
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    resume: Mapped["Resume"] = relationship(
        back_populates="analyses",
    )

    job_description: Mapped["JobDescription"] = relationship(
        back_populates="analyses",
    )

    recommendations: Mapped[list["Recommendation"]] = relationship(
        back_populates="analysis",
        cascade="all, delete-orphan",
    )
