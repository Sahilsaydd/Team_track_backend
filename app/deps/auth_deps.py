from fastapi import Depends , HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt , JWTError
from app.core.config import settings
from app.deps.db import get_db
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.modules.users.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Cookie

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)

# Read the token from the cookie and get the current user

async def get_current_user(token: str = Cookie(None), db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401, detail="Invalid Token"
    )
    if not token:
        raise credentials_exception
    
    
    
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            settings.ALGORITHM
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