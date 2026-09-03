from pydantic import BaseModel


class JobCreate(BaseModel):
    title: str
    company: str
    location: str
    remote: bool
    description: str
    url: str


class JobResponse(BaseModel):
    id: int
    title: str
    company: str
    location: str
    remote: bool
    description: str
    url: str