from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from gw_team.database import db_session
from sqlalchemy.orm import Session
from gw_team.security import hash_password
from gw_team.models.users import User
from gw_team.schemas.users import UserSchema, UserPublic
from typing import Annotated

router = APIRouter(prefix='/users', tags=['usuarios'])

T_Session = Annotated[Session, Depends(db_session)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create(user: UserSchema, session: T_Session):
    user_db = session.scalar(select(User).where(User.email == user.email))
    if user_db:
        ...
    user = User(
        name=user.name,
        last_name=user.last_name,
        email=user.email,
        password=hash_password(user.password),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.get('/{user_id}', response_model=UserPublic)
def read_user(user_id: int, session: T_Session):
    user_db = session.scalar(select(User).where(User.id == user_id))
    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )
    return user_db
