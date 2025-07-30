from http import HTTPStatus


def test_read_user(client, user):
    response = client.get(f'/users/{user.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'name': user.name,
        'last_name': user.last_name,
        'id': user.id,
        'email': user.email,
    }


def test_read_user_not_found(client):
    response = client.get('/users/0')
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_create_user(client):
    payload = {
        'name': 'test',
        'last_name': 'last_test',
        'email': 'tst@tst.com',
        'password': 'tst_secret',
    }
    response = client.post(
        '/users/',
        json=payload,
    )
    del payload['password']
    payload.update({'id': 1})

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == payload


def test_create_user_with_existing_email(client, user):
    payload = {
        'name': 'test',
        'last_name': 'last_test',
        'email': user.email,
        'password': 'tst_secret',
    }
    response = client.post('/users/', json=payload)
    assert response.status_code == HTTPStatus.CONFLICT
