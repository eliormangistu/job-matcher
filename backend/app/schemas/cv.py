from pydantic import AliasChoices, BaseModel, Field

from app.schemas.match import JobMatch


class CvCandidateProfile(BaseModel):
    summary: str | None = None
    skills: list[str] = Field(default_factory=list)
    roles: list[str] = Field(
        default_factory=list,
        validation_alias=AliasChoices("roles", "job_titles"),
    )
    years_of_experience: float | None = None
    education: list[str] = Field(default_factory=list)
    languages: list[str] = Field(default_factory=list)
    industries: list[str] = Field(default_factory=list)

    @property
    def job_titles(self) -> list[str]:
        """Backward-compatible name for profiles generated before `roles`."""
        return self.roles


class CVUploadData(BaseModel):
    filename: str
    profile: CvCandidateProfile
    matches: list[JobMatch]
