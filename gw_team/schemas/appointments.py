from datetime import date
from typing import List

from pydantic import BaseModel, ConfigDict


class AppointmentSchema(BaseModel):
    date: date
    modality_id: int


class AppointmentPublic(BaseModel):
    date: date
    modality_name: str
    period: str
    id: int

    model_config = ConfigDict(from_attributes=True)


class AppointmentList(BaseModel):
    appointments: List[AppointmentPublic]
