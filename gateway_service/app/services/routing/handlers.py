from typing import List

from fastapi import APIRouter, Depends, status, Query

from app.services.routing.client import RoutingServiceClient, get_routing_service_client
from app.services.routing.models import RouteCreate, RouteRead, PointRead, RouteReadExtended


router = APIRouter()


@router.get('/points', response_model=List[PointRead])
async def read_points(
        offset: int = Query(default=0, ge=0),
        limit: int = Query(..., ge=0),
        routing_service_cli: RoutingServiceClient = Depends(get_routing_service_client),
):
    return await routing_service_cli.read_points(offset=offset, limit=limit)


@router.get('/routes', response_model=List[RouteRead])
async def read_routes(
        offset: int = Query(default=0, ge=0),
        limit: int = Query(..., ge=0),
        routing_service_cli: RoutingServiceClient = Depends(get_routing_service_client)
):
    return await routing_service_cli.read_routes(offset=offset, limit=limit)


@router.get('/routes/{route_id}', response_model=RouteReadExtended)
async def read_route(
        route_id: int,
        routing_service_cli: RoutingServiceClient = Depends(get_routing_service_client)
):
    return await routing_service_cli.read_route(route_id=route_id)


@router.post('/routes', response_model=RouteRead, status_code=status.HTTP_201_CREATED)
async def create_route(
        create_params: RouteCreate,
        routing_service_cli: RoutingServiceClient = Depends(get_routing_service_client),
):
    return await routing_service_cli.create_route(route_params=create_params)


@router.get('/report')
async def read_report(
        routing_service_cli: RoutingServiceClient = Depends(get_routing_service_client),
):
    return await routing_service_cli.generate_report_by_owners()
