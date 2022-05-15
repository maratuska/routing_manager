from typing import Dict, Any

from app.connections.abc import AbstractServiceClient


class UsersServiceClient(AbstractServiceClient):
    class Endpoint:
        sing_up = 'sign-up'
        sing_in = 'sign-in'
        user = 'user'

    async def sing_up(self, username: str, password: str) -> Dict[str, Any]:
        return await self._http_client.post(
            endpoint_url=f'{self._service_url}{self.Endpoint.sing_up}',
            json_data={'username': username, 'password': password},
        )

    async def sing_in(self, username: str, password: str) -> Dict[str, Any]:
        return await self._http_client.post(
            endpoint_url=f'{self._service_url}{self.Endpoint.sing_in}',
            json_data={'username': username, 'password': password},
        )

    async def get_user_by_token(self, token: str) -> Dict[str, Any]:
        return await self._http_client.get(
            endpoint_url=f'{self._service_url}{self.Endpoint.user}',
            query_params={'token': token},
        )
