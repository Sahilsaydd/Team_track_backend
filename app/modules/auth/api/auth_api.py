from fastapi import APIRouter , Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from app.deps.db import get_db
from app.modules.auth.services.auth_service import login_service


router = APIRouter(prefix='/auth' , tags=['auth'])

@router.post("/login")
async def login(data: OAuth2PasswordRequestForm = Depends(), db:AsyncSession = Depends(get_db)):
    return await login_service(db, data)
