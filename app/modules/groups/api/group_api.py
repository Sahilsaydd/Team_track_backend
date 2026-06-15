from fastapi import APIRouter, Depends,status


from sqlalchemy.ext.asyncio import AsyncSession

from app.deps.db import get_db
from app.deps.auth_deps import get_current_user

from app.deps.auth_deps import require_role

from app.modules.groups.schemas.group_schema import (
    AddMemberSchema,
    ChangeLeaderSchema,
    UpdateGroupSchema,
    CreateGroupSchema,
    RemoveMemberSchema,
)
from app.modules.groups.services.group_service import (
    add_member_service,
    change_group_leader_service,
    create_group_service,
    deactivate_group_service,
    activate_group_service,
    get_all_groups_service,
    get_groups_by_creator_service,
    get_group_members_service,
    get_single_group_service,
    remove_member_service,
    get_My_Group,
    update_group_service
)

router = APIRouter(prefix="/groups",tags=["Groups"])


@router.post("/create",status_code=status.HTTP_201_CREATED)
async def create_group(data: CreateGroupSchema,db: AsyncSession = Depends(get_db),current_user = Depends(require_role(["Admin", "SuperAdmin"]))):
    return await create_group_service(db, data, current_user)


@router.get("/")
async def get_all_groups(db: AsyncSession = Depends(get_db) ,current_user = Depends(require_role(["Admin", "SuperAdmin"]))):
    return await get_all_groups_service(db)

@router.get("/my_groups")
async def get_my_groups(db:AsyncSession=Depends(get_db),current_user = Depends(get_current_user)):
    return await get_My_Group(db,current_user)


@router.get("/created-by/{creator_id}")
async def get_groups_by_creator(
    creator_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role(["Admin", "SuperAdmin"]))
):
    return await get_groups_by_creator_service(db, creator_id)


@router.get("/{group_id}")
async def get_single_group(group_id: int, db: AsyncSession = Depends(get_db) ):
    return await get_single_group_service(db, group_id)


@router.get("/{group_id}/members")
async def get_group_members(group_id: int, db: AsyncSession = Depends(get_db)):
    return await get_group_members_service(db, group_id)


@router.post("/members/add")
async def add_members(data: AddMemberSchema,db: AsyncSession = Depends(get_db), current_user = Depends(require_role(["Admin", "SuperAdmin"]))):
    return await add_member_service(db, data)


@router.delete("/members/remove")
async def remove_member(data: RemoveMemberSchema,db: AsyncSession = Depends(get_db), current_user = Depends(require_role(["Admin", "SuperAdmin"]))):
    return await remove_member_service(db, data)


@router.patch("/leader/change")
async def change_leader(data: ChangeLeaderSchema,db: AsyncSession = Depends(get_db), current_user = Depends(require_role(["Admin", "SuperAdmin"]))):
    return await change_group_leader_service(db, data)


@router.delete("/{group_id}")
async def deactivate_group(group_id: int,db: AsyncSession = Depends(get_db), current_user = Depends(require_role(["Admin", "SuperAdmin"]))):
    return await deactivate_group_service(db, group_id)


@router.put("/{group_id}")
async def activate_group(group_id: int , db:AsyncSession = Depends(get_db), current_user = Depends(require_role(["Admin", "SuperAdmin"]))):
    return await activate_group_service(db, group_id)

@router.put("/update/{group_id}")
async def update_group(group_id:int , data:UpdateGroupSchema ,db:AsyncSession=Depends(get_db)):
    return await update_group_service(db,group_id,data)