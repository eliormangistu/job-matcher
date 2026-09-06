from sqlalchemy import String, Boolean, Text, Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(primary_key=True)

    airtable_id: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    job_id: Mapped[int | None] = mapped_column(Integer, nullable=True)

    title: Mapped[str] = mapped_column(String(255))
    company: Mapped[str] = mapped_column(String(255))

    location: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)

    remote: Mapped[bool] = mapped_column(Boolean, default=False)

    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    url: Mapped[str | None] = mapped_column(Text, nullable=True)

    field: Mapped[str | None] = mapped_column(String(255), nullable=True)

    company_industry: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)

    min_experience: Mapped[int | None] = mapped_column(Integer, nullable=True)

    requirements: Mapped[str | None] = mapped_column(Text, nullable=True)

    required_skills: Mapped[list[str]] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )

    language_requirement: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)

    education_requirements: Mapped[str | None] = mapped_column(Text, nullable=True)

    posted: Mapped[str | None] = mapped_column(String(100), nullable=True)
