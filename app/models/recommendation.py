
from datetime import datetime

from sqlalchemy import (
    String,
    Text,
    DateTime,
    ForeignKey,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Recommendation(Base):

    __tablename__ = "recommendations"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    analysis_id: Mapped[int] = mapped_column(
        ForeignKey(
            "resume_analyses.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    recommendation_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    analysis: Mapped["ResumeAnalysis"] = relationship(
        back_populates="recommendations",
    )
