from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from server.auth.exceptions import InvalidCredentialsException
from server.core.security import verify_password, create_access_token, create_refresh_token, validate_refresh_token
from server.users.models.user import User
from server.users.services.user_service import get_user_by_username, user_exists


async def login_user(
        db: AsyncSession,
        username: str,
        password: str,
) -> tuple[str, str]:
    user: User | None = await get_user_by_username(db, username)
    if not user or user.is_deleted or not verify_password(password, user.password_hash):
        raise InvalidCredentialsException
    return create_access_token(user.id), create_refresh_token(user.id)


async def get_new_access_token(
        db: AsyncSession,
        refresh_token: str,
) -> str:
    user_id: UUID = validate_refresh_token(refresh_token)
    if not user_exists(db, id=user_id):
        raise InvalidCredentialsException
    return create_access_token(user_id)
