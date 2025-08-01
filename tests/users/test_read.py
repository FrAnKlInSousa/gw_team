from http import HTTPStatus

import pytest

from gw_team.schemas.users import UserList, UserPublic
from tests.conftest import UserFactory


def test_read_user(client, user, token):
    response = client.get(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'name': user.name,
        'last_name': user.last_name,
        'id': user.id,
        'email': user.email,
        'user_type': user.user_type,
    }


def test_read_user_not_found(client, token_admin):
    response = client.get(
        '/users/0', headers={'Authorization': f'Bearer {token_admin}'}
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_read_users(client, user_admin, token_admin):
    response = client.get(
        '/users/', headers={'Authorization': f'Bearer {token_admin}'}
    )
    assert response.status_code == HTTPStatus.OK
    expected = UserList(users=[UserPublic.model_validate(user_admin)])
    assert response.json() == expected.model_dump()


@pytest.mark.asyncio
async def test_filter_users_should_return_3(client, session, token_admin):
    expected_len = 3
    session.add_all(UserFactory.create_batch(5, name='Carla'))
    session.add_all(UserFactory.create_batch(3, name='Sabrina'))
    await session.commit()

    response = client.get(
        '/users/?name=Sab', headers={'Authorization': f'Bearer {token_admin}'}
    )
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['users']) == expected_len
