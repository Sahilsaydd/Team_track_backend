from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CreateTaskSchema(BaseModel):

    title: str

    description: Optional[str]

    assigned_to: int

    priority: str
    group_id: int
    deadline: Optional[datetime]


class SelfTaskSchema(BaseModel):

    title: str

    description: Optional[str]

    priority: Optional[str] = "medium"


class UpdateTaskStatusSchema(BaseModel):

    status: str


class ReviewTaskSchema(BaseModel):

    review_status: str

    comment: str


# ==========================================
# CREATE TASK LOG
# ==========================================

class TaskLogSchema(BaseModel):

    task_id: int

    work_note: str

    hours_spent: float


# ==========================================
# RESPONSE TASK LOG
# ==========================================

class TaskLogResponseSchema(BaseModel):

    id: int

    task_id: int

    user_id: int

    work_note: str

    hours_spent: float

    created_at: datetime

    class Config:
        from_attributes = True