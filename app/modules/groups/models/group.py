from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.database import Base
from app.db.mixins import TimestampMixin


class Group(TimestampMixin, Base):
    __tablename__ = "groups"

    id = Column(Integer,primary_key=True,index=True)

    name = Column(String,nullable=False)

    description = Column(String,nullable=True)

    group_code = Column(String, unique=True,nullable=False)

    profile_pic = Column(String, nullable=True)

    created_by = Column(Integer,ForeignKey("users.id") )
