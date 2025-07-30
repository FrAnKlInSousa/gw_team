from http import HTTPStatus

from fastapi import FastAPI

from gw_team.schemas.health_check import HealthCheck
from gw_team.routers import users

app = FastAPI(title='GW Team')

app.include_router(users.router)


@app.get('/', response_model=HealthCheck, tags=['health'])
def health_check():
    return {'status': HTTPStatus.OK}
