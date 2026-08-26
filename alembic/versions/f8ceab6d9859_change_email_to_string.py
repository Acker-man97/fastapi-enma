"""change email to string

Revision ID: f8ceab6d9859
Revises: cf55581733cd
Create Date: 2026-08-26 12:19:47.114761

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f8ceab6d9859'
down_revision: Union[str, Sequence[str], None] = 'cf55581733cd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        "users",
        "email",
        existing_type=sa.Integer(),
        type_=sa.String(),
        existing_nullable=False
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'email')
