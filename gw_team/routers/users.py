from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from gw_team.database import db_session
from gw_team.models.users import User
from gw_team.schemas.filters import FilterUser
from gw_team.schemas.users import UserList, UserPublic, UserSchema
from gw_team.security import hash_password

router = APIRouter(prefix='/users', tags=['usuarios'])

T_Session = Annotated[AsyncSession, Depends(db_session)]
T_Filter = Annotated[FilterUser, Query()]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
async def create_user(user: UserSchema, session: T_Session):
    user_db = await session.scalar(
        select(User).where(User.email == user.email)
    )
    if user_db:
        if user_db.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail='email já existe.'
            )
    db_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password),
        last_name=user.last_name,
    )
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user


@router.get('/{user_id}', response_model=UserPublic)
async def read_user(user_id: int, session: T_Session):
    user_db = await session.scalar(select(User).where(User.id == user_id))
    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )
    return user_db


@router.get('/', status_code=HTTPStatus.OK, response_model=UserList)
async def read_users(
    session: T_Session,
    filter_users: T_Filter,
):
    query = select(User)
    if filter_users.name:
        query = query.filter(User.name.contains(filter_users.name))
    users = await session.scalars(
        query.limit(filter_users.limit).offset(filter_users.page)
    )
    return {'users': users.all()}

