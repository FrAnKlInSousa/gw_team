from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from gw_team.database import appointments
from gw_team.database.engine import db_session
from gw_team.models.models import User
from gw_team.schemas.appointments import AppointmentList, AppointmentSchema
from gw_team.schemas.schemas import Message
from gw_team.security.security import current_user

router = APIRouter(prefix='/appointments', tags=['appointments'])

T_CurrentUser = Annotated[User, Depends(current_user)]
T_Session = Annotated[AsyncSession, Depends(db_session)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=Message)
async def create_schedule(
    user: T_CurrentUser, session: T_Session, data: AppointmentSchema
):
    await appointments.create(data, user.id, session)
    return Message(message='Appointment created successfully')


@router.get('/', response_model=AppointmentList)
async def list_appointments(user: T_CurrentUser, session: T_Session):
    my_appointments = await appointments.list_appointments(
        session=session, user=user
    )
    return {'appointments': my_appointments}


@router.delete('/{appointment_id}', response_model=Message)
async def delete_schedule(appointment_id: int, session: T_Session):
    await appointments.cancel_appointment(appointment_id, session)
    return Message(message='Appointment deleted successfully')
