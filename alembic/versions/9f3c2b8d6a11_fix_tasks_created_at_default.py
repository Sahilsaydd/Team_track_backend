"""fix tasks created_at default

Revision ID: 9f3c2b8d6a11
Revises: c371f0993dfd
Create Date: 2026-05-20 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "9f3c2b8d6a11"
down_revision: Union[str, Sequence[str], None] = "c371f0993dfd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(sa.text("UPDATE tasks SET created_at = NOW() WHERE created_at IS NULL"))
    op.alter_column(
        "tasks",
        "created_at",
        existing_type=sa.DateTime(),
        nullable=False,
        server_default=sa.text("now()"),
    )


def downgrade() -> None:
    op.alter_column(
        "tasks",
        "created_at",
        existing_type=sa.DateTime(),
        nullable=True,
        server_default=None,
    )
