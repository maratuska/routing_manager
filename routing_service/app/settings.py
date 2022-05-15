from pydantic import BaseSettings as PydanticBaseSettings, BaseModel, Field, PostgresDsn


__all__ = [
    'conf',
    'AppConfig',
]


class BaseSettings(PydanticBaseSettings):
    class Config:
        env_file = './.env'
        env_file_encoding = 'utf-8'


class ApiSettings(BaseSettings):
    title = Field(default='Routing service', env='api_title')
    debug = Field(default=False, env='debug_mode')


class DatabaseSettings(BaseSettings):
    postgres_dsn: PostgresDsn = Field(..., env='postgres_url')


class AppConfig(BaseModel):
    api_settings: ApiSettings = ApiSettings()
    db_settings: DatabaseSettings = DatabaseSettings()

    class Config:
        allow_mutation = False


conf = AppConfig()
