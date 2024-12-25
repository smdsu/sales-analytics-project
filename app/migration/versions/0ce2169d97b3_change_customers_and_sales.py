"""Change customers and sales

Revision ID: 0ce2169d97b3
Revises: 0567d5cc6b9f
Create Date: 2024-12-25 16:35:15.218616

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0ce2169d97b3'
down_revision: Union[str, None] = '0567d5cc6b9f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
