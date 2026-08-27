"""renamed comments owner_id to user_id

Revision ID: abe61f13c82a
Revises: 5da9e9912144
Create Date: 2026-08-27 19:48:13.337255

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'abe61f13c82a'
down_revision: Union[str, Sequence[str], None] = '5da9e9912144'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column('comments', 'owner_id', new_column_name='user_id')


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('comments', 'user_id', new_column_name='owner_id')
