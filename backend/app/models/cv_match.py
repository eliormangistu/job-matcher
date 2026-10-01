from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Float, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base

if TYPE_CHECKING:
    from app.models.cv import CV
    from app.models.job import Job


class CVMatch(Base):
    __tablename__ = "cv_matches"

    id: Mapped[int] = mapped_column(primary_key=True)

    cv_id: Mapped[int] = mapped_column(
        ForeignKey("cvs.id"),
        nullable=False,
    )

    job_id: Mapped[int] = mapped_column(
        ForeignKey("jobs.id"),
        nullable=False,
    )

    score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    matched_skills: Mapped[list[str]] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )

    missing_skills: Mapped[list[str]] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    cv: Mapped["CV"] = relationship(
        "CV",
        back_populates="matches",
    )

    job: Mapped["Job"] = relationship(
        "Job",
    )
