from http import HTTPStatus


def test_delete_user(client, user, header_client):
    response = client.delete(f'/users/{user.id}', headers=header_client)
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User successfully deleted'}


def test_delete_user_not_found(client, header_admin):
    response = client.delete('/users/0', headers=header_admin)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_delete_other_user_as_admin(client, user, header_admin):
    response = client.delete(f'/users/{user.id}', headers=header_admin)
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User successfully deleted'}


def test_delete_other_user_as_client(client, header_client):
    response = client.delete('/users/0', headers=header_client)
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'You have no permission'}
