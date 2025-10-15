"""enable citext and convert hotels columns to CITEXT

Revision ID: 36a4c07d5e7b
Revises: e26ea4be27e2
Create Date: 2025-10-15 15:09:22.430784

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "36a4c07d5e7b"
down_revision: Union[str, Sequence[str], None] = "e26ea4be27e2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        "hotels",
        "title",
        existing_type=sa.VARCHAR(length=100),
        type_=postgresql.CITEXT(),
        existing_nullable=False,
    )
    op.alter_column(
        "hotels",
        "location",
        existing_type=sa.VARCHAR(),
        type_=postgresql.CITEXT(),
        existing_nullable=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "hotels",
        "location",
        existing_type=postgresql.CITEXT(),
        type_=sa.VARCHAR(),
        existing_nullable=False,
    )
    op.alter_column(
        "hotels",
        "title",
        existing_type=postgresql.CITEXT(),
        type_=sa.VARCHAR(length=100),
        existing_nullable=False,
    )
