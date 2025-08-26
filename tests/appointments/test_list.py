from http import HTTPStatus


def test_list_appointments(client, header_client, create_appointment):
    response = client.get('/appointments', headers=header_client)
    assert response.status_code == HTTPStatus.OK
