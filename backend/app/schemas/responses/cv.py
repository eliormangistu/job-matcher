from pydantic import AliasChoices, BaseModel, ConfigDict, Field
from datetime import datetime


class CVResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    filename: str
    file_type: str
    content: str | None
    summary: str | None
    skills: list[str]
    job_titles: list[str]
    years_of_experience: int | None
    education: list[str]
    languages: list[str]
    industries: list[str]
    created_at: datetime
    updated_at: datetime
