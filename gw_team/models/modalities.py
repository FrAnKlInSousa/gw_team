from enum import Enum

from sqlalchemy.orm import Mapped, mapped_column, relationship
from gw_team.models import table_registry


class FightStyle(str, Enum):
    jiu_jitsu='jiu-jitsu'
    capoeira='capoeira'


@table_registry.mapped_as_dataclass
class Modality:
    __tablename__ = 'modalities'
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[FightStyle]
    users_assoc = Mapped[list['UserModality']] = relationship(
        back_populates='modality',
        cascade='all, delete-orphan'
    )