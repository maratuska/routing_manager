from typing import List

import sqlalchemy as sa
from sqlalchemy import desc
from sqlalchemy.engine import Row
from sqlmodel import select

from app.abc import AbstractService
from app.routes.models import RouteOwner, Route


__all__ = [
    'ReportsService',
]


class ReportsService(AbstractService):
    async def get_report_by_owners(self) -> List[Row]:
        raw_query = """
            SELECT 
                u.id,
                u.username,
                COUNT(*) as routes_count,
                SUM(r."length") as length_total
            FROM users u
            LEFT JOIN routes r ON r.owner_id = u.id
            GROUP BY u.id, u.username
            ORDER BY routes_count DESC
        """

        select_statement = select(
            RouteOwner.id,
            RouteOwner.username,
            sa.func.count(Route.id).label('routes_count'),
            sa.func.sum(Route.length).label('length_total'),
        ).join(
            target=Route,
            isouter=True,
        ).group_by(
            RouteOwner.id,
            RouteOwner.username,
        ).order_by(
            desc('routes_count'),
        )

        result = await self._session.execute(statement=select_statement)
        report_list = result.all()
        return report_list
