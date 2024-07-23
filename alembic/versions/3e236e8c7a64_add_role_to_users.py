"""Add role to users

Revision ID: 3e236e8c7a64
Revises: 
Create Date: 2024-07-23 10:10:25.083426

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3e236e8c7a64'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('role', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'role')
