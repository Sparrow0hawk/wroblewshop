"""Add user table

Revision ID: 9aea673aeeac
Revises: 
Create Date: 2024-10-10 20:36:42.352504

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "9aea673aeeac"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("user", sa.Column("id", sa.Integer, primary_key=True), sa.Column("email", sa.Text))


def downgrade() -> None:
    op.drop_table("user")
