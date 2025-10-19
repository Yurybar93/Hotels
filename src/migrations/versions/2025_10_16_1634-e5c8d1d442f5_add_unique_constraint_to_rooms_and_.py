"""add unique constraint to rooms and citiex

Revision ID: e5c8d1d442f5
Revises: 36a4c07d5e7b
Create Date: 2025-10-16 16:34:01.175273

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "e5c8d1d442f5"
down_revision: Union[str, Sequence[str], None] = "36a4c07d5e7b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(
        "uix_title_location_hotel",
        "rooms",
        ["hotel_id", "title", "description", "price"],
    )


def downgrade() -> None:
    op.drop_constraint("uix_title_location_hotel", "rooms", type_="unique")
