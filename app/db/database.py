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
from app.modules.groups.models.group import Group
from app.modules.groups.models.group_member import GroupMember
from app.modules.tasks.models.task import Task

from app.modules.tasks.models.task_log import TaskLog

from app.modules.tasks.models.task_comment import TaskComment

from app.modules.tasks.models.task_attachments import TaskAttachment

from app.modules.tasks.models.task_review import TaskReview

from app.modules.notification.model.notification import Notification