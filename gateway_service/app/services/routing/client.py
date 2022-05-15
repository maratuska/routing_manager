from typing import List, Dict, Any

from fastapi import Depends

from app.connections.http import HttpxClient
from app.connections.abc import AbstractHttpClient, AbstractServiceClient
from app.services.auth.dependencies import get_current_user
from app.services.auth.models import UserRead
from app.services.routing.models import RouteCreate
from app.settings import conf


class RoutingServiceClient(AbstractServiceClient):
    class Endpoint:
        points = 'points'
        routes = 'routes'
        report_by_owners = 'reports/owners'

    def __init__(
            self,
            service_url: str,
            http_client: AbstractHttpClient,
            user: UserRead,
    ):
        super().__init__(service_url=service_url, http_client=http_client)
        self._user = user

    async def read_points(self, offset: int, limit: int) -> List[Dict[str, Any]]:
        return await self._http_client.get(
            endpoint_url=f'{self._service_url}{self.Endpoint.points}/',
            query_params={'offset': offset, 'limit': limit},
        )

    async def read_routes(self, offset: int, limit: int) -> List[Dict[str, Any]]:
        return await self._http_client.get(
            endpoint_url=f'{self._service_url}{self.Endpoint.routes}/',
            query_params={'offset': offset, 'limit': limit},
        )

    async def read_route(self, route_id: int) -> Dict[str, Any]:
        return await self._http_client.get(endpoint_url=f'{self._service_url}{self.Endpoint.routes}/{route_id}')

    async def create_route(self, route_params: RouteCreate) -> Dict[str, Any]:
        return await self._http_client.post(
            endpoint_url=f'{self._service_url}{self.Endpoint.routes}/',
            json_data={
                'owner_id': self._user.id,
                **route_params.dict()
            },
        )

    async def generate_report_by_owners(self) -> List[Dict[str, Any]]:
        return await self._http_client.get(endpoint_url=f'{self._service_url}{self.Endpoint.report_by_owners}/')


async def get_routing_service_client(
        http_client: AbstractHttpClient = Depends(HttpxClient),
        user: UserRead = Depends(get_current_user),
) -> AbstractServiceClient:
    return RoutingServiceClient(
        service_url=conf.services_connection_settings.routing_service_url,
        http_client=http_client,
        user=user,
    )
