from faker import Faker
from passlib.hash import bcrypt
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession, AsyncConnection, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import exists

from app.auth.models import User
from app.settings import conf


__all__ = [
    'get_session',
    'init_db_and_tables',
]


engine = create_async_engine(
    conf.db_settings.postgres_dsn,
    echo=True,
    future=True,
)

async_session_factory = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncSession:
    async with async_session_factory() as session:
        yield session


async def init_db_and_tables():
    async with engine.begin() as connection:
        connection: AsyncConnection
        await connection.run_sync(SQLModel.metadata.create_all)

    await create_testable_users()


async def create_testable_users():
    fake = Faker()

    users = [
        User(
            username=fake.user_name(),
            password_hash=bcrypt.hash(fake.password()),
        )
        for _ in range(4)
    ]

    sys_user = User(
        username='sys',
        password_hash=bcrypt.hash('123'),
    )
    users.append(sys_user)

    async with async_session_factory() as session:
        session: AsyncSession

        result = await session.execute(exists(User).select())
        is_users_exists = result.scalar()
        if is_users_exists:
            return

        session.add_all(users)
        await session.commit()
