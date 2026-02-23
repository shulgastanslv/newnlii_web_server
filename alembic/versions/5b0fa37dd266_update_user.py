"""Update User

Revision ID: 5b0fa37dd266
Revises: 674d65e4ca3b
Create Date: 2026-01-13 22:38:00.800611

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '5b0fa37dd266'
down_revision: Union[str, Sequence[str], None] = '674d65e4ca3b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users', sa.Column('isStared', sa.Boolean(), nullable=False, server_default=sa.text('false')))
    op.add_column('users', sa.Column('isArchived', sa.Boolean(), nullable=False, server_default=sa.text('false')))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'isArchived')
    op.drop_column('users', 'isStared')
    # ### end Alembic commands ###
