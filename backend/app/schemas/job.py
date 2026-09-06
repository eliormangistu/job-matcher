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


class JobAnalysisRequest(BaseModel):
    job_id: int
    requirements: str


class JobAnalysisItem(BaseModel):
    job_id: int
    required_skills: list[str]


class JobAnalysisBatch(BaseModel):
    jobs: list[JobAnalysisItem]
