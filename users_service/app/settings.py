from pydantic import BaseSettings as PydanticBaseSettings, BaseModel, Field, PostgresDsn


__all__ = [
    'conf',
    'AppConfig',
    'AuthSettings',
]


class BaseSettings(PydanticBaseSettings):
    class Config:
        env_file = './.env'
        env_file_encoding = 'utf-8'


class ApiSettings(BaseSettings):
    title = Field(default='Users service', env='api_title')
    debug = Field(default=False, env='debug_mode')


class AuthSettings(BaseSettings):
    jwt_secret: str = Field(..., env='jwt_secret')
    jwt_algorithm: str = Field(default='HS256', env='jwt_algorithm')
    jwt_expires_s: int = Field(default=3600, env='jwt_expires_s')


class DatabaseSettings(BaseSettings):
    postgres_dsn: PostgresDsn = Field(..., env='postgres_url')


class AppConfig(BaseModel):
    api_settings: ApiSettings = ApiSettings()
    db_settings: DatabaseSettings = DatabaseSettings()
    auth_settings: AuthSettings = AuthSettings()

    class Config:
        allow_mutation = False


conf = AppConfig()
