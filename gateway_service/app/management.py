from fastapi import FastAPI, APIRouter

from app.services.auth.handlers import router as auth_service_router
from app.services.routing.handlers import router as routing_service_router
from app.settings import AppConfig


__all__ = [
    'ApiManager',
]


class ApiManager:
    _routing_prefix = '/api'

    def __init__(self, config: AppConfig) -> None:
        self._config = config
        self._app = self._create_app()
        self._configure_routing()

    def _create_app(self) -> FastAPI:
        return FastAPI(
            title=self._config.api_settings.title,
            description=self._config.api_settings.description,
            debug=self._config.api_settings.debug,
            on_startup=[self._on_startup],
            on_shutdown=[self._on_shutdown],
        )

    def _configure_routing(self):
        self._router = APIRouter(prefix=self._routing_prefix)
        self._router.include_router(router=auth_service_router)
        self._router.include_router(router=routing_service_router)
        self._app.include_router(router=self._router)

    async def _on_startup(self):
        pass

    async def _on_shutdown(self):
        pass

    @property
    def app_instance(self) -> FastAPI:
        return self._app
