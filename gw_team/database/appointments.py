from datetime import date
from typing import List

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from gw_team.models.models import Appointment, Modality, User
from gw_team.schemas.appointments import (
    AppointmentPublic,
    AppointmentSchema,
)


async def create(
    appointment: AppointmentSchema, user_id: int, session: AsyncSession
):
    stmt = select(Modality).where(Modality.id == appointment.modality_id)
    result = await session.execute(stmt)
    modality = result.scalar_one_or_none()

    if not modality:
        raise HTTPException(status_code=404, detail='Modality not found')
    my_appointment = Appointment(
        date=appointment.date,
        user_id=user_id,
        modality_id=appointment.modality_id,
    )
    session.add(my_appointment)
    await session.commit()


async def list_appointments(
    session: AsyncSession, user: User
) -> List[AppointmentPublic]:
    statement = select(Appointment).where(
        Appointment.user_id == user.id, Appointment.date >= date.today()
    )
    appointments_obj = await session.scalars(statement)
    my_appointments = appointments_obj.all()
    result = [
        AppointmentPublic.model_validate(appointment)
        for appointment in my_appointments
    ]
    return result
