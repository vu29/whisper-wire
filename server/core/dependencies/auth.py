from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException
from jose import jwt, JWTError

from server.core.config import settings
from server.core.dependencies.db import DBSessionDep
from server.core.security import oauth2_scheme
from server.users.models.user import User


async def get_current_user(db: DBSessionDep, token: str = Depends(oauth2_scheme)):
    from server.users.services.user_service import get_user_by_id  # Avoid circular import

    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])
        user_id: str = payload.get("sub")
        token_type: str = payload.get("type")
        if user_id is None or token_type != "access":
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await get_user_by_id(db, UUID(user_id))
    if user is None:
        raise credentials_exception
    return user


AuthRequiredDep = Annotated[User, Depends(get_current_user)]
