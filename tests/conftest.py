import factory
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from gw_team.app import app
from gw_team.database import db_session
from gw_team.models.users import User, table_registry
from gw_team.security import hash_password
from gw_team.settings import Settings


class UserFactory(factory.Factory):
    class Meta:
        model = User

    name = factory.Sequence(lambda n: f'test{n}')
    last_name = factory.Sequence(lambda n: f'last_name{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.name}@tst.com')
    password = factory.LazyAttribute(lambda obj: f'{obj.name}#secret')


@pytest.fixture(scope='session')
def engine():
    return create_engine(Settings().DATABASE_URL)


@pytest.fixture
def session(engine):
    table_registry.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    table_registry.metadata.drop_all(engine)


@pytest.fixture
def user(session):
    pwd = 'secret'
    user = UserFactory(password=hash_password(pwd))
    session.add(user)
    session.commit()
    session.refresh(user)
    user.clean_password = pwd
    return user


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[db_session] = get_session_override
        yield client
    app.dependency_overrides.clear()
