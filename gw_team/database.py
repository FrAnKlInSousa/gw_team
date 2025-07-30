from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from gw_team.settings import Settings

engine = create_engine(Settings().DATABASE_URL)


def db_session():  # pragma: no cover
    with Session(engine, expire_on_commit=False) as session:
        yield session
