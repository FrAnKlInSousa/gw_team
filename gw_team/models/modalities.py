from pydantic import BaseModel
from enum import Enum

from sqlalchemy.orm import Mapped, mapped_column, relationship


class Fight(str, Enum):
    jiu_jitsu='jiu-jitsu'
    capoeira='capoeira'

class Modalidades(BaseModel):
    luta: Mapped[Fight]
    int: Mapped[int] = mapped_column(primary_key=True)
    client: Mapped[int] = relationship(init=False,
        cascade='all, delete-orphan', lazy='selectin')