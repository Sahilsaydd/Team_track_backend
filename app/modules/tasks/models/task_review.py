from sqlalchemy import Column ,String , Text ,DateTime, Enum ,ForeignKey ,Integer
from datetime import datetime
from app.db.database import Base
from app.modules.tasks.enums import ApprovalStatus

class TaskReview(Base):
    __tablename__ ="task_reviews"
    
    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    reviewed_by = Column(Integer, ForeignKey("users.id"))
    reviewed_status = Column(Enum(ApprovalStatus))
    comment = Column(Text)
    created_at = Column(DateTime , default=datetime.utcnow())
