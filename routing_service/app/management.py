from fastapi import FastAPI, APIRouter

from app.connections.db import init_db_and_tables
from app.settings import AppConfig
from app.points.handlers import router as points_router
from app.routes.handlers import router as routes_router
from app.reports.handlers import router as reports_router


__all__ = [
    'ApiManager',
]


class ApiManager:
    def __init__(self, config: AppConfig) -> None:
        self._config = config
        self._app = self._create_app()
        self._configure_routing()

    def _create_app(self) -> FastAPI:
        return FastAPI(
            title=self._config.api_settings.title,
            debug=self._config.api_settings.debug,
            on_startup=[self._on_startup],
            on_shutdown=[self._on_shutdown],
        )

    def _configure_routing(self):
        self._router = APIRouter()
        self._router.include_router(router=points_router)
        self._router.include_router(router=routes_router)
        self._router.include_router(router=reports_router)
        self._app.include_router(router=self._router)

    async def _on_startup(self):
        await init_db_and_tables()

    async def _on_shutdown(self):
        pass

    @property
    def app_instance(self) -> FastAPI:
        return self._app
