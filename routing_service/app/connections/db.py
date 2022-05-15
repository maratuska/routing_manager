from random import randint, random

from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncConnection
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text as sa_text, exists

from app.points.models import Point
from app.settings import conf
from app.routes.models import (
    Route,
    RoutePoint,
)


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

    await _create_points()
    await _create_routes()


async def _create_points():
    create_points_query = """
        INSERT INTO points (name, latitude, longitude)
        SELECT md5(random()::text), random() * 1000, random() * 1000
        FROM generate_series(0, 1000000)
    """

    async with engine.begin() as connection:
        connection: AsyncConnection

        result = await connection.execute(exists(Point).select())
        is_points_exists = result.scalar()
        if is_points_exists:
            return

        await connection.execute(statement=sa_text(create_points_query))


async def _create_routes():
    routes = [
        Route(
            departure_point_id=randint(1, 499_999),
            arrival_point_id=randint(500_000, 1_000_000),
            route_number=randint(100, 1000),
            length=random() * 1000,
            owner_id=randint(1, 5),
        )
        for _ in range(1, 3)
    ]

    route_points = []
    intermediate_points_count_iter = iter((2, 100))
    for route_id, route in enumerate(routes, start=1):
        for point_seq_num in range(next(intermediate_points_count_iter)):
            intermediate_point_id = randint(1, 1_000_000)
            route_points.append(RoutePoint(
                route_id=route_id,
                point_id=intermediate_point_id,
                seq_num=point_seq_num,
            ))

    async with async_session_factory() as session:
        session: AsyncSession

        result = await session.execute(exists(Route).select())
        is_routes_exists = result.scalar()
        if is_routes_exists:
            return

        session.add_all(routes)
        session.add_all(route_points)
        await session.commit()
