from pydantic import BaseModel, Field


class FilterPage(BaseModel):
    limit: int = Field(default=10, ge=0)
    page: int = Field(default=0, ge=0)


class FilterUser(FilterPage):
    name: str | None = Field(default=None, min_length=3)
