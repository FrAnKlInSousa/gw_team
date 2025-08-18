from http import HTTPStatus

from fastapi.exceptions import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from gw_team.models.models import User, UserModality
from gw_team.schemas.filters import FilterUser
from gw_team.schemas.users import UserCreate
from gw_team.security.token import hash_password


async def find_user_by_email(email: str, session: AsyncSession) -> User | None:
    user_db = await session.scalar(select(User).where(User.email == email))
    return user_db or None


async def update_password(user_id: int, session: AsyncSession, new_pass: str):
    user_db = await find_user_by_id(user_id, session)
    user_db.password = hash_password(new_pass)

    session.add(user_db)
    await session.commit()


async def delete_user(user_id: int, session: AsyncSession):
    user_db = await find_user_by_id(user_id, session)
    user_db.disabled = True
    session.add(user_db)
    await session.commit()


async def find_user_by_id(user_id: int, session: AsyncSession) -> User | None:
    user_db = await session.scalar(
        select(User)
        .where(User.id == user_id)
        .options(
            selectinload(User.modalities_assoc).selectinload(
                UserModality.modality
            )
        )
    )
    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )
    return user_db


async def find_users(filter_users: FilterUser, session):
    query = select(User).options(
        selectinload(User.modalities_assoc).selectinload(UserModality.modality)
    )
    if filter_users.name:
        query = query.filter(User.name.contains(filter_users.name))
    result = await session.scalars(
        query.limit(filter_users.limit).offset(filter_users.page)
    )
    return result.all()


async def update(user_id: int, data, session) -> User:
    user_db = await find_user_by_id(user_id, session)

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user_db, key, value)

    session.add(user_db)
    await session.commit()
    await session.refresh(user_db)
    user_db = await session.scalar(
        select(User)
        .where(User.id == user_id)
        .options(
            selectinload(User.modalities_assoc).selectinload(
                UserModality.modality
            )
        )
    )
    return user_db


async def create(user: UserCreate, session: AsyncSession) -> User:
    user_db = await find_user_by_email(str(user.email), session)
    if user_db:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='email já existe.'
        )

    user_db = await User.from_schema(user, session)

    session.add(user_db)
    await session.commit()
    await session.refresh(user_db)
    await session.execute(
        select(User)
        .where(User.id == user_db.id)
        .options(
            selectinload(User.modalities_assoc).selectinload(
                UserModality.modality
            )
        )
    )
    return user_db
