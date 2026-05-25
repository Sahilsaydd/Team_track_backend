from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import DateTime
from sqlalchemy import Boolean
from sqlalchemy import Float
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

    is_active = Column(Boolean, default=True, nullable=False, server_default=func.true())

    deadline = Column(DateTime(timezone=True), nullable=False)

    created_at = Column(DateTime(timezone=True),server_default=func.now())
     # =========================
    # NEW FIELDS
    # =========================

    project_name = Column(
        String,
        nullable=True
    )

    worked_hours = Column(
        Float,
        default=0
    )

    is_recurring = Column(
        Boolean,
        default=False
    )

    recurring_type = Column(
        String,
        nullable=True
    )

    last_activity_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    reminder_sent = Column(
        Boolean,
        default=False
    )

    completed_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    blocked_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    overdue_at = Column(
        DateTime(timezone=True),
        nullable=True
    )


    group = relationship("Group")
