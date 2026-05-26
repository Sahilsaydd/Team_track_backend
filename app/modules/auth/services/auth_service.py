from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select

from sqlalchemy.orm import selectinload

from fastapi import Response
from fastapi import HTTPException
from fastapi import status

from app.modules.users.models.user import User

from app.core.security import (
    verify_password,
    create_access_token
)


async def login_service(db: AsyncSession,data,response: Response):


    result = await db.execute(select(User).options(selectinload(User.role)).where(User.email == data.email))

    user = result.scalar_one_or_none()


    if not user:

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid email or password")


    if not verify_password(data.password,user.password):

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid email or password")


    token = create_access_token({"sub": str(user.id),"role": user.role.name})


    response.set_cookie(
    key="access_token",
    value=token,
    httponly=True,
    secure=False,
    samesite="lax",
    path="/",
    max_age=60 * 60 * 24
)


    return {

        "message": "Login Successful",
        "access_token": token,
        "role": user.role.name,

        "user": {

            "id": user.id,

            "email": user.email,

            "name": user.username,

            "role": user.role.name

        }

    }

# Logout service
async def logout_service(response: Response):

    response.delete_cookie(
        key="access_token",
        httponly=True,
        path="/",
        secure=False,
        samesite="lax"
    )

    return {
        "message": "Logout successful"
    }
