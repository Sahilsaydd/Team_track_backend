from pydantic import BaseModel
from datetime import datetime


class NotificationResponseSchema(BaseModel):

    id: int

    title: str

    message: str

    notification_type: str

    is_read: bool

    created_at: datetime

    class Config:
        from_attributes = True