from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Whisper Wire Server"
    db_url: str = "postgresql+asyncpg://root:@localhost/whisper-wire"
    echo_sql: bool = False
    access_token_expire_minutes: int = 5
    refresh_token_expire_days: int = 7
    secret_key: str = "insecure-secret"
    jwt_algorithm: str = "HS256"


    model_config = SettingsConfigDict(env_file=('.env',))


settings = Settings()  # type: ignore
