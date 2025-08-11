"""alterando nome da modalidade jiu_jitsu para jiu-jitsu

Revision ID: d103af87e544
Revises: a8b842953843
Create Date: 2025-08-11 13:15:58.054749

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import MetaData

# revision identifiers, used by Alembic.
revision: str = 'd103af87e544'
down_revision: Union[str, Sequence[str], None] = 'a8b842953843'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    modalities = sa.Table(
        'modalities',
        MetaData(),
        sa.Column('name', sa.String),
    )
    op.execute(
        modalities.update()
        .where('jiu_jitsu' == modalities.c.name)
        .values(name='jiu-jitsu')
    )


def downgrade() -> None:
    """Downgrade schema."""
    modalities = sa.Table(
        'modalities',
        MetaData(),
        sa.Column('name', sa.String),
    )

    op.execute(
        modalities.update()
        .where('jiu-jitsu' == modalities.c.name)
        .values(name='jiu_jitsu')
    )