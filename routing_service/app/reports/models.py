from typing import Optional

from app.routes.models import RouteOwnerRead


__all__ = [
    'ReportByRouteOwner',
]


class ReportByRouteOwner(RouteOwnerRead):
    routes_count: int
    length_total: Optional[float]
