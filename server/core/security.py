from uuid import UUID

import pendulum
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext

from server.auth.exceptions import InvalidCredentialsException
from server.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(user_id: UUID) -> str:
    expire = pendulum.now("UTC") + pendulum.duration(minutes=settings.access_token_expire_minutes)
    to_encode = {
        "sub": str(user_id),
        "type": "access",
        "exp": expire
    }
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.jwt_algorithm)


def create_refresh_token(user_id: UUID) -> str:
    expire = pendulum.now("UTC") + pendulum.duration(days=settings.refresh_token_expire_days)
    to_encode = {
        "sub": str(user_id),
        "type": "refresh",
        "exp": expire
    }
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.jwt_algorithm)

def validate_refresh_token(token: str) -> UUID:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])
        user_id: str = payload.get("sub")
        token_type: str = payload.get("type")
        if user_id is None or token_type != "refresh":
            raise InvalidCredentialsException
        return UUID(user_id)
    except JWTError:
        raise InvalidCredentialsException
