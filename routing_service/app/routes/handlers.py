from typing import List

from fastapi import APIRouter, Depends, Query, status, BackgroundTasks

from app.routes.models import RouteRead, RouteReadWithRelations, RouteOwnerReadWithRoutes, RouteCreate
from app.routes.service import RoutingService


__all__ = [
    'router',
]


router = APIRouter(prefix='/routes')


@router.get('/', response_model=List[RouteRead])
async def get_routes(
        offset: int = Query(default=0, ge=0),
        limit: int = Query(default=10, ge=0, le=100),
        service: RoutingService = Depends(),
):
    routes_list = await service.get_routes_list(offset=offset, limit=limit)
    return routes_list


@router.get('/{route_id}', response_model=RouteReadWithRelations)
async def get_route(
        route_id: int,
        service: RoutingService = Depends(),
):
    route = await service.get_route_by_id(route_id=route_id)
    return route


@router.post('/', response_model=RouteRead, status_code=status.HTTP_201_CREATED)
async def create_route(
        route_create: RouteCreate,
        background_tasks: BackgroundTasks,
        service: RoutingService = Depends(),
):
    new_route = await service.create_route(route_create=route_create)
    background_tasks.add_task(
        service.calculate_optimal_route,
        route_id=new_route.id,
        departure_point_id=new_route.departure_point_id,
        arrival_point_id=new_route.arrival_point_id,
    )
    return new_route


@router.get('/owner/{owner_id}', response_model=RouteOwnerReadWithRoutes)
async def get_owner(
        owner_id: int,
        service: RoutingService = Depends(),
):
    owner = await service.get_routes_owner(owner_id=owner_id)
    return owner






