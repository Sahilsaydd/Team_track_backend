from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps.db import get_db
from app.deps.auth_deps import get_current_user

from app.modules.dashboard.services.dashboard_services import (
    superadmin_dashboard_service
)

from app.modules.dashboard.schemas.dashboard_schemas import (
    DashboardResponseSchema
)

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get(
    "/superadmin",
    response_model=DashboardResponseSchema
)
async def get_superadmin_dashboard(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return await superadmin_dashboard_service(
        db,
        current_user
    )