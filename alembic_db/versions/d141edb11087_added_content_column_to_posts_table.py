"""added content column to posts table

Revision ID: d141edb11087
Revises: cc99b71f9377
Create Date: 2026-03-05 16:03:12.844660

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd141edb11087'
down_revision: Union[str, Sequence[str], None] = 'cc99b71f9377'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'posts',
        sa.Column('content', sa.String(), nullable=False)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content')
