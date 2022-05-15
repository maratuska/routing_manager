from typing import List

from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.connections.db import get_session
from app.points.models import Point, PointRead


__all__ = [
    'router',
]


router = APIRouter(prefix='/points')


@router.get('/{point_id}', response_model=PointRead)
async def get_point(
    point_id: int,
    session: AsyncSession = Depends(get_session),
):
    point = await session.get(entity=Point, ident=point_id)
    if not point:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return point


@router.get('/', response_model=List[PointRead])
async def get_points(
    session: AsyncSession = Depends(get_session),
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=0, le=100),
):
    select_statement = select(Point).offset(offset).limit(limit)
    result = await session.execute(statement=select_statement)
    points_list = result.scalars().all()
    return points_list
