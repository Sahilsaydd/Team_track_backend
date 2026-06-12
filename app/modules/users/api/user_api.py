from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.deps.db import get_db
from typing import List
from app.deps.auth_deps import get_current_user , require_role
from app.modules.users.schemas.user_schema import UserSchema , CreateEmployeeSchema ,UserResponseSchema
from app.modules.users.services.user_service import ( create_admin_service , create_employee_service 
    ,get_all_employees_service,get_all_admins ,get_all_users_service, deactivate_user_service,deactivated_users ,activate_user_again)
router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/create_admin",status_code=status.HTTP_201_CREATED)
async def create_Admin(data:UserSchema , db:AsyncSession=Depends(get_db) , current_user = Depends(require_role(["SuperAdmin"]))):
    return await create_admin_service(db,data,current_user)

@router.post("/create_employee",status_code=status.HTTP_201_CREATED)
async def create_employee(data: CreateEmployeeSchema,db: AsyncSession = Depends(get_db),current_user = Depends(require_role(["SuperAdmin" , "Admin"]))
):

    return await create_employee_service(
        db,
        data,
        current_user
    )


@router.get("/all_employees",response_model=List[UserResponseSchema])
async def get_all_employees( db:AsyncSession=Depends(get_db),current_user = Depends(require_role([ "SuperAdmin","Admin"]))):
    return await get_all_employees_service(db)


@router.get("/all_admins",response_model=List[UserResponseSchema])
async def get_all_admin(db:AsyncSession=Depends(get_db),current_user = Depends(require_role(["SuperAdmin"]))):
    return await get_all_admins(db)

@router.get("/")
async def get_all_users(db: AsyncSession = Depends(get_db),current_user = Depends(require_role([ "SuperAdmin"]))):
    return await get_all_users_service(db)


@router.put("/deactivate/{user_id}")
async def deactivate_user(user_id: int,db: AsyncSession = Depends(get_db),current_user = Depends(require_role(["Admin", "SuperAdmin"]))):
    return await deactivate_user_service(user_id, db)

@router.get("/deactivate" , response_model=List[UserResponseSchema])
async def all_deactivated_users(db:AsyncSession = Depends(get_db) , current_user = Depends(require_role(["Admin","SuperAdmin"]))):
    return await deactivated_users(db)


@router.put("/activate/{user_id}")
async def activate_user(user_id:int , db:AsyncSession=Depends(get_db), current_user = Depends(require_role(["Admin", "SuperAdmin"]))):
    return await activate_user_again(user_id,db)

