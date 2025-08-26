from contextlib import contextmanager
from datetime import date, datetime

import factory.fuzzy
import pytest
import pytest_asyncio
from sqlalchemy import event, select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from starlette.testclient import TestClient
from testcontainers.postgres import PostgresContainer

from gw_team.app import app
from gw_team.database.engine import db_session
from gw_team.models.models import (
    Appointment,
    Modality,
    User,
    UserType,
    table_registry,
)
from gw_team.security.token import hash_password
from gw_team.settings import Settings


@pytest.fixture
def client(session, add_modalities_to_db):
    def get_session_override():
        return session

    app.dependency_overrides[db_session] = get_session_override

    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture(scope='session')
def engine():
    with PostgresContainer('postgres:17', driver='psycopg') as postgres:
        yield create_async_engine(postgres.get_connection_url())


@pytest_asyncio.fixture
async def session(engine):
    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.create_all)

    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.drop_all)


@contextmanager
def _mock_db_time(*, model, time=datetime(2025, 5, 20)):
    def fake_time_hook(mapper, connection, target):
        if hasattr(target, 'created_at'):
            target.created_at = time
        if hasattr(target, 'updated_at'):
            target.updated_at = time

    event.listen(model, 'before_insert', fake_time_hook)
    yield time
    event.remove(model, 'before_insert', fake_time_hook)


@pytest.fixture
def mock_db_time():
    return _mock_db_time


@pytest_asyncio.fixture
async def user(session: AsyncSession) -> User:
    password = 'secret'
    new_user = UserFactory(password=hash_password(password))
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    new_user.clean_password = password
    return new_user


@pytest_asyncio.fixture
async def other_user(session: AsyncSession) -> User:
    password = 'secret'
    new_user = UserFactory(password=hash_password(password))
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    new_user.clean_password = password
    return new_user


@pytest_asyncio.fixture
async def custom_user(session: AsyncSession):
    async def create_user(**kwargs) -> User:
        new_user = UserFactory(**kwargs)
        password = new_user.password
        new_user.password = hash_password(password)
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        new_user.clean_password = password
        return new_user

    return create_user


@pytest_asyncio.fixture
async def user_admin(session: AsyncSession) -> User:
    password = 'secret'
    new_user = UserFactory(
        password=hash_password(password), user_type=UserType.admin
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    new_user.clean_password = password
    return new_user


@pytest.fixture
def token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    return response.json()['access_token']


@pytest.fixture
def header_client(token):
    return {'Authorization': f'Bearer {token}'}


@pytest.fixture
def header_admin(token_admin):
    return {'Authorization': f'Bearer {token_admin}'}


@pytest.fixture
def token_admin(client, user_admin):
    response = client.post(
        '/auth/token',
        data={
            'username': user_admin.email,
            'password': user_admin.clean_password,
        },
    )
    return response.json()['access_token']


@pytest.fixture
def settings():
    return Settings()


class UserFactory(factory.Factory):
    class Meta:
        model = User

    name = factory.Sequence(lambda n: f'test{n}')
    last_name = factory.Sequence(lambda n: f'last_name{n}')
    email = factory.LazyAttribute(
        lambda obj: f'{obj.name}{obj.last_name}@test.com'
    )
    password = factory.LazyAttribute(lambda obj: f'{obj.name}#secret')
    user_type = UserType.client


@pytest_asyncio.fixture
async def add_modalities_to_db(session: AsyncSession):
    session.add_all([
        Modality(modality_name='capoeira', period='diurno'),
        Modality(modality_name='jiu-jitsu'),
        Modality(modality_name='muay-thai', period='diurno'),
    ])
    await session.commit()
    result = await session.scalars(select(Modality))
    return result.all()


class AppointmentFactory(factory.Factory):
    class Meta:
        model = Appointment

    date = factory.LazyFunction(date.today)
    modality_id = 0
    user_id = 0


@pytest_asyncio.fixture
async def create_appointment(session: AsyncSession, user):
    modalities_obj = await session.scalars(select(Modality))
    modality = modalities_obj.first()
    appointment = AppointmentFactory(modality_id=modality.id, user_id=user.id)
    session.add(appointment)
    await session.commit()
