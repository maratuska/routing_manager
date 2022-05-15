from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship

from app.points.models import PointBase


__all__ = [
    'Route',
    'RouteRead',
    'RouteReadWithRelations',
    'RouteCreate',

    'RouteOwner',
    'RouteOwnerRead',
    'RouteOwnerReadWithRoutes',

    'RoutePoint',
    'RoutePointRead',
]


# route
#
class RouteBase(SQLModel):
    route_number: int

    departure_point_id: int = Field(foreign_key='points.id')
    arrival_point_id: int = Field(foreign_key='points.id')
    owner_id: int = Field(foreign_key='users.id')


class Route(RouteBase, table=True):
    __tablename__ = 'routes'

    id: Optional[int] = Field(default=None, primary_key=True)
    length: Optional[float] = Field(default=None, nullable=True)
    owner: 'RouteOwner' = Relationship(back_populates='routes')
    points: List['RoutePoint'] = Relationship(back_populates='route')


class RouteRead(RouteBase):
    id: int
    length: Optional[float]


class RouteReadWithRelations(RouteRead):
    owner: 'RouteOwnerRead'
    points: List['RoutePointRead'] = Field(default_factory=list)


class RouteCreate(RouteBase):
    pass


# route owner
#
class RouteOwnerBase(SQLModel):
    username: str


class RouteOwner(RouteOwnerBase, table=True):
    __tablename__ = 'users'

    id: Optional[int] = Field(default=None, primary_key=True)
    routes: List[Route] = Relationship(back_populates='owner')


class RouteOwnerRead(RouteOwnerBase):
    id: int


class RouteOwnerReadWithRoutes(RouteOwnerRead):
    routes: List[RouteRead] = Field(default_factory=list)


# route points
#
class RoutePointBase(SQLModel):
    route_id: Optional[int] = Field(default=None, foreign_key='routes.id', primary_key=True)
    point_id: Optional[int] = Field(default=None, foreign_key='points.id', primary_key=True)
    seq_num: int = Field(ge=0)


class RoutePoint(RoutePointBase, table=True):
    __tablename__ = 'route_points'

    route: Route = Relationship(back_populates='points')


class RoutePointRead(PointBase):
    point_id: int
    seq_num: int


RouteReadWithRelations.update_forward_refs()
