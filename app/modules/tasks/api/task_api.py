

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


from app.deps.db import get_db

from app.deps.auth_deps import get_current_user ,require_role

from app.modules.tasks.schemas.task_schema import (
    CreateTaskSchema,
    SelfTaskSchema,
    UpdateTaskStatusSchema,
    ReviewTaskSchema,
    TaskLogSchema,
    TaskLogResponseSchema
    
)

from app.modules.tasks.services.task_service import (
    create_task_service,
    create_self_task_service,
    update_task_status_service,
    add_task_log_service,
    submit_task_service,
    review_task_service,
    get_my_tasks_service,
    get_group_tasks_service,
    get_all_tasks_service
)

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)



@router.post("/assign")
async def assign_task_api(data: CreateTaskSchema, db: AsyncSession = Depends(get_db),current_user = Depends(get_current_user)):

    return await create_task_service(
        db,
        data,
        current_user
    )



@router.post("/self")
async def create_self_task_api(
    data: SelfTaskSchema,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return await create_self_task_service(
        db,
        data,
        current_user
    )



@router.patch("/{task_id}/status")
async def update_task_status_api(
    task_id: int,
    data: UpdateTaskStatusSchema,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return await update_task_status_service(
        db,
        task_id,
        data,
        current_user
    )



@router.post("/logs")
async def add_task_log_api(
    data: TaskLogSchema,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return await add_task_log_service(
        db,
        data,
        current_user
    )



@router.post("/{task_id}/submit")
async def submit_task_api(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return await submit_task_service(
        db,
        task_id,
        current_user
    )



@router.post("/{task_id}/review")
async def review_task_api(
    task_id: int,
    data: ReviewTaskSchema,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return await review_task_service(
        db,
        task_id,
        data,
        current_user
    )



@router.get("/my")
async def get_my_tasks_api(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return await get_my_tasks_service(
        db,
        current_user
    )



@router.get("/group")
async def get_group_tasks_api(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return await get_group_tasks_service(
        db,
        current_user
    )



@router.get("/all")
async def get_all_tasks_api(
    db: AsyncSession = Depends(get_db)
):

    return await get_all_tasks_service(db)