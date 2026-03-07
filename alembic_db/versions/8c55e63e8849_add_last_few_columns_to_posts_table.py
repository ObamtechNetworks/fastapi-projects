"""add last few columns to posts table

Revision ID: 8c55e63e8849
Revises: 156145170607
Create Date: 2026-03-07 13:41:56.549305

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8c55e63e8849'
down_revision: Union[str, Sequence[str], None] = '156145170607'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('published', sa.Boolean(),
                                     nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.DateTime(timezone=True),
                                     server_default=sa.func.now(), nullable=False))
    op.add_column('posts', sa.Column('updated_at', sa.DateTime(timezone=True),
                                     server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    op.drop_column('posts', 'updated_at')
