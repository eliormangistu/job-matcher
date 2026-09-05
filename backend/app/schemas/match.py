from pydantic import BaseModel

from app.schemas.job import JobResponse


class MatchResult(BaseModel):
    job_id: int
    score: float
    matched_skills: list[str]
    missing_skills: list[str]
    job: JobResponse


JobMatch = MatchResult
