"""create user - saved posts

Revision ID: 78e8f3e427c7
Revises: bc265c72afe7
Create Date: 2026-02-28 16:46:10.168514

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '78e8f3e427c7'
down_revision: Union[str, Sequence[str], None] = 'bc265c72afe7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
