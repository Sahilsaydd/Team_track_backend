# app/modules/notifications/models/notification.py

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey

from datetime import datetime

from app.db.database import Base


class Notification(Base):

    __tablename__ = "notifications"

    id = Column(Integer,primary_key=True,index=True)

    # receiver user
    user_id = Column(Integer,ForeignKey("users.id"),nullable=False)

    title = Column(String,nullable=False)

    message = Column(Text,nullable=False)

    notification_type = Column(String,nullable=False)

    is_read = Column(Boolean,default=False)

    created_at = Column(DateTime,default=datetime.utcnow)