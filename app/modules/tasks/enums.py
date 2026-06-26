import enum


class TaskStatus(str, enum.Enum):

    TODO = "todo"

    IN_PROGRESS = "in_progress"
    SUBMITTED = "submitted"
    COMPLETED = "completed"

    BLOCKED = "blocked"


class ApprovalStatus(str, enum.Enum):

    PENDING = "pending"

    SUBMITTED = "submitted"

    APPROVED = "approved"

    NEEDS_REVISION = "needs_revision"


class PriorityEnum(str, enum.Enum):

    LOW = "low"

    MEDIUM = "medium"

    HIGH = "high"