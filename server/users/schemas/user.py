from pydantic import BaseModel, UUID4


class UserRead(BaseModel):
    id: UUID4
    username: str
    is_active: bool
    is_deleted: bool

    class Config:
        from_attributes = True
