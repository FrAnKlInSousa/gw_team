"""populando tabela modalities

Revision ID: a8b842953843
Revises: af740ece1b01
Create Date: 2025-08-06 17:17:47.806373

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a8b842953843'
down_revision: Union[str, Sequence[str], None] = 'af740ece1b01'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

table_name = sa.Table(
    'modalities',
    sa.MetaData(),
    sa.Column('name', sa.String(), primary_key=False),
    sa.Column('id', sa.Integer(), primary_key=True)
)

def upgrade() -> None:
    """Upgrade schema."""
    op.bulk_insert(
        table_name,
        [{'name': 'jiu_jitsu'}, {'name': 'capoeira'}]
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        "DELETE FROM modalities WHERE name IN ('jiu_jitsu', 'capoeira')"
    )
