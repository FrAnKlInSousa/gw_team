from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from gw_team.models import table_registry
from gw_team.models.modalities import Modality
from gw_team.models.users import User


@table_registry.mapped_as_dataclass
class UserModality:
    __tablename__ = 'user_modalities'

    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'), primary_key=True
    )
    modality_id: Mapped[int] = mapped_column(
        ForeignKey('modalities.id', ondelete='CASCADE'), primary_key=True
    )
    start_date: Mapped[datetime]
    user: Mapped['User'] = relationship(back_populates='modalities_assoc')
    modality: Mapped['Modality'] = relationship(back_populates='users_assoc')
