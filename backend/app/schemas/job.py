from pydantic import BaseModel


class JobAnalysisItem(BaseModel):
    job_id: int
    required_skills: list[str]


class JobAnalysisBatch(BaseModel):
    jobs: list[JobAnalysisItem]
