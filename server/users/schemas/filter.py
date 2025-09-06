from pydantic import BaseModel, Field


class ListUserFilter(BaseModel):
    page: int = Field(default=1, ge=1, description="Page number")
    per_page: int = Field(default=10, ge=1, le=100, description="Page number")
