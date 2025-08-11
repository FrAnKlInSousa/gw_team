from http import HTTPStatus


def test_update_password(client, user, header_client):
    old_pass = user.clean_password

    response = client.patch(
        f'/users/password/{user.id}',
        headers=header_client,
        json={'new_password': 'new_pass'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Password changed successfully'}

    # todo: mover o restante para teste de integração
    response = client.post(
        '/auth/token', data={'username': user.email, 'password': 'new_pass'}
    )
    assert response.status_code == HTTPStatus.OK

    response = client.post(
        '/auth/token', data={'username': user.email, 'password': old_pass}
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_update_other_user_password(client, header_client):
    response = client.patch(
        '/users/password/0',
        headers=header_client,
        json={'new_password': 'new_pass'},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_update_other_user_password_with_admin(client, header_admin, user):
    response = client.patch(
        f'/users/password/{user.id}',
        headers=header_admin,
        json={'new_password': 'new_pass'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Password changed successfully'}


def test_update_password_user_not_found(client, header_admin):
    response = client.patch(
        '/users/password/0',
        headers=header_admin,
        json={'new_password': 'new_pass'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
