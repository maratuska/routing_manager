from typing import Any

import httpx
from fastapi import HTTPException, status
from httpx import ReadTimeout, ConnectError

from app.connections.abc import AbstractHttpClient


class HttpxClient(AbstractHttpClient):
    async def get(self, endpoint_url: str, query_params: Any = None) -> Any:
        async with self.async_client as client:
            try:
                response = await client.get(url=endpoint_url, params=query_params)
            except ReadTimeout:
                raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT)
            except ConnectError:
                raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
            except Exception as exc:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))

            if response.is_error:
                error_detail = f'GET {endpoint_url} with query {query_params}: {response.text}'
                raise HTTPException(status_code=response.status_code, detail=error_detail)

        response_json = response.json()
        return response_json

    async def post(self, endpoint_url: str, data: Any = None, json_data: Any = None) -> Any:
        async with self.async_client as client:
            try:
                response = await client.post(url=endpoint_url, data=data, json=json_data)
            except ReadTimeout:
                raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT)
            except ConnectError:
                raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
            except Exception as exc:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))

            if response.is_error:
                error_detail = f'POST {endpoint_url}: {response.text}'
                raise HTTPException(status_code=response.status_code, detail=error_detail)

        response_json = response.json()
        return response_json

    @property
    def async_client(self) -> httpx.AsyncClient:
        return httpx.AsyncClient(timeout=self._request_timeout)
