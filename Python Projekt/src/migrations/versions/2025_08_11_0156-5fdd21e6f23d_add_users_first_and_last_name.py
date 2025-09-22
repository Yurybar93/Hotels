"""add users(first and last name)

Revision ID: 5fdd21e6f23d
Revises: a7629d4ef0a2
Create Date: 2025-08-11 01:56:04.768958

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "5fdd21e6f23d"
down_revision: Union[str, Sequence[str], None] = "a7629d4ef0a2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("first_name", sa.String(length=100), nullable=False))
    op.add_column("users", sa.Column("last_name", sa.String(length=100), nullable=False))


def downgrade() -> None:
    op.drop_column("users", "last_name")
    op.drop_column("users", "first_name")
