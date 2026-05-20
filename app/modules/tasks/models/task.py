from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import DateTime
from sqlalchemy import Boolean
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.database import Base

from app.modules.tasks.enums import (
    TaskStatus,
    ApprovalStatus,
    PriorityEnum
)


class Task(Base):

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)

    description = Column(Text)

    status = Column(String,default=TaskStatus.TODO.value)

    approval_status = Column(String,default=ApprovalStatus.PENDING.value)

    priority = Column(String,default=PriorityEnum.MEDIUM.value)

    created_by = Column(Integer,ForeignKey("users.id"))

    assigned_by = Column(Integer,ForeignKey("users.id"))

    assigned_to = Column(Integer,ForeignKey("users.id"))
    task_type = Column(String ,default="personal")
    submitted_to = Column(Integer,ForeignKey("users.id"))

    group_id = Column(Integer,ForeignKey("groups.id"))

    is_self_task = Column(Boolean,default=False)

    deadline = Column(DateTime(timezone=True), nullable=False)

    created_at = Column(DateTime(timezone=True),server_default=func.now())

    group = relationship("Group")
