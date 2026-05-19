

from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.deps.db import get_db

from app.deps.auth_deps import get_current_user

from app.modules.notification.services.notification_service import (

    get_notifications_service,

    mark_notification_read_service,

    unread_notification_count_service
)

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)


# =====================================================
# GET MY NOTIFICATIONS
# =====================================================

@router.get("/")
async def get_notifications_api(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return await get_notifications_service(
        db,
        current_user
    )


# =====================================================
# MARK NOTIFICATION AS READ
# =====================================================

@router.patch("/{notification_id}/read")
async def mark_notification_read_api(
    notification_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return await mark_notification_read_service(
        db,
        notification_id,
        current_user
    )


# =====================================================
# GET UNREAD COUNT
# =====================================================

@router.get("/unread/count")
async def unread_notification_count_api(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return await unread_notification_count_service(
        db,
        current_user
    )