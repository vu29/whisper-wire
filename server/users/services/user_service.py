from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from server.core.security import hash_password
from server.users.exceptions import UserExistsException, UserNotFoundException
from server.users.models.user import User
from server.users.schemas.filter import ListUserFilter

__all__ = [
    "create_user",
    "get_user_by_id",
    "list_users",
    "get_user_by_username",
    "user_exists",
    "delete_user"
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


async def user_exists(
        db: AsyncSession,
        *,
        id: UUID | None = None,
        username: str | None = None
) -> bool:
    if not id and not username:
        raise ValueError("user_id or user_name must be provided")
    query = select(User.is_deleted)
    if id:
        query = query.where(User.id == id)
    if username:
        query = query.where(User.username == username)

    result = await db.execute(query)
    return result.scalars().first() is False


async def get_user_by_id(
        db: AsyncSession,
        user_id: UUID
) -> User | None:
    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    return result.scalars().first()


async def get_user_by_username(
        db: AsyncSession,
        username: str
) -> User | None:
    query = select(User).where(User.username == username)
    result = await db.execute(query)
    return result.scalars().first()


async def delete_user(
        db: AsyncSession,
        user_id: UUID
) -> None:
    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    user = result.scalars().first()
    if not user:
        raise UserNotFoundException
    user.is_deleted = True
    await db.commit()


async def list_users(
        db: AsyncSession,
        filter_: ListUserFilter
) -> list[User]:
    query = select(User).limit(filter_.per_page).offset((filter_.page - 1) * filter_.per_page)
    result = await db.execute(query)
    return list(result.scalars().all())
