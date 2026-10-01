"""Make CV unique per user

Revision ID: fd7afc01ac9b
Revises: 605b5017ec96
Create Date: 2026-09-16
"""

from typing import Sequence, Union

from alembic import op


revision: str = "fd7afc01ac9b"
down_revision: Union[str, Sequence[str], None] = "605b5017ec96"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(
        "uq_cvs_user_id",
        "cvs",
        ["user_id"],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        "uq_cvs_user_id",
        "cvs",
        type_="unique",
    )
