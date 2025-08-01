from http import HTTPStatus


def test_create_user(client):
    payload = {
        'name': 'test',
        'last_name': 'last_test',
        'email': 'tst@tst.com',
        'password': 'tst_secret',
        'user_type': 'client',
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
        'user_type': 'client',
    }
    response = client.post('/users/', json=payload)
    assert response.status_code == HTTPStatus.CONFLICT
