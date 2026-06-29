from datetime import datetime

from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import (
    select,
    func,
    case
)
from sqlalchemy.orm import aliased
from app.modules.groups.models.group_member import GroupMember
from app.modules.groups.models.group import Group
from app.modules.users.models.user import User
from app.modules.roles.model.role import Role
from app.modules.groups.models.group_member import GroupMember

from app.modules.tasks.models.task import Task

from app.modules.tasks.enums import (
    TaskStatus,
    ApprovalStatus
)


async def superadmin_dashboard_service(
    db,
    current_user
):

    if current_user.role.name != "SuperAdmin":

        raise HTTPException(
            status_code=403,
            detail="Only SuperAdmin can access dashboard"
        )

    return {

        "summary": await get_summary(db),

        "task_status": await get_task_status(db),

        "role_distribution": await get_role_distribution(db),

        "group_performance": await get_group_performance(db),

        "top_employees": await get_top_employees(db),

        "workload": await get_employee_workload(db),

        "overdue_tasks": await get_overdue_tasks(db)

    }


# =======================================================
# Summary Cards
# =======================================================

async def get_summary(db: AsyncSession):

    total_users = await db.scalar(
        select(func.count(User.id))
        .where(User.is_active == True)
    )

    total_admins = await db.scalar(
        select(func.count(User.id))
        .join(Role)
        .where(
            Role.name == "Admin",
            User.is_active == True
        )
    )

    total_employees = await db.scalar(
        select(func.count(User.id))
        .join(Role)
        .where(
            Role.name == "Employee",
            User.is_active == True
        )
    )

    total_groups = await db.scalar(
        select(func.count(Group.id))
        .where(Group.is_active == True)
    )

    active_tasks = await db.scalar(
        select(func.count(Task.id))
        .where(
            Task.is_active == True,
            Task.status != TaskStatus.COMPLETED
        )
    )

    completed_today = await db.scalar(
        select(func.count(Task.id))
        .where(
            func.date(Task.completed_at) == datetime.now().date(),
            Task.status == TaskStatus.COMPLETED
        )
    )

    pending_reviews = await db.scalar(
        select(func.count(Task.id))
        .where(
            Task.approval_status == ApprovalStatus.SUBMITTED
        )
    )

    overdue_tasks = await db.scalar(
        select(func.count(Task.id))
        .where(
            Task.deadline < datetime.now(),
            Task.status != TaskStatus.COMPLETED
        )
    )

    return {

        "users": total_users or 0,

        "admins": total_admins or 0,

        "employees": total_employees or 0,

        "groups": total_groups or 0,

        "active_tasks": active_tasks or 0,

        "completed_today": completed_today or 0,

        "pending_reviews": pending_reviews or 0,

        "overdue_tasks": overdue_tasks or 0

    }


# =======================================================
# Task Status Chart
# =======================================================

async def get_task_status(db: AsyncSession):

    result = await db.execute(

        select(

            Task.status,

            func.count(Task.id)

        )

        .where(Task.is_active == True)

        .group_by(Task.status)

    )

    rows = result.all()

    response = {

        "todo": 0,

        "in_progress": 0,

        "submitted": 0,

        "completed": 0,

        "needs_revision": 0

    }

    for status, total in rows:

        if status == TaskStatus.TODO:
            response["todo"] = total

        elif status == TaskStatus.IN_PROGRESS:
            response["in_progress"] = total

        elif status == TaskStatus.SUBMITTED:
            response["submitted"] = total

        elif status == TaskStatus.COMPLETED:
            response["completed"] = total

    revision = await db.scalar(

        select(func.count(Task.id))

        .where(
            Task.approval_status == ApprovalStatus.NEEDS_REVISION
        )

    )

    response["needs_revision"] = revision or 0

    return response




# =====================================================
# Role Distribution (Pie Chart)
# =====================================================

