from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError

from app.core.config import settings
from app.deps.db import get_db
from app.modules.users.models.user import User

security = HTTPBearer(auto_error=False)


async def get_current_user(
    db: AsyncSession = Depends(get_db),
    token: HTTPAuthorizationCredentials = Depends(security)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid Token"
    )

    if not token:
        raise credentials_exception

    access_token = token.credentials

    try:
        payload = jwt.decode(
            access_token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        user_id = payload.get("sub")

        if not user_id:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    result = await db.execute(
        select(User)
        .options(selectinload(User.role))
        .where(User.id == int(user_id))
    )

    user = result.scalar_one_or_none()

    if not user:
        raise credentials_exception

    return user


def require_role(allowed_role: list):

    async def checker(
        current_user: User = Depends(get_current_user)
    ):

        if current_user.role.name not in allowed_role:
            raise HTTPException(
                status_code=403,
                detail=f"You don't have permission to access this resource. Only {', '.join(allowed_role)} can access."
            )

        return current_user

    return checker