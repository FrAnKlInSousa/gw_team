from enum import Enum
from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from gw_team.models.registry import table_registry


@table_registry.mapped_as_dataclass
class Modality:
    __tablename__ = 'modalities'
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]
    users_assoc: Mapped[List['UserModality']] = relationship(
        back_populates='modality', cascade='all, delete-orphan'
    )
