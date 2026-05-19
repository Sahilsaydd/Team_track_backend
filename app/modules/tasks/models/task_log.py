from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy import Float
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey

from datetime import datetime

from app.db.database import Base


class TaskLog(Base):

    __tablename__ = "task_logs"

    id = Column(Integer, primary_key=True)

    task_id = Column(Integer,ForeignKey("tasks.id"))

    user_id = Column(Integer,ForeignKey("users.id"))

    work_note = Column(Text)

    hours_spent = Column(Float)

    created_at = Column(DateTime,default=datetime.utcnow)