"""Change customers and sales

Revision ID: 0567d5cc6b9f
Revises: c237f24b7274
Create Date: 2024-12-25 16:32:10.424142

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0567d5cc6b9f'
down_revision: Union[str, None] = 'c237f24b7274'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
