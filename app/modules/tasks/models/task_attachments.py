from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey

from datetime import datetime

from app.db.database import Base


class TaskAttachment(Base):

    __tablename__ = "task_attachments"

    id = Column(Integer, primary_key=True)

    task_id = Column(Integer,ForeignKey("tasks.id"))

    uploaded_by = Column(Integer,ForeignKey("users.id"))

    file_name = Column(String)

    file_url = Column(String)

    created_at = Column(DateTime,default=datetime.utcnow)