from http import HTTPStatus

from fastapi.exceptions import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from gw_team.models.models import User, UserModality
from gw_team.schemas.users import UserCreate


async def find_user_by_email(email: str, session: AsyncSession) -> User | None:
    user_db = await session.scalar(select(User).where(User.email == email))
    return user_db or None


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
