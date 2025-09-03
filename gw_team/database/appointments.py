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
    statement = (
        select(
            Appointment.date,
            Modality.modality_name,
            Modality.period,
            Appointment.id,
        )
        .join(Modality, Appointment.modality_id == Modality.id)
        .where(
            Appointment.user_id == user.id, Appointment.date >= date.today()
        )
        .order_by(Appointment.date.asc())
    )

    results = await session.execute(statement)
    appointments = results.all()

    return [
        AppointmentPublic.model_validate(appointment)
        for appointment in appointments
    ]


async def cancel_appointment(appointment_id: int, session: AsyncSession):
    appointment = await session.scalar(
        select(Appointment).where(Appointment.id == appointment_id)
    )

    if not appointment:
        raise HTTPException(status_code=404, detail='Appointment not found')

    await session.delete(appointment)
    await session.commit()
