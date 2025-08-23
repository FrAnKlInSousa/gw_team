from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from gw_team.database.engine import db_session
from gw_team.models.models import User
from gw_team.schemas.appointments import AppointmentSchema
from gw_team.security.security import current_user

router = APIRouter()

T_CurrentUser = Annotated[User, Depends(current_user)]
T_Session = Annotated[AsyncSession, Depends(db_session)]


@router.post('/')
async def create_schedule(
    user: T_CurrentUser, session: T_Session, data: AppointmentSchema
):
    print(data)
