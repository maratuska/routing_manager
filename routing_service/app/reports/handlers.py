from typing import List

from fastapi import APIRouter, Depends

from app.reports.models import ReportByRouteOwner
from app.reports.service import ReportsService


__all__ = [
    'router',
]


router = APIRouter(prefix='/reports')


@router.get('/owners/', response_model=List[ReportByRouteOwner])
async def get_report_by_owners(
        service: ReportsService = Depends(),
):
    report = await service.get_report_by_owners()
    return report
