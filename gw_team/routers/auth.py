from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from gw_team.database import db_session
from gw_team.models.models import User
from gw_team.schemas.auth import Token
from gw_team.security import create_token, is_valid_password

router = APIRouter(prefix='/auth', tags=['auth'])
T_Session = Annotated[AsyncSession, Depends(db_session)]
OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post('/token', status_code=HTTPStatus.OK, response_model=Token)
async def authenticate(
    form_data: OAuth2Form,
    session: T_Session,
):
    user_db = await session.scalar(
        select(User).where(User.email == form_data.username)
    )

    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Invalid email or password',
        )
    if user_db.disabled:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='User account is not active',
        )
    valid_password = is_valid_password(
        password=form_data.password, hashed_password=user_db.password
    )
    if not valid_password:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Invalid email or password',
        )

    token = create_token({'sub': user_db.email})
    return {'access_token': token, 'token_type': 'Bearer'}
