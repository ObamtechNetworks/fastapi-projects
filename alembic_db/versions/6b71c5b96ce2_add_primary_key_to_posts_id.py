"""add primary key to posts.id

Revision ID: 6b71c5b96ce2
Revises: c77119879417
Create Date: 2026-03-07 13:58:54.419508

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6b71c5b96ce2'
down_revision: Union[str, Sequence[str], None] = '8c55e63e8849'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_primary_key('posts_pkey', 'posts', ['id'])



def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('posts_pkey', 'posts', type_='primary')
