from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from app.modules.users.models.user import User
from app.modules.roles.model.role import Role
from sqlalchemy.orm import joinedload
from app.core.security import hash_password

async def create_admin_service(db:AsyncSession ,data ,  current_user):

    if current_user.role.name != "SuperAdmin":

        raise HTTPException(
            status_code=403,
            detail="Only SuperAdmin can create admin"
        )
    
    result = await db.execute(select(User).where(User.email == data.email))
    
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=400 , detail= "Email already exits")
    
    role_result = await db.execute(select(Role).where(Role.name=="Admin"))

    admin_role =role_result.scalar_one()
    new_admin  = User(
        username = data.username,
        email = data.email,
        password = hash_password(data.password),
        role_id = admin_role.id
    

    )

    db.add(new_admin)
    await db.commit()
    await db.refresh(new_admin)
    return {
        "Massage" : "Admin Created Successfully"
    }


async def create_employee_service(db:AsyncSession,data,current_user):

   result = await db.execute(select(User).where(User.email == data.email))
   existing_user = result.scalar_one_or_none()
   if existing_user:
       raise HTTPException(status_code=400 , detail="Email already exists")
   
   role_result = await db.execute(select(Role).where(Role.name == "Employee"))
   employee_role = role_result.scalar_one()

   new_employee = User(
       username = data.username,
       email = data.email,
       password = hash_password(data.password),
       role_id = employee_role.id

   )
   db.add(new_employee)
   await db.commit()
   await db.refresh(new_employee)
   return {
         "Message" : "Employee Created Successfully",
         "username":new_employee.username,
         "email":new_employee.email,
         "role": employee_role.name,
   }



async def get_all_employees_service(db:AsyncSession):
    result = await db.execute(select(User).options(joinedload(User.role)).join(Role).where(Role.name=="Employee").order_by(User.created_at.desc()))

    employees =  result.scalars().all()
    return [
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role.name,
            "is_active": user.is_active,
            "created_at": user.created_at
        }
        for user in employees
    ]


async def get_all_admins(db:AsyncSession):
    result = await db.execute(select(User).options(joinedload(User.role)).join(Role).where(Role.name=="Admin",User.is_active==True))

    admins = result.scalars().all()
    return [
    {
        "id": admin.id,
        "username": admin.username,
        "email": admin.email,
        "role": admin.role.name,
        "is_active": admin.is_active,
        "created_at": admin.created_at
    }
    for admin in admins
]


async def get_all_users_service(db: AsyncSession):

    result = await db.execute(
        select(User)
        .options(joinedload(User.role))
        .order_by(User.created_at.desc())
    )

    users = result.scalars().all()

    return [
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role.name,
            "is_active": user.is_active,
            "created_at": user.created_at
        }
        for user in users
    ]


async def deactivate_user_service(user_id: int, db: AsyncSession):

    result = await db.execute(
        select(User).where(User.id == user_id , User.is_active == True)
    )

    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    user.is_active = False

    await db.commit()

    return {
        "message": "User deactivated successfully",
        "Username":user.username,
        "is_active":user.is_active
    }



async def deactivated_users(db:AsyncSession):
    result = await db.execute(select(User).options(joinedload(User.role)).where(User.is_active == False))
    users = result.scalars().all()
    if not users:
        raise HTTPException(status_code=404 , detail=" Deactivated  Users Not Found")
    
    return [
       {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role.name,
            "is_active": user.is_active,
            "created_at": user.created_at
        }
        for user in users
    ]

async def activate_user_again(user_id , db:AsyncSession):
    result = await db.execute(select(User).where(User.id==user_id , User.is_active==False))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User Not Found")
    
    user.is_active=True
    await db.commit()

    return {
        "massage":"User Activated SuccessFully",
        "Username":user.username,
        "is_active":user.is_active
    }