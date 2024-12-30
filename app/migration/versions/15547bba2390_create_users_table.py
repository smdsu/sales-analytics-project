"""create users table

Revision ID: 15547bba2390
Revises: fbe885161656
Create Date: 2024-12-28 21:33:30.366736

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '15547bba2390'
down_revision: Union[str, None] = 'fbe885161656'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
