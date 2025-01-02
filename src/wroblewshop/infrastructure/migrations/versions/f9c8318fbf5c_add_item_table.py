"""Add item table

Revision ID: f9c8318fbf5c
Revises: e9c97ae0d208
Create Date: 2024-12-15 21:10:51.525512

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f9c8318fbf5c"
down_revision: Union[str, None] = "e9c97ae0d208"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "item",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.Text, unique=True, nullable=False),
        sa.Column(
            "cupboard_id", sa.Integer, sa.ForeignKey("cupboard.id", name="item_cupboard_id_fkey"), nullable=False
        ),
    )


def downgrade() -> None:
    op.drop_table("item")
