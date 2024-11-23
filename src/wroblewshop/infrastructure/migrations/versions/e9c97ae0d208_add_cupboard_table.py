"""Add cupboard table

Revision ID: e9c97ae0d208
Revises: 9aea673aeeac
Create Date: 2024-11-18 20:55:02.666387

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e9c97ae0d208"
down_revision: Union[str, None] = "9aea673aeeac"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "cupboard",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.Text, unique=True, nullable=False),
    )
    with op.batch_alter_table("user") as batch_op:
        batch_op.add_column(
            sa.Column(
                "cupboard_id", sa.Integer, sa.ForeignKey("cupboard.id", name="user_cupboard_id_fkey"), nullable=False
            )
        )


def downgrade() -> None:
    with op.batch_alter_table("user") as batch_op:
        batch_op.drop_column(column_name="cupboard_id")

    op.drop_table("cupboard")
