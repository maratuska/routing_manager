from abc import ABC, abstractmethod
from typing import Any


class AbstractHttpClient(ABC):
    _request_timeout: float = 10.

    @abstractmethod
    async def get(self, endpoint_url: str, query_params: Any = None) -> Any:
        pass

    @abstractmethod
    async def post(self, endpoint_url: str, data: Any = None, json_data: Any = None) -> Any:
        pass


class AbstractServiceClient(ABC):
    def __init__(
            self,
            service_url: str,
            http_client: AbstractHttpClient,
    ):
        self._service_url = service_url
        self._http_client = http_client
