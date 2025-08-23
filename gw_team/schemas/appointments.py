from datetime import date

from pydantic import BaseModel


class AppointmentSchema(BaseModel):
    date: date
    modality_id: int


class AppointmentPublic(BaseModel):
    date: date
    modality_id: int
    user_id: int

    class Config:
        from_attributes = True
