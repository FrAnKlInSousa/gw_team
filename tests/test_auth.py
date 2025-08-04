from http import HTTPStatus

import pytest


def test_authenticate(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},  # type: ignore[attr-defined]
    )

    assert response.status_code == HTTPStatus.CREATED
    assert 'access_token' in response.json()
    assert 'token_type' in response.json()


def test_authenticate_error_by_wrong_email(client, token, user):
    response = client.post(
        '/auth/token',
        data={'username': 'wrong@test.com', 'password': user.clean_password},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_authenticate_error_by_wrong_password(client, token, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': 'wrong_secret'},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.asyncio
async def test_authenticate_error_with_disabled_account(client, custom_user):
    new_user = await custom_user(disabled=True)
    response = client.post(
        '/auth/token',
        data={'username': new_user.email, 'password': new_user.password},
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'User account is not active'}
