
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from app.modules.groups.models.group_member import GroupMember
from app.modules.tasks.models.task import Task
from app.modules.tasks.models.task_review import TaskReview
from app.modules.tasks.models.task_log import TaskLog

from app.modules.notification.model.notification import (
    Notification
)

from app.modules.users.models.user import User

from app.modules.tasks.enums import (
    ApprovalStatus,
    TaskStatus
)



async def create_task_service(db: AsyncSession,data,current_user):

    # CHECK CURRENT USER IS GROUP LEAD

    leader_result = await db.execute(
        select(GroupMember).where(
            GroupMember.group_id == data.group_id,
            GroupMember.user_id == current_user.id,
            GroupMember.role_in_group == "Lead",
            GroupMember.is_active == True
        )
    )

    leader = leader_result.scalar_one_or_none()

    if not leader:

        raise HTTPException(
            status_code=403,
            detail="Only group leader can assign tasks"
        )

    # CHECK ASSIGNED USER BELONGS TO GROUP

    member_result = await db.execute(
        select(GroupMember).where(
            GroupMember.group_id == data.group_id,
            GroupMember.user_id == data.assigned_to,
            GroupMember.is_active == True
        )
    )

    member = member_result.scalar_one_or_none()

    if not member:

        raise HTTPException(
            status_code=404,
            detail="Assigned user is not member of this group"
        )

    # PREVENT LEAD TO LEAD ASSIGNMENT

    if member.role_in_group == "Lead":

        raise HTTPException(
            status_code=400,
            detail="Cannot assign task to another lead"
        )

    # CREATE TASK

    task = Task(

        title=data.title,

        description=data.description,

        priority=data.priority,

        deadline=data.deadline,

        group_id=data.group_id,

        created_by=current_user.id,

        assigned_by=current_user.id,

        assigned_to=data.assigned_to,

        submitted_to=current_user.id,

        is_self_task=False
    )

    db.add(task)

    # CREATE NOTIFICATION

    notification = Notification(

        user_id=data.assigned_to,

        title="New Task Assigned",

        message=f"You received task '{task.title}'",

        notification_type="task_assigned"
    )

    db.add(notification)

    await db.commit()

    await db.refresh(task)

    return task

async def create_self_task_service(
    db: AsyncSession,
    data,
    current_user
):

    task = Task(

        title=data.title,

        description=data.description,

        priority=data.priority,

        created_by=current_user.id,

        assigned_by=current_user.id,

        assigned_to=current_user.id,

        submitted_to=current_user.id,

        is_self_task=True
    )

    db.add(task)

    await db.commit()

    await db.refresh(task)

    return task



async def update_task_status_service(
    db: AsyncSession,
    task_id: int,
    data,
    current_user
):

    result = await db.execute(
        select(Task).where(
            Task.id == task_id
        )
    )

    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    if task.assigned_to != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not allowed"
        )

    task.status = data.status

    notification = Notification(

        user_id=task.submitted_to,

        title="Task Status Updated",

        message=f"Task '{task.title}' moved to {data.status}",

        notification_type="status_changed"
    )

    db.add(notification)

    await db.commit()

    await db.refresh(task)

    return task



async def add_task_log_service(
    db: AsyncSession,
    data,
    current_user
):

    result = await db.execute(
        select(Task).where(
            Task.id == data.task_id
        )
    )

    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    log = TaskLog(

        task_id=data.task_id,

        user_id=current_user.id,

        work_note=data.work_note,

        hours_spent=data.hours_spent
    )

    db.add(log)

    await db.commit()

    await db.refresh(log)

    return log



async def submit_task_service(
    db: AsyncSession,
    task_id: int,
    current_user
):

    result = await db.execute(
        select(Task).where(
            Task.id == task_id
        )
    )

    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    task.approval_status = ApprovalStatus.SUBMITTED

    notification = Notification(

        user_id=task.submitted_to,

        title="Task Submitted",

        message=f"Task '{task.title}' submitted for review",

        notification_type="task_submitted"
    )

    db.add(notification)

    await db.commit()

    await db.refresh(task)

    return task



async def review_task_service(
    db: AsyncSession,
    task_id: int,
    data,
    current_user
):

    result = await db.execute(
        select(Task).where(
            Task.id == task_id
        )
    )

    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    task.approval_status = data.review_status

    review = TaskReview(

        task_id=task.id,

        reviewed_by=current_user.id,

        reviewed_status=data.review_status,

        comment=data.comment
    )

    db.add(review)

    notification = Notification(

        user_id=task.assigned_to,

        title="Task Review Update",

        message=data.comment,

        notification_type=data.review_status
    )

    db.add(notification)

    await db.commit()

    return {
        "message": "Task reviewed successfully"
    }



async def get_my_tasks_service(
    db: AsyncSession,
    current_user
):

    result = await db.execute(
        select(Task).where(
            Task.assigned_to == current_user.id
        )
    )

    return result.scalars().all()



async def get_group_tasks_service(
    db: AsyncSession,
    current_user
):

    result = await db.execute(
        select(Task).where(
            Task.submitted_to == current_user.id
        )
    )

    return result.scalars().all()



async def get_all_tasks_service(
    db: AsyncSession
):

    result = await db.execute(
        select(Task)
    )

    return result.scalars().all() 
