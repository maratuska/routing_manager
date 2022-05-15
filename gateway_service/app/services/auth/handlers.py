from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.services.auth.client import UsersServiceClient
from app.services.auth.dependencies import get_users_service_client, get_current_user
from app.services.auth.models import Token, UserCreate, UserRead


router = APIRouter(prefix='/auth')


@router.post(
    '/sign-up',
    response_model=Token,
    status_code=status.HTTP_201_CREATED,
)
async def sign_up(
    user_data: UserCreate,
    users_service_cli: UsersServiceClient = Depends(get_users_service_client),
):
    return await users_service_cli.sing_up(username=user_data.username, password=user_data.password)


@router.post(
    '/sign-in',
    response_model=Token,
)
async def sign_in(
    auth_data: OAuth2PasswordRequestForm = Depends(),
    users_service_cli: UsersServiceClient = Depends(get_users_service_client),
):
    return await users_service_cli.sing_in(username=auth_data.username, password=auth_data.password)


@router.get(
    '/user',
    response_model=UserRead,
)
async def get_current_user(
    user: UserRead = Depends(get_current_user),
):
    return user
