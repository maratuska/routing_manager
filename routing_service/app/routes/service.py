import asyncio
from random import randint, random
from typing import List

from fastapi import HTTPException, status
from sqlmodel import select

from app.abc import AbstractService
from app.points.models import Point
from app.routes.models import RouteReadWithRelations, Route, RouteOwner, RoutePoint, RouteOwnerReadWithRoutes, \
    RouteCreate


__all__ = [
    'RoutingService',
]


class RoutingService(AbstractService):
    async def get_routes_list(self, offset: int, limit: int) -> List[Route]:
        select_statement = select(Route).offset(offset).limit(limit)
        result = await self._session.execute(statement=select_statement)
        routes_list = result.scalars().all()
        return routes_list

    async def get_routes_owner(self, owner_id: int) -> RouteOwnerReadWithRoutes:
        owner = await self._session.get(entity=RouteOwner, ident=owner_id)
        if not owner:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        routes = await self._session.execute(select(Route).where(Route.owner_id == owner_id))

        result_model = RouteOwnerReadWithRoutes(
            **owner.dict(),
            routes=routes.scalars().all(),
        )
        return result_model

    async def get_route_by_id(self, route_id: int) -> RouteReadWithRelations:
        route = await self._session.get(entity=Route, ident=route_id)
        if not route:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Route not found')

        required_point_fields = (
            RoutePoint.point_id,
            RoutePoint.seq_num,
            Point.name,
            Point.latitude,
            Point.longitude,
        )
        points = await self._session.execute(
            select(*required_point_fields).join(Point).where(RoutePoint.route_id == route.id),
        )
        route_owner = await self._session.get(entity=RouteOwner, ident=route.owner_id)
        if not route_owner:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Route owner not found')

        result_model = RouteReadWithRelations(
            **route.dict(),
            owner=route_owner,
            points=points.all(),
        )
        return result_model

    async def create_route(
            self,
            route_create: RouteCreate,
    ) -> Route:
        new_route = Route.from_orm(route_create)
        self._session.add(new_route)
        await self._session.commit()

        return new_route

    async def calculate_optimal_route(
            self,
            route_id: int,
            departure_point_id: int,
            arrival_point_id: int,
    ) -> None:
        await asyncio.sleep(randint(5, 10))

        intermediate_point = [
            RoutePoint(
                route_id=route_id,
                point_id=randint(1, 1_000_000),
                seq_num=point_seq_num,
            )
            for point_seq_num in range(randint(2, 100))
        ]
        route_length = random() * 10_000

        statement = select(Route).where(Route.id == route_id)
        result = await self._session.execute(statement)
        route = result.scalar()
        route.length = route_length

        self._session.add_all(intermediate_point)
        self._session.add(route)
        await self._session.commit()
