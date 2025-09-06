from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Header
from fastapi.security import OAuth2PasswordRequestForm

from server.auth.exceptions import InvalidCredentialsException
from server.auth.schemas.requests import RefreshRequestPayload
from server.auth.schemas.responses import LoginResponse, RefreshResponse
from server.auth.services.auth_service import login_user, get_new_access_token
from server.core.dependencies import DBSessionDep

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: DBSessionDep
) -> LoginResponse:
    try:
        access_token, refresh_token = await login_user(db, form_data.username, form_data.password)
    except InvalidCredentialsException:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return LoginResponse(access_token=access_token, refresh_token=refresh_token)

@router.post("/refresh")
async def refresh_token(
        db: DBSessionDep,
        payload: RefreshRequestPayload
) -> RefreshResponse:
    try:
        access_token = await get_new_access_token(db, payload.refresh_token)
    except InvalidCredentialsException:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    return RefreshResponse(access_token=access_token)

