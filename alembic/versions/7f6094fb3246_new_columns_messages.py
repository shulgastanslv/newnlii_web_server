"""New columns messages

Revision ID: 7f6094fb3246
Revises: 5c37b50d462b
Create Date: 2026-01-05 11:10:16.421027

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7f6094fb3246'
down_revision: Union[str, Sequence[str], None] = '5c37b50d462b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
