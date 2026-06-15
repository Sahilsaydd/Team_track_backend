from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException ,UploadFile
from datetime import datetime
from random import randint

from app.modules.groups.models.group import Group
from app.modules.groups.models.group_member import GroupMember
from app.modules.users.models.user import User
from app.core.file_upload import save_base64_file



def generate_group_code(name: str) -> str:
    slug = "".join(ch for ch in name.upper() if ch.isalnum())
    slug = slug[:8] or "GROUP"
    return f"{slug}-{datetime.utcnow().strftime('%Y%m%d')}-{randint(1000, 9999)}"


async def create_group_service(db: AsyncSession, data, current_user):

    group_code = generate_group_code(data.name)
    while True:
        result = await db.execute(
            select(Group).where(
                Group.group_code == group_code,
                Group.is_active == True
            )
        )
        if not result.scalar_one_or_none():
            break
        group_code = generate_group_code(data.name)

    profile_pic_path = None
    if data.profile_pic:
        profile_pic_path = save_base64_file(data.profile_pic, "groups")

    new_group = Group(
        name=data.name,
        description=data.description,
        group_code=group_code,
        profile_pic=profile_pic_path,
        created_by=current_user.id
    )

    db.add(new_group)
    await db.flush()

    leader_created = False

    for member in data.members:

        user_result = await db.execute(
            select(User).where(
                User.id == member.user_id,
                User.is_active == True
            ).options(selectinload(User.role))
        )

        existing_user = user_result.scalar_one_or_none()

        if not existing_user:
            raise HTTPException(
                status_code=404,
                detail=f"User {member.user_id} not found"
            )

        if not existing_user.role or existing_user.role.name != "Employee":
            raise HTTPException(
                status_code=400,
                detail=f"Only Employee users can be added to a team. User {member.user_id} is {existing_user.role.name if existing_user.role else 'unassigned'}"
            )

        normalized_role = (member.role_in_group or "Member").strip().title()
        if normalized_role == "Lead":
            if leader_created:
                raise HTTPException(
                    status_code=400,
                    detail="Only one leader is allowed in a group"
                )
            leader_created = True

        group_member = GroupMember(
            group_id=new_group.id,
            user_id=member.user_id,
            role_in_group=normalized_role,
            note=member.note
        )

        db.add(group_member)

    await db.commit()
    await db.refresh(new_group)

    return {
        "message": "Group created successfully",
        "group_id": new_group.id,
        "group_code": new_group.group_code,
        "profile_pic": new_group.profile_pic
    }

    

async def get_all_groups_service(
    db: AsyncSession
):

    result = await db.execute(select(Group).order_by(Group.created_at.desc()))

    groups = result.scalars().all()

    return groups


async def get_My_Group(db:AsyncSession ,current_user):
    result = await db.execute(
        select(Group)
        .join(
            GroupMember,
            Group.id == GroupMember.group_id
        )
        .where(
            GroupMember.user_id == current_user.id,
            GroupMember.is_active == True,
            Group.is_active == True
        )
        .order_by(Group.created_at.desc())
    )

    return result.scalars().all()
    

async def get_groups_by_creator_service(
    db: AsyncSession,
    creator_id: int
):

    result = await db.execute(
        select(Group).where(
            Group.created_by == creator_id,
            Group.is_active == True
        )
    )

    groups = result.scalars().all()

    return groups



async def add_member_service(
    db: AsyncSession,
    data
):

    group_result = await db.execute(
        select(Group).where(
            Group.id == data.group_id,
            Group.is_active == True
        )
    )

    group = group_result.scalar_one_or_none()

    if not group:
        raise HTTPException(
            status_code=404,
            detail="Group not found"
        )

    existing_leader_result = await db.execute(
        select(GroupMember).where(
            GroupMember.group_id == data.group_id,
            GroupMember.role_in_group == "Lead",
            GroupMember.is_active == True
        )
    )
    existing_leader = existing_leader_result.scalar_one_or_none()

    for member in data.members:

        user_result = await db.execute(
            select(User).where(
                User.id == member.user_id,
                User.is_active == True
            ).options(selectinload(User.role))
        )

        user = user_result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=404,
                detail=f"User {member.user_id} not found"
            )

        if not user.role or user.role.name != "Employee":
            raise HTTPException(
                status_code=400,
                detail=f"Only Employee users can be added to a team. User {member.user_id} is {user.role.name if user.role else 'unassigned'}"
            )

        existing_member_result = await db.execute(
            select(GroupMember).where(
                GroupMember.group_id == data.group_id,
                GroupMember.user_id == member.user_id,
                GroupMember.is_active == True
            )
        )

        existing_member = existing_member_result.scalar_one_or_none()

        if existing_member:
            continue

        new_member = GroupMember(
            group_id=data.group_id,
            user_id=member.user_id,
            role_in_group="Member",
            note=member.note
        )

        db.add(new_member)

    await db.commit()

    return {
        "message": "Members added successfully"
    }



