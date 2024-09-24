"""add user table

Revision ID: d1e07c1cc232
Revises: 52c889a302bf
Create Date: 2024-09-24 16:19:37.037673

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd1e07c1cc232'
down_revision: Union[str, None] = '52c889a302bf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id',sa.Integer,nullable=False),
                    sa.Column('email',sa.String,nullable=False),
                    sa.Column('password',sa.String,nullable=False),
                    sa.Column('created_at',sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'),nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'))
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
