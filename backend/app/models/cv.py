from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import DateTime, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.cv_match import CVMatch


class CV(Base):
    __tablename__ = "cvs"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        unique=True,
    )

    filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    file_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    content: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    skills: Mapped[list[str]] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )

    job_titles: Mapped[list[str]] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )

    years_of_experience: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    education: Mapped[list[str]] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )

    languages: Mapped[list[str]] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )

    industries: Mapped[list[str]] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="cvs",
    )

    matches: Mapped[list["CVMatch"]] = relationship(
        "CVMatch",
        back_populates="cv",
        cascade="all, delete-orphan",
    )
