from pydantic import BaseSettings as PydanticBaseSettings, BaseModel, Field


__all__ = [
    'conf',
    'AppConfig',
]


class BaseSettings(PydanticBaseSettings):
    class Config:
        env_file = './.env'
        env_file_encoding = 'utf-8'


class ApiSettings(BaseSettings):
    title = Field(default='Gateway service', env='api_title')
    description = Field(default='', env='api_description')
    debug = Field(default=False, env='debug_mode')


class ServicesConnectionSettings(BaseSettings):
    routing_service_url: str = Field(..., env='routing_service_url')
    users_service_url: str = Field(..., env='users_service_url')


class AppConfig(BaseModel):
    api_settings: ApiSettings = ApiSettings()
    services_connection_settings: ServicesConnectionSettings = ServicesConnectionSettings()

    class Config:
        allow_mutation = False


conf = AppConfig()
