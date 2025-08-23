from datetime import date, datetime
from typing import List

from sqlalchemy import Date, ForeignKey, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

from gw_team.enums import UserType
from gw_team.schemas.users import UserCreate
from gw_team.security.token import hash_password

table_registry = registry()


@table_registry.mapped_as_dataclass
class Modality:
    __tablename__ = 'modalities'
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    modality_name: Mapped[str]
    period: Mapped[str] = mapped_column(default='noturno')
    users_assoc: Mapped[List['UserModality']] = relationship(  # noqa: F821
        back_populates='modality',
        cascade='all, delete-orphan',
        default_factory=list,
    )
    appointments: Mapped[List['Appointment']] = relationship(
        back_populates='modality',
        cascade='all, delete-orphan',
        default_factory=list,
    )


@table_registry.mapped_as_dataclass
class UserModality:
    __tablename__ = 'user_modalities'

    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'),
        init=False,
        primary_key=True,
    )
    modality_id: Mapped[int] = mapped_column(
        ForeignKey('modalities.id', ondelete='CASCADE'),
        init=False,
        primary_key=True,
    )

    start_date: Mapped[datetime]
    user: Mapped['User'] = relationship(back_populates='modalities_assoc')  # noqa: F821
    modality: Mapped['Modality'] = relationship(back_populates='users_assoc')  # noqa: F821


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
    appointments: Mapped[List['Appointment']] = relationship(
        back_populates='user',
        cascade='all, delete-orphan',
        default_factory=list,
    )
    disabled: Mapped[bool] = mapped_column(default=False)

    @property
    def modalities(self) -> list[str]:
        return [
            assoc.modality.modality_name for assoc in self.modalities_assoc
        ]

    @classmethod
    async def from_schema(
        cls, user_schema: UserCreate, session: AsyncSession
    ) -> 'User':
        modalities_obj = await session.scalars(
            select(Modality).where(
                Modality.modality_name.in_(user_schema.modalities)
            )
        )
        modalities = modalities_obj.all()

        user = cls(
            name=user_schema.name,
            email=str(user_schema.email),
            password=hash_password(user_schema.password),
            last_name=user_schema.last_name,
            user_type=user_schema.user_type,
            modalities_assoc=[],
        )
        now = datetime.now()
        user.modalities_assoc.extend([
            UserModality(modality=modality, user=user, start_date=now)
            for modality in modalities
        ])

        return user

    @property
    def is_admin(self) -> bool:
        return self.user_type.value == 'admin'


@table_registry.mapped_as_dataclass
class Appointment:
    __tablename__ = 'appointments'

    date: Mapped[date] = mapped_column(Date())
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    modality_id: Mapped[int] = mapped_column(ForeignKey('modalities.id'))

    user: Mapped['User'] = relationship(
        back_populates='appointments', lazy='raise', init=False
    )
    modality: Mapped['Modality'] = relationship(
        back_populates='appointments', lazy='raise', init=False
    )

    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
