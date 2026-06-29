from pydantic import BaseModel
from datetime import datetime


class DashboardSummarySchema(BaseModel):
    users: int
    admins: int
    employees: int
    groups: int
    active_tasks: int
    completed_today: int
    pending_reviews: int
    overdue_tasks: int


class TaskStatusSchema(BaseModel):
    todo: int = 0
    in_progress: int = 0
    submitted: int = 0
    completed: int = 0
    needs_revision: int = 0


class RoleDistributionSchema(BaseModel):
    super_admin: int = 0
    admin: int = 0
    employee: int = 0


class GroupPerformanceSchema(BaseModel):
    group_id: int
    group_name: str
    leader: str
    total_tasks: int
    completed_tasks: int
    progress: float


class TopEmployeeSchema(BaseModel):
    employee_id: int
    employee_name: str
    completed_tasks: int


class WorkloadSchema(BaseModel):
    employee_id: int
    employee_name: str
    pending_tasks: int


class OverdueTaskSchema(BaseModel):
    task: str
    employee: str
    deadline: datetime


class DashboardResponseSchema(BaseModel):
    summary: DashboardSummarySchema
    task_status: TaskStatusSchema
    role_distribution: RoleDistributionSchema

    group_performance: list[GroupPerformanceSchema]

    top_employees: list[TopEmployeeSchema]

    workload: list[WorkloadSchema]

    overdue_tasks: list[OverdueTaskSchema]