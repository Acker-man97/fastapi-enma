"""create foreign key

Revision ID: 2b3de6e5b8eb
Revises: 00324fd809b8
Create Date: 2026-08-24 21:33:16.890262

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2b3de6e5b8eb'
down_revision: Union[str, Sequence[str], None] = '00324fd809b8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('owner_id', sa.Integer, nullable=False))
    op.create_foreign_key('posts_users_fk', source_table='posts', referent_table='users',local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name='posts',type_='foreignkey')
    op.drop_column('posts', 'owner_id')
    pass
