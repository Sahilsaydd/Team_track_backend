# app/modules/notifications/services/notification_service.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from fastapi import HTTPException

from app.modules.notification.model.notification import Notification


# =====================================================
# CREATE NOTIFICATION
# =====================================================

async def create_notification_service(
    db: AsyncSession,
    user_id: int,
    title: str,
    message: str,
    notification_type: str
):

    notification = Notification(

        user_id=user_id,

        title=title,

        message=message,

        notification_type=notification_type
    )

    db.add(notification)

    await db.commit()

    await db.refresh(notification)

    return notification


# =====================================================
# GET USER NOTIFICATIONS
# =====================================================

async def get_notifications_service(
    db: AsyncSession,
    current_user
):

    result = await db.execute(
        select(Notification).where(
            Notification.user_id == current_user.id
        ).order_by(
            Notification.created_at.desc()
        )
    )

    notifications = result.scalars().all()

    return notifications


# =====================================================
# MARK NOTIFICATION AS READ
# =====================================================

async def mark_notification_read_service(
    db: AsyncSession,
    notification_id: int,
    current_user
):

    result = await db.execute(
        select(Notification).where(
            Notification.id == notification_id,
            Notification.user_id == current_user.id
        )
    )

    notification = result.scalar_one_or_none()

    if not notification:
        raise HTTPException(
            status_code=404,
            detail="Notification not found"
        )

    notification.is_read = True

    await db.commit()

    await db.refresh(notification)

    return notification


# =====================================================
# GET UNREAD NOTIFICATION COUNT
# =====================================================

async def unread_notification_count_service(
    db: AsyncSession,
    current_user
):

    result = await db.execute(
        select(Notification).where(
            Notification.user_id == current_user.id,
            Notification.is_read == False
        )
    )

    notifications = result.scalars().all()

    return {
        "unread_count": len(notifications)
    }