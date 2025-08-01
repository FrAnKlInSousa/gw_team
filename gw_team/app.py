from http import HTTPStatus

from fastapi import FastAPI

from gw_team.routers import auth, users
from gw_team.schemas.health_check import HealthCheck

app = FastAPI(title='GW Team')

app.include_router(users.router)
app.include_router(auth.router)


@app.get('/', response_model=HealthCheck, tags=['health'])
async def health_check():
    return {'status': HTTPStatus.OK}
