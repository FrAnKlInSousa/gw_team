from http import HTTPStatus


class TestAuth:
    def test_authenticate(self, client, user):
        response = client.post(
            '/auth/token',
            data={'username': user.email, 'password': user.clean_password},  # type: ignore[attr-defined]
        )

        assert response.status_code == HTTPStatus.OK
        assert 'access_token' in response.json()
        assert 'token_type' in response.json()

    def test_authenticate_error_by_wrong_email(self, client, token, user):
        response = client.post(
            '/auth/token',
            data={
                'username': 'wrong@test.com',
                'password': user.clean_password,
            },
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_authenticate_error_by_wrong_password(self, client, token, user):
        response = client.post(
            '/auth/token',
            data={'username': user.email, 'password': 'wrong_secret'},
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_authenticate_error_with_disabled_account(self, client, make_user):
        new_user = make_user(disabled=True)
        response = client.post(
            '/auth/token',
            data={'username': new_user.email, 'password': new_user.password},
        )
        assert response.status_code == HTTPStatus.FORBIDDEN
        assert response.json() == {'detail': 'User account is not active'}
