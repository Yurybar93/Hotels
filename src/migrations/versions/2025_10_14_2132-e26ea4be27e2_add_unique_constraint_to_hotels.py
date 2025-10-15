"""add unique constraint to hotels

Revision ID: e26ea4be27e2
Revises: 3b924b7eef99
Create Date: 2025-10-14 21:32:50.064140

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e26ea4be27e2"
down_revision: Union[str, Sequence[str], None] = "3b924b7eef99"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint("uix_title_location", "hotels", ["title", "location"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("uix_title_location", "hotels", type_="unique")
