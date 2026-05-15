from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from app.modules.users.models.user import User
from app.modules.roles.model.role import Role
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

   # check email is exit or not 
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
   db.refresh(new_employee)
   return {
         "Message" : "Employee Created Successfully"
   }