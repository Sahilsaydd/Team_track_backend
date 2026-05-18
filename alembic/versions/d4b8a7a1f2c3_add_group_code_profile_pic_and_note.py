"""add group_code profile_pic and note

Revision ID: d4b8a7a1f2c3
Revises: c3d2f6b7a9e1
Create Date: 2026-05-18 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "d4b8a7a1f2c3"
down_revision: Union[str, Sequence[str], None] = "c3d2f6b7a9e1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("groups", sa.Column("group_code", sa.String(length=100), nullable=False, server_default="TEMP"))
    op.add_column("groups", sa.Column("profile_pic", sa.String(length=255), nullable=True))
    op.add_column("group_members", sa.Column("note", sa.String(length=255), nullable=True))


def downgrade() -> None:
    op.drop_column("group_members", "note")
    op.drop_column("groups", "profile_pic")
    op.drop_column("groups", "group_code")
