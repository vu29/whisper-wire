from pydantic import BaseModel, UUID4, AwareDatetime


class UserRead(BaseModel):
    id: UUID4
    username: str
    is_active: bool
    is_deleted: bool
    created_at: AwareDatetime

    class Config:
        from_attributes = True
