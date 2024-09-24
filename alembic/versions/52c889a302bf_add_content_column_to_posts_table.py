"""add content column to posts table

Revision ID: 52c889a302bf
Revises: 1e16847b3e28
Create Date: 2024-09-24 16:16:02.302781

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '52c889a302bf'
down_revision: Union[str, None] = '1e16847b3e28'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String,nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