async def remove_member_service(
    db: AsyncSession,
    data
):

    result = await db.execute(
        select(GroupMember).where(
            GroupMember.group_id == data.group_id,
            GroupMember.user_id == data.user_id,
            GroupMember.is_active == True
        )
    )

    member = result.scalar_one_or_none()

    if not member:
        raise HTTPException(
            status_code=404,
            detail="Member not found in group"
        )

    member.is_active = False

    await db.commit()

    return {
        "message": "Member removed successfully"
    }



async def change_group_leader_service(
    db: AsyncSession,
    data
):

    old_leader_result = await db.execute(
        select(GroupMember).where(
            GroupMember.group_id == data.group_id,
            GroupMember.role_in_group == "Lead",
            GroupMember.is_active == True
        )
    )

    old_leader = old_leader_result.scalar_one_or_none()

    if old_leader:
        old_leader.role_in_group = "Member"

    new_leader_result = await db.execute(
        select(GroupMember).where(
            GroupMember.group_id == data.group_id,
            GroupMember.user_id == data.new_leader_id,
            GroupMember.is_active == True
        )
    )

    new_leader = new_leader_result.scalar_one_or_none()

    if not new_leader:
        raise HTTPException(
            status_code=404,
            detail="New leader not found in group"
        )

    new_leader.role_in_group = "Lead"

    await db.commit()

    return {
        "message": "Group leader updated successfully"
    }



async def deactivate_group_service(db: AsyncSession,group_id: int):

    result = await db.execute(
        select(Group).where(
            Group.id == group_id,
            Group.is_active == True
        )
    )

    group = result.scalar_one_or_none()

    if not group:
        raise HTTPException(
            status_code=404,
            detail="Group not found"
        )

    group.is_active = False

    await db.commit()

    return {
        "message": "Group deactivated successfully"
    }

async def activate_group_service(db:AsyncSession, group_id:int):
    result = await db.execute(
        select(Group).where(
            Group.id == group_id,
            Group.is_active == False
        )
    )
    group = result.scalar_one_or_none()

    if not group:
        raise HTTPException(
            status_code=404,
            detail="Group not found"
        )

    group.is_active =True

    await db.commit()
    return {
        "Massage":"Group Activated Successfully"
    }







async def get_single_group_service(
    db: AsyncSession,
    group_id: int
):

    result = await db.execute(
        select(Group).where(
            Group.id == group_id,
            Group.is_active == True
        )
    )

    group = result.scalar_one_or_none()

    if not group:
        raise HTTPException(
            status_code=404,
            detail="Group not found"
        )

    return group




async def get_group_members_service(
    db: AsyncSession,
    group_id: int
):

    result = await db.execute(
        select(
            GroupMember.id,
            GroupMember.role_in_group,
            GroupMember.is_active,
            GroupMember.note,
            GroupMember.group_id,
            GroupMember.user_id,
            GroupMember.created_at,

            User.email,
            User.username
        )
        .join(
            User,
            User.id == GroupMember.user_id
        )
        .where(
            GroupMember.group_id == group_id,
            GroupMember.is_active == True
        )
    )

    members = result.mappings().all()

    # fetch leader details separately (if any)
    leader_result = await db.execute(
        select(
            GroupMember.id,
            GroupMember.role_in_group,
            GroupMember.note,
            GroupMember.group_id,
            GroupMember.user_id,
            GroupMember.created_at,
            User.email,
            User.username
        )
        .join(User, User.id == GroupMember.user_id)
        .where(
            GroupMember.group_id == group_id,
            GroupMember.role_in_group == "Lead",
            GroupMember.is_active == True
        )
    )

    leader = leader_result.mappings().first()

    return {
        "members": members,
        "leader": leader
    }

async def update_group_service(
    db: AsyncSession,
    group_id: int,
    data
):

    result = await db.execute(
        select(Group).where(Group.id == group_id)
    )

    group = result.scalar_one_or_none()

    if not group:
        raise HTTPException(
            status_code=404,
            detail="Group not found"
        )

    # Name validation
    if len(data.name.strip()) < 3:
        raise HTTPException(
            status_code=400,
            detail="Group name must be at least 3 characters"
        )

    # Description validation
    if len(data.description.strip()) < 5:
        raise HTTPException(
            status_code=400,
            detail="Description must be at least 5 characters"
        )

    # Duplicate name check
    duplicate = await db.execute(
        select(Group).where(
            Group.name == data.name,
            Group.id != group_id
        )
    )

    if duplicate.scalar_one_or_none():
        raise HTTPException(
            status_code=400,
            detail="Group name already exists"
        )

    # Update image only if new image received
    if data.profile_pic:
        group.profile_pic = save_base64_file(
            data.profile_pic,
            "groups"
        )

    group.name = data.name
    group.description = data.description
    group.is_active = data.is_active

    await db.commit()
    await db.refresh(group)

    return {
        "message": "Group updated successfully",
        "group": {
            "id": group.id,
            "name": group.name,
            "description": group.description,
            "group_code": group.group_code,
            "profile_pic": group.profile_pic,
            "is_active": group.is_active
        }
    }

