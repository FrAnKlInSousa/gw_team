from datetime import datetime
from enum import Enum
from typing import List

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from gw_team.models.registry import table_registry


class UserType(str, Enum):
    admin = 'admin'
    client = 'client'


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, onupdate=func.now(), server_default=func.now()
    )
    name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    last_name: Mapped[str]
    password: Mapped[str]
    user_type: Mapped[UserType]
    modalities_assoc: Mapped[List['UserModality']] = relationship(  # noqa: F821
        back_populates='user',
        cascade='all, delete-orphan',
        default_factory=list,
    )
    disabled: Mapped[bool] = mapped_column(default=False)

    @property
    def modalities(self):
        return [modality.name for modality in self.modalities_assoc]
