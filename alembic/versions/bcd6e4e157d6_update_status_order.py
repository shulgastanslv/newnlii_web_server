"""Update Status Order

Revision ID: bcd6e4e157d6
Revises: 416ca8ebf5ae
Create Date: 2026-01-14 02:42:42.921314

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'bcd6e4e157d6'
down_revision: Union[str, Sequence[str], None] = '416ca8ebf5ae'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        ALTER TABLE orders
        ALTER COLUMN status
        TYPE order_status_enum
        USING status::text::order_status_enum;
    """)
    op.execute("DROP TYPE IF EXISTS status_enum;")


def downgrade() -> None:
  pass