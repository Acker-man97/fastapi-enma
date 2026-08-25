"""Create posts table

Revision ID: 2bcd75b47a1c
Revises: 
Create Date: 2026-08-24 18:37:39.405048

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2bcd75b47a1c'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('posts', sa.Column("id",sa.Integer,nullable=False,primary_key=True,autoincrement=True),sa.Column("title",sa.String,nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('posts')
    pass
