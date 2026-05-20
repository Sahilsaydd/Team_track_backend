"""make tasks deadline required

Revision ID: c2d3e4f5a6b7
Revises: 7b8c9d0e1f22
Create Date: 2026-05-20 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "c2d3e4f5a6b7"
down_revision: Union[str, Sequence[str], None] = "7b8c9d0e1f22"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(sa.text("UPDATE tasks SET deadline = created_at WHERE deadline IS NULL"))
    op.alter_column(
        "tasks",
        "deadline",
        existing_type=sa.DateTime(timezone=True),
        nullable=False,
    )


def downgrade() -> None:
    op.alter_column(
        "tasks",
        "deadline",
        existing_type=sa.DateTime(timezone=True),
        nullable=True,
    )
