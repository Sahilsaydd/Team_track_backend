from enum import Enum


class ReportType(str, Enum):

    DAILY = "daily"

    WEEKLY = "weekly"

    MONTHLY = "monthly"

    YEARLY = "yearly"