from pydantic import BaseModel


class RefreshRequestPayload(BaseModel):
    refresh_token: str