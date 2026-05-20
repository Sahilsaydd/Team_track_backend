from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, String
from datetime import datetime

from app.db.database import Base


class TaskEvidence(Base):
    __tablename__ = "task_evidences"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    description = Column(Text, nullable=False)
    screenshot_path = Column(String, nullable=True)
    file_path = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
