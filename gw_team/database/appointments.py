from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from gw_team.models.models import Appointment, Modality
from gw_team.schemas.appointments import AppointmentSchema


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
