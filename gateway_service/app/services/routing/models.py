from typing import Optional, List

from pydantic import BaseModel


class PointBase(BaseModel):
    name: str
    latitude: float
    longitude: float


class PointRead(PointBase):
    id: int


class BaseRoute(BaseModel):
    route_number: int
    departure_point_id: int
    arrival_point_id: int


class RouteCreate(BaseRoute):
    pass


class RouteRead(BaseRoute):
    id: int
    length: Optional[float]
    owner_id: int


class RouteOwnerRead(BaseModel):
    id: int
    username: str


class RoutePointRead(PointBase):
    point_id: int
    seq_num: int


class RouteReadExtended(RouteRead):
    owner: RouteOwnerRead
    points: List[RoutePointRead]

