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


class TaskEvidenceResponseSchema(BaseModel):
    id: int
    task_id: int
    user_id: int
    description: str
    screenshot_path: Optional[str] = None
    file_path: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True



class TaskLogSchema(BaseModel):

    task_id: int

    work_note: str

    hours_spent: float



class TaskLogResponseSchema(BaseModel):

    id: int

    task_id: int

    user_id: int

    work_note: str

    hours_spent: float

    created_at: datetime

    class Config:
        from_attributes = True





class CreatePersonalTaskSchemas(BaseModel):
    title: str

    description: str

    assigned_to: int

    priority: str

    deadline: datetime



class TaskReviewResponse(BaseModel):
    id:int
    task_id:int
    reviewed_by:int
    reviewed_status:str
    comment:str | None
    created_at:datetime

    class Config:
        from_attributes = True


class TaskReportExportResponse(BaseModel):
    message: str
    file_name: str
    file_path: str
