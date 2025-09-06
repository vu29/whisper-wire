from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from server.core.security import hash_password
from server.users.exceptions import UserExistsException
from server.users.models.user import User
from server.users.schemas.filter import ListUserFilter


__all__ = [
    "create_user",
    "get_user",
    "list_users",
]


async def create_user(
        db: AsyncSession,
        username: str,
        password: str
) -> User:
    query = select(User.id).where(User.username == username)
    result = await db.execute(query)
    if result.scalars().first():
        raise UserExistsException("User with this username already exists")
    new_user = User(username=username, password_hash=hash_password(password))
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def get_user(
        db: AsyncSession,
        user_id: UUID
) -> User | None:
    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    return result.scalars().first()


async def list_users(
        db: AsyncSession,
        filter_: ListUserFilter
) -> list[User]:
    query = select(User).limit(filter_.per_page).offset((filter_.page - 1) * filter_.per_page)
    result = await db.execute(query)
    return list(result.scalars().all())
