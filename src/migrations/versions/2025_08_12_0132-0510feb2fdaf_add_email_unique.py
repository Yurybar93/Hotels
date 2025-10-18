"""add email unique

Revision ID: 0510feb2fdaf
Revises: 5fdd21e6f23d
Create Date: 2025-08-12 01:32:40.392211

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "0510feb2fdaf"
down_revision: Union[str, Sequence[str], None] = "5fdd21e6f23d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    op.drop_constraint(None, "users", type_="unique")  # type: ignore
