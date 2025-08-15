from dataclasses import asdict

import pytest
from sqlalchemy import select
from sqlalchemy.exc import DataError, PendingRollbackError

from gw_team.models.models import User


@pytest.mark.asyncio
async def test_create_user(mock_db_time, session):
    with mock_db_time(model=User) as time:
        new_user = User(
            name='test_name',
            last_name='test_last_name',
            user_type='client',
            password='secret',
            email='test@test.com',
            disabled=False,
        )
        session.add(new_user)
        await session.commit()
        user_db = await session.scalar(
            select(User).where(User.name == 'test_name')
        )
        assert asdict(user_db) == {
            'id': 1,
            'name': 'test_name',
            'last_name': 'test_last_name',
            'user_type': 'client',
            'password': 'secret',
            'email': 'test@test.com',
            'created_at': time,
            'updated_at': time,
            'disabled': False,
            'modalities_assoc': [],
        }


@pytest.mark.asyncio
async def test_create_invalid_user(session):
    invalid_user = User(
        name='test_name',
        last_name='test_last_name',
        user_type='invalid',
        password='secret',
        email='test@test.com',
        disabled=False,
    )
    session.add(invalid_user)
    with pytest.raises(DataError):
        await session.commit()

    with pytest.raises(PendingRollbackError):
        await session.scalar(select(User))
