from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.services.auth.client import UsersServiceClient
from app.services.auth.models import UserRead
from app.connections.http import HttpxClient
from app.connections.abc import AbstractHttpClient, AbstractServiceClient
from app.settings import conf


oauth2_header = OAuth2PasswordBearer(tokenUrl='/api/auth/sign-in')


async def get_users_service_client(http_client: AbstractHttpClient = Depends(HttpxClient)) -> AbstractServiceClient:
    return UsersServiceClient(
        service_url=conf.services_connection_settings.users_service_url,
        http_client=http_client,
    )


async def get_current_user(
        token: str = Depends(oauth2_header),
        users_service_cli: UsersServiceClient = Depends(get_users_service_client),
) -> UserRead:
    user_data = await users_service_cli.get_user_by_token(token=token)
    return UserRead.parse_obj(user_data)

