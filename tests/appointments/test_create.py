from datetime import date
from http import HTTPStatus


def test_create_appointment(client, header_client):
    data = {
        'date': date.today().isoformat(),
        'modality_id': 1,
    }
    response = client.post('/appointments/', headers=header_client, json=data)
    assert response.status_code == HTTPStatus.CREATED


def test_create_appointment_with_wrong_modality(client, header_client):
    data = {
        'date': date.today().isoformat(),
        'modality_id': 0,
    }
    response = client.post('/appointments/', headers=header_client, json=data)
    assert response.status_code == HTTPStatus.NOT_FOUND
