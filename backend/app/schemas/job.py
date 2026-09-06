from pydantic import BaseModel


class JobResponse(BaseModel):
    id: int
    title: str
    company: str
    location: list[str] | None
    remote: bool
    description: str | None
    url: str | None
    field: str | None
    company_industry: list[str] | None
    min_experience: int | None
    requirements: str | None
    required_skills: list[str]
    language_requirement: list[str] | None
    education_requirements: str | None
    posted: str | None


class JobAnalysis(BaseModel):
    required_skills: list[str]
