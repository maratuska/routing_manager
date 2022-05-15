from typing import Optional

from sqlmodel import SQLModel, Field


__all__ = [
    'PointBase',
    'Point',
    'PointRead',
]


class PointBase(SQLModel):
    name: str
    latitude: float
    longitude: float


class Point(PointBase, table=True):
    __tablename__ = 'points'

    id: Optional[int] = Field(default=None, primary_key=True)


class PointRead(PointBase):
    id: int
