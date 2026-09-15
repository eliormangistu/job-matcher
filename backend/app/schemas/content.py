from typing import Any

from pydantic import BaseModel


class ContentResponse(BaseModel):
    homepage: dict[str, Any]
    jobspage: dict[str, Any]
    cvpage: dict[str, Any]
    matchpage: dict[str, Any]
    errorpage: dict[str, Any]
    loaderpage: dict[str, Any]
    header: dict[str, Any]
    footer: dict[str, Any]
