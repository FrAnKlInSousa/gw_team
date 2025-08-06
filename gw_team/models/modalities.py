from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from gw_team.models.registry import table_registry


@table_registry.mapped_as_dataclass
class Modality:
    __tablename__ = 'modalities'
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    users_assoc: Mapped[List['UserModality']] = relationship(  # noqa: F821
        back_populates='modality',
        cascade='all, delete-orphan',
        default_factory=list,
    )
