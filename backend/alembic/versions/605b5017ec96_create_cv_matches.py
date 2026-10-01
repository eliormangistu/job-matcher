"""Create CV matches

Revision ID: 605b5017ec96
Revises: fb021e71eb44
Create Date: 2026-09-16 16:22:17.433589

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "605b5017ec96"
down_revision: Union[str, Sequence[str], None] = "fb021e71eb44"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "cv_matches",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("cv_id", sa.Integer(), nullable=False),
        sa.Column("job_id", sa.Integer(), nullable=False),
        sa.Column("score", sa.Float(), nullable=False),
        sa.Column("matched_skills", sa.JSON(), nullable=False),
        sa.Column("missing_skills", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["cv_id"], ["cvs.id"]),
        sa.ForeignKeyConstraint(["job_id"], ["jobs.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    pass
