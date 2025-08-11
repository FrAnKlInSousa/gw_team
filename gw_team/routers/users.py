from datetime import datetime
from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from gw_team.database import db_session
from gw_team.models import Modality
from gw_team.models.user_modalities import (
    UserModality,
)
from gw_team.models.users import User
from gw_team.schemas.filters import FilterUser
from gw_team.schemas.schemas import Message
from gw_team.schemas.users import (
    UpdatePassword,
    UpdateUser,
    UserList,
    UserPublic,
    UserSchema,
)
from gw_team.security import current_user, hash_password

router = APIRouter(prefix='/users', tags=['usuários'])

T_Session = Annotated[AsyncSession, Depends(db_session)]
T_Filter = Annotated[FilterUser, Query()]
T_CurrentUser = Annotated[User, Depends(current_user)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
async def create_user(user: UserSchema, session: T_Session):
    user_db = await session.scalar(
        select(User).where(User.email == user.email)
    )
    if user_db:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='email já existe.'
        )

    modalities_obj = await session.scalars(
        select(Modality).where(Modality.name.in_(user.modalities))
    )

    modalities = modalities_obj.all()

    user_db = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password),
        last_name=user.last_name,
        user_type=user.user_type,
    )
    for modality in modalities:
        assoc = UserModality(
            user=user_db,
            modality=modality,
            start_date=datetime.now(),
        )
        user_db.modalities_assoc.append(assoc)

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

    return UserPublic.model_validate(user_db)


@router.get('/{user_id}', response_model=UserPublic)
async def read_user(user_id: int, session: T_Session, user: T_CurrentUser):
    if user.id != user_id and user.user_type != 'admin':
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='You have no permission'
        )
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
    return UserPublic.model_validate(user_db)


@router.get('/', status_code=HTTPStatus.OK, response_model=UserList)
async def read_users(
    session: T_Session, filter_users: T_Filter, user: T_CurrentUser
):
    if user.user_type != 'admin':
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='You have no permission'
        )
    query = select(User).options(
        selectinload(User.modalities_assoc).selectinload(UserModality.modality)
    )
    if filter_users.name:
        query = query.filter(User.name.contains(filter_users.name))
    result = await session.scalars(
        query.limit(filter_users.limit).offset(filter_users.page)
    )
    users = result.all()
    return UserList(users=[UserPublic.model_validate(user) for user in users])


@router.patch('/{user_id}', response_model=UserPublic)
async def update(
    user_id: int,
    auth_user: T_CurrentUser,
    session: T_Session,
    data: UpdateUser,
):
    # todo permite mudar email? apenas admin? melhor nao.. pensar sobre
    if auth_user.user_type != 'admin' and user_id != auth_user.id:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='You have no permission',
        )
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
    return UserPublic.model_validate(user_db)


@router.patch('/password/{user_id}', response_model=Message)
async def update_password(
    user_id: int,
    auth_user: T_CurrentUser,
    session: T_Session,
    data: UpdatePassword,
):
    if auth_user.user_type != 'admin' and user_id != auth_user.id:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='You have no permission',
        )

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

    user_db.password = hash_password(data.new_password)

    session.add(user_db)
    await session.commit()

    return Message(message='Password changed successfully')


@router.delete('/{user_id}', response_model=Message)
async def delete_user(user_id: int, user: T_CurrentUser, session: T_Session):
    if user.id != user_id and user.user_type != 'admin':
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='You have no permission',
        )
    user_db = await session.scalar(select(User).where(User.id == user_id))
    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )
    user_db.disabled = True
    session.add(user_db)
    await session.commit()
    return Message(message='User successfully deleted')
