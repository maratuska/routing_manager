from fastapi import APIRouter, status, Depends

from app.auth.service import get_auth_service, AuthService
from app.auth.models import Token, UserCreate, User, UserAuth

router = APIRouter()


@router.post(
    '/sign-up',
    response_model=Token,
    status_code=status.HTTP_201_CREATED,
)
async def sign_up(
    user_create: UserCreate,
    auth_service: AuthService = Depends(get_auth_service),
):
    return await auth_service.register_new_user(user_data=user_create)


@router.post(
    '/sign-in',
    response_model=Token,
)
async def sign_in(
    user_auth: UserAuth,
    auth_service: AuthService = Depends(get_auth_service),
):
    return await auth_service.authenticate_user(
        username=user_auth.username,
        password=user_auth.password,
    )


@router.get(
    '/user',
    response_model=User,
)
async def get_user(
    token: str,
    auth_service: AuthService = Depends(get_auth_service),
):
    return auth_service.verify_token(token=token)
