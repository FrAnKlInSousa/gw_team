"""adicionando coluna user_type

Revision ID: 365621fbeace
Revises: abbb8b2c4d98
Create Date: 2025-08-04 15:11:31.938121

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '365621fbeace'
down_revision: Union[str, Sequence[str], None] = 'abbb8b2c4d98'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("CREATE TYPE usertype AS ENUM ('admin', 'client')")

    op.add_column('users', sa.Column('user_type', sa.Enum('admin', 'client', name='usertype'), nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'user_type')
    op.execute("DROP TYPE usertype")
