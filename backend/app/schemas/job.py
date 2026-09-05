from pydantic import BaseModel, Field




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
    language_requirement: list[str] | None
    education_requirements: str | None
    salary: str | None
    point_of_contact: str | None
    linkedin: str | None
    email: str | None
    phone: str | None
    posted: str | None