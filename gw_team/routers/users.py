from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from gw_team.database import users
from gw_team.database.engine import db_session
from gw_team.database.users import find_users
from gw_team.models.models import User
from gw_team.permissions import check_admin_permission, check_permission
from gw_team.schemas.filters import FilterUser
from gw_team.schemas.schemas import Message
from gw_team.schemas.users import (
    UpdatePassword,
    UpdateUser,
    UserCreate,
    UserList,
    UserPublic,
)
from gw_team.security.security import current_user

router = APIRouter(prefix='/users', tags=['usuários'])

T_Session = Annotated[AsyncSession, Depends(db_session)]
T_Filter = Annotated[FilterUser, Query()]
T_CurrentUser = Annotated[User, Depends(current_user)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
async def create_user(user: UserCreate, session: T_Session):
    user_db = await users.create(user, session)
    return UserPublic.model_validate(user_db)


@router.get('/{user_id}', response_model=UserPublic)
async def read_user(user_id: int, session: T_Session, user: T_CurrentUser):
    await check_permission(user, user_id)
    user_db = await users.find_user_by_id(user_id, session)

    return UserPublic.model_validate(user_db)


@router.get('/', status_code=HTTPStatus.OK, response_model=UserList)
async def read_users(
    session: T_Session, filter_users: T_Filter, user: T_CurrentUser
):
    await check_admin_permission(user)
    users_list = await find_users(filter_users, session)

    return UserList(
        users=[UserPublic.model_validate(user) for user in users_list]
    )


@router.patch('/{user_id}', response_model=UserPublic)
async def update(
    user_id: int,
    auth_user: T_CurrentUser,
    session: T_Session,
    data: UpdateUser,
):
    # todo permite mudar email? apenas admin? melhor nao.. pensar sobre
    await check_permission(auth_user, user_id)
    user_db = await users.update(user_id, data, session)

    return UserPublic.model_validate(user_db)


@router.patch('/password/{user_id}', response_model=Message)
async def update_password(
    user_id: int,
    auth_user: T_CurrentUser,
    session: T_Session,
    data: UpdatePassword,
):
    await check_permission(auth_user, user_id)
    await users.update_password(user_id, session, data.new_password)

    return Message(message='Password changed successfully')


@router.delete('/{user_id}', response_model=Message)
async def delete_user(user_id: int, user: T_CurrentUser, session: T_Session):
    await check_permission(user, user_id)
    await users.delete_user(user_id, session)

    return Message(message='User successfully deleted')
