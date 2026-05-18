from sqlalchemy import Boolean, Column, DateTime
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import true


class TimestampMixin:
    is_active = Column(Boolean, nullable=False, default=True, server_default=true())
    created_at = Column(DateTime(timezone=True), nullable=False,default=func.now(),server_default=func.now())
