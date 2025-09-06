from typing import Annotated

from fastapi import APIRouter, HTTPException
from fastapi.params import Query
from pydantic import UUID4

from server.core.dependencies import DBSessionDep
from server.users.models.user import User
from server.users.schemas.filter import ListUserFilter
from server.users.schemas.user import UserRead
from server.users.services import user_service

router = APIRouter(tags=["Users"])


@router.get("/users")
async def list_users(
        db: DBSessionDep,
        filter_: Annotated[ListUserFilter, Query()]
) -> list[UserRead]:
    users: list[User] = await user_service.list_users(db, filter_)
    return [UserRead.model_validate(user) for user in users]

@router.get("/users/{user_id}")
async def get_user(
        db: DBSessionDep,
        user_id: UUID4
) -> UserRead:
    user: User | None = await user_service.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserRead.model_validate(user)


