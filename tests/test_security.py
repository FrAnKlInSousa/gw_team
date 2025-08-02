from http import HTTPStatus

from jwt import encode

from gw_team.settings import Settings

settings = Settings()


def custom_encode(payload: dict, key: str):
    return encode(payload, key, algorithm=settings.ALGORITHM)


def build_header(payload: dict, key: str = settings.SECRET_KEY):
    test_token = custom_encode(payload, key)
    return {'Authorization': f'Bearer {test_token}'}


def test_current_user_decode_error(client):
    fake_key = 'wrong-secret'
    payload = {'sub': 'someuser@test.com'}

    headers = build_header(payload, fake_key)
    response = client.get('/users/1', headers=headers)
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_current_user_without_sub(client):
    headers = build_header({})
    response = client.get('/users/1', headers=headers)
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_current_user_not_found(client):
    payload = {'sub': 'fake@email.com'}

    headers = build_header(payload)

    response = client.get('/users/1', headers=headers)
    assert response.status_code == HTTPStatus.UNAUTHORIZED
