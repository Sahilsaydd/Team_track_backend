from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker ,declarative_base
from app.core.config import settings

Database_url = settings.Database_url
engine = create_async_engine(Database_url ,echo=True)
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

Base = declarative_base()


from app.modules.users.models.user import User
from app.modules.roles.model.role import Role