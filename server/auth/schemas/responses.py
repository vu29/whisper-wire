from pydantic import BaseModel


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str

class RefreshResponse(BaseModel):
    access_token: str