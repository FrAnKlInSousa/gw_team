from pydantic import BaseModel, Field


class Filter(BaseModel):
    limit: int = Field(default=10, ge=0)
    page: int = Field(default=0, ge=0)
