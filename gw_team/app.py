from http import HTTPStatus

from fastapi import FastAPI
from gw_team.schemas.health_check import HealthCheck


app = FastAPI(title='GW Team')

@app.get('/', response_model=HealthCheck, tags=['health'])
def health_check():
    return {'status': HTTPStatus.OK}
