from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.config import settings
from app.deps.db import get_db
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.modules.users.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError

security = HTTPBearer(auto_error=False)

# Read the token from the cookie and get the current user

async def get_current_user(
    request: Request,
    db: AsyncSession = Depends(get_db),
    token: HTTPAuthorizationCredentials = Depends(security)
):
    credentials_exception = HTTPException(
        status_code=401, detail="Invalid Token"
    )
    
    access_token = None
    if token:
        access_token = token.credentials

    # Prioritize Authorization header (tab-scoped) over cookies (browser-wide)
    if not access_token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            access_token = auth_header.removeprefix("Bearer ").strip()

    if not access_token:
        access_token = request.cookies.get("access_token")

    if not access_token:
        raise credentials_exception
    
    
    
    try:
        if access_token.startswith("Bearer "):
            access_token = access_token.removeprefix("Bearer ").strip()

        payload = jwt.decode(
            access_token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        print(payload)
        user_id = payload.get("sub")
        if not user_id :
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
                detail="You don't have permission to access this resource Only {} can access".format(", ".join(allowed_role))
            )

        return current_user

    return checker
