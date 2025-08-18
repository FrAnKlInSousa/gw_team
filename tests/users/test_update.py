from http import HTTPStatus

from gw_team.schemas.users import UserPublic
from tests.faker import fake


def test_update_all_user_info(client, user, header_client):
    user_info = {
        'name': fake.name(),
        'last_name': fake.last_name(),
        'email': fake.email(),
        'user_type': fake.user_type(),
    }
    response = client.patch(
        f'/users/{user.id}', headers=header_client, json=user_info
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == UserPublic.model_validate(user).model_dump()


def test_update_user_not_found(client, header_admin):
    response = client.patch('/users/0', headers=header_admin, json={})
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_other_user_error(client, header_client):
    response = client.patch('/users/0', headers=header_client, json={})
    assert response.status_code == HTTPStatus.FORBIDDEN
