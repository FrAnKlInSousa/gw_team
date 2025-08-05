from sqlalchemy import Table, Column, ForeignKey, Integer
from gw_team.models import table_registry


user_modalities = Table(
    'user_modalities',
    table_registry.metadata,
    Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
    Column('modality_id', ForeignKey('modalities.id', ondelete='CASCADE'), primary_key=True)
)