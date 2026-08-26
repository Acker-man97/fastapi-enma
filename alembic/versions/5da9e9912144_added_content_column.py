"""added content  column 

Revision ID: 5da9e9912144
Revises: f8ceab6d9859
Create Date: 2026-08-26 12:29:13.094393

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5da9e9912144'
down_revision: Union[str, Sequence[str], None] = 'f8ceab6d9859'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(
        "posts",
        sa.Column("content", sa.String(), nullable=True)
    )



def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts", "content")
