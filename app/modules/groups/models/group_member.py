from sqlalchemy import Column, Integer, ForeignKey, String
from app.db.database import Base
from app.db.mixins import TimestampMixin


class GroupMember(TimestampMixin, Base):
    __tablename__ = "group_members"

    id = Column(Integer, primary_key=True, index=True)

    group_id = Column(Integer,ForeignKey("groups.id"),nullable=False)

    user_id = Column(Integer,ForeignKey("users.id"),nullable=False)

    role_in_group = Column(String,default="Member")

    note = Column(String,nullable=True)
