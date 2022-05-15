from datetime import (
    datetime,
    timedelta,
)
from fastapi import (
    HTTPException,
    status, Depends,
)
from jose import (
    JWTError,
    jwt,
)
from passlib.hash import bcrypt
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.auth.models import UserCreate, User, Token
from app.connections.db import get_session
from app.settings import AuthSettings, conf


class AuthService:
    _settings: AuthSettings = conf.auth_settings

    def __init__(self, session: AsyncSession):
        self._session = session

    async def register_new_user(
        self,
        user_data: UserCreate,
    ) -> Token:
        user = User(
            username=user_data.username,
            password_hash=self.hash_password(user_data.password),
        )
        try:
            self._session.add(user)
            await self._session.commit()
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='User already exists')

        return self._create_token(user)

    async def authenticate_user(
        self,
        username: str,
        password: str,
    ) -> Token:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )

        result = await self._session.execute(select(User).where(User.username == username))
        user = result.scalar()

        if not user:
            raise exception

        if not self.verify_password(password, user.password_hash):
            raise exception

        return self._create_token(user)

    @classmethod
    def verify_token(cls, token: str) -> User:
        auth_error_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
        )

        try:
            payload = jwt.decode(
                token=token,
                key=cls._settings.jwt_secret,
                algorithms=[cls._settings.jwt_algorithm],
            )
        except JWTError:
            raise auth_error_exception

        try:
            user_data = payload.get('user')
            user = User.parse_obj(user_data)
        except ValidationError:
            raise auth_error_exception

        return user

    @classmethod
    def _create_token(cls, user: User) -> Token:
        utc_now = datetime.utcnow()
        payload = {
            'iat': utc_now,
            'nbf': utc_now,
            'exp': utc_now + timedelta(seconds=cls._settings.jwt_expires_s),
            'sub': str(user.id),
            'user': user.dict(),
        }
        token = jwt.encode(
            claims=payload,
            key=cls._settings.jwt_secret,
            algorithm=cls._settings.jwt_algorithm,
        )
        return Token(access_token=token)

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.verify(plain_password, hashed_password)

    @classmethod
    def hash_password(cls, password: str) -> str:
        return bcrypt.hash(password)


async def get_auth_service(session: AsyncSession = Depends(get_session)) -> AuthService:
    return AuthService(session=session)
