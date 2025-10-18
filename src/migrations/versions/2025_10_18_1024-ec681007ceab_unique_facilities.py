"""unique facilities

Revision ID: ec681007ceab
Revises: e5c8d1d442f5
Create Date: 2025-10-18 10:24:00

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "ec681007ceab"
down_revision: Union[str, Sequence[str], None] = "e5c8d1d442f5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # уникальность по title
    op.create_unique_constraint(None, "facilities", ["title"])

def downgrade() -> None:
    op.drop_constraint("facilities_title_key", "facilities", type_="unique")
