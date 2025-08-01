from http import HTTPStatus

from pydantic import BaseModel


class HealthCheck(BaseModel):
    status: int = HTTPStatus.OK