async def get_role_distribution(db):

    result = await db.execute(
        select(
            Role.name,
            func.count(User.id)
        )
        .join(User, User.role_id == Role.id)
        .where(User.is_active == True)
        .group_by(Role.name)
    )

    response = {
        "super_admin": 0,
        "admin": 0,
        "employee": 0
    }

    for role, total in result.all():

        if role == "SuperAdmin":
            response["super_admin"] = total

        elif role == "Admin":
            response["admin"] = total

        elif role == "Employee":
            response["employee"] = total

    return response


# =====================================================
# Group Performance
# =====================================================

async def get_group_performance(db):

    Leader = aliased(User)

    result = await db.execute(

        select(

            Group.id,

            Group.name,

            Leader.username.label("leader_name"),

            func.count(Task.id).label("total_tasks"),

            func.sum(

                case(
                    (
                        Task.status == TaskStatus.COMPLETED,
                        1
                    ),
                    else_=0
                )

            ).label("completed_tasks")

        )

        .outerjoin(
            GroupMember,
            Group.id == GroupMember.group_id
        )

        .outerjoin(
            Leader,
            Leader.id == GroupMember.user_id
        )

        .outerjoin(
            Task,
            Task.group_id == Group.id
        )

        .where(
            Group.is_active == True
        )

        .group_by(
            Group.id,
            Group.name,
            Leader.username
        )

        .order_by(Group.name)

    )

    rows = result.all()

    response = []

    for row in rows:

        total = row.total_tasks or 0

        completed = row.completed_tasks or 0

        progress = 0

        if total > 0:

            progress = round(
                (completed / total) * 100,
                2
            )

        response.append({

            "group_id": row.id,

            "group_name": row.name,

            "leader": row.leader_name,

            "total_tasks": total,

            "completed_tasks": completed,

            "progress": progress

        })

    return response


# =====================================================
# Top Employees
# =====================================================

async def get_top_employees(db):

    result = await db.execute(

        select(

            User.id,

            User.username,

            func.count(Task.id).label("completed_tasks")

        )

        .join(
            Task,
            Task.assigned_to == User.id
        )

        .where(
            Task.status == TaskStatus.COMPLETED
        )

        .group_by(
            User.id,
            User.username
        )

        .order_by(
            func.count(Task.id).desc()
        )

        .limit(10)

    )

    rows = result.all()

    response = []

    for row in rows:

        response.append({

            "employee_id": row.id,

            "employee_name": row.username,

            "completed_tasks": row.completed_tasks

        })

    return response


from sqlalchemy import func, select
from app.modules.tasks.enums import TaskStatus


async def get_employee_workload(db):

    result = await db.execute(

        select(

            User.id,

            User.username,

            func.count(Task.id).label("pending_tasks")

        )

        .join(
            Task,
            Task.assigned_to == User.id
        )

        .where(

            Task.is_active == True,

            Task.status != TaskStatus.COMPLETED

        )

        .group_by(

            User.id,

            User.username

        )

        .order_by(

            func.count(Task.id).desc()

        )

    )

    rows = result.all()

    response = []

    for row in rows:

        response.append({

            "employee_id": row.id,

            "employee_name": row.username,

            "pending_tasks": row.pending_tasks

        })

    return response




async def get_overdue_tasks(db: AsyncSession):
    """Return list of overdue tasks with task title, assigned employee, and deadline.
    A task is overdue if its deadline is before current UTC time and status is not COMPLETED.
    """
    result = await db.execute(
        select(
            Task.title.label("task_title"),
            User.username.label("employee_name"),
            Task.deadline
        )
        .join(User, Task.assigned_to == User.id)
        .where(
            Task.deadline < datetime.utcnow(),
            Task.status != TaskStatus.COMPLETED,
            Task.is_active == True
        )
        .order_by(Task.deadline)
    )
    rows = result.all()
    response = []
    for row in rows:
        response.append({
            "task": row.task_title,
            "employee": row.employee_name,
            "deadline": row.deadline
        })
    return response
#
# get_summary()
# get_task_status()
# get_role_distribution()
# get_group_performance()
# get_top_employees()
# get_employee_workload()
# get_overdue_tasks()
#
# (Use the implementations I provided in the previous response.)