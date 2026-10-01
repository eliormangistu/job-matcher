from .base import BaseRequest


class JobAnalysisRequest(BaseRequest):
    job_id: int
    requirements: str
