"""add last few columns to posts table 

Revision ID: a94ba7afabd0
Revises: c24a747de398
Create Date: 2024-09-24 17:00:06.815101

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a94ba7afabd0'
down_revision: Union[str, None] = 'c24a747de398'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column(
        'published',sa.Boolean,nullable=False,server_default='TRUE'),)
    op.add_column('posts',sa.Column(
        'created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('now()')
    ))
    pass


def downgrade() -> None:
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
    pass
