from app.db.database import async_session
from sqlalchemy.ext.asyncio import AsyncSession


async def get_db():
    db: AsyncSession = async_session()
    try:
        yield db
    finally:
        await db.close()

        