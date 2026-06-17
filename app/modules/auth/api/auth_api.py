from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from app.deps.auth_deps import get_current_user
from app.deps.db import get_db
from app.modules.auth.services.auth_service import login_service
from app.modules.auth.schemas.login_schema import LoginSchema
from app.modules.auth.services.auth_service import logout_service

router = APIRouter(prefix='/auth' , tags=['auth'])

@router.post("/login")
async def login(
    data: LoginSchema,
    db: AsyncSession = Depends(get_db)
):
    return await login_service(
        db,
        data
    )

@router.post("/logout")
async def logout():
    return await logout_service()
