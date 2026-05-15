from fastapi import APIRouter ,Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.deps.db import get_db
from app.deps.auth_deps import get_current_user , require_role
from app.modules.users.schemas.user_schema import UserSchema , CreateEmployeeSchema
from app.modules.users.services.user_service import create_admin_service , create_employee_service
router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/create_admin")
async def create_Admin(data:UserSchema , db:AsyncSession=Depends(get_db) , current_user = Depends(get_current_user)):
    return await create_admin_service(db,data,current_user)

@router.post("/create-employee")
async def create_employee(
    data: CreateEmployeeSchema,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role(["SuperAdmin" , "Admin"]))
):

    return await create_employee_service(
        db,
        data,
        current_user
    )