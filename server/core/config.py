from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Whisper Wire Server"
    db_url: str = "postgresql+asyncpg://root:@localhost/whisper-wire"
    echo_sql: bool = False

    model_config = SettingsConfigDict(env_file=('.env',))


settings = Settings()  # type: ignore
