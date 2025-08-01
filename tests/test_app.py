from http import HTTPStatus


def test_check_health(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'status': HTTPStatus.OK}
