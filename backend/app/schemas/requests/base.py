from pydantic import BaseModel, ConfigDict


class BaseRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
