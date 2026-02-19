"""initial schema

Revision ID: 202602191300
Revises:
Create Date: 2026-02-19 13:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "202602191300"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "machines",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
    )
    op.create_index("ix_machines_id", "machines", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_machines_id", table_name="machines")
    op.drop_table("machines")
