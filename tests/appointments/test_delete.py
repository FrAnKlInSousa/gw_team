from http import HTTPStatus


def test_delete_appointment(client, create_appointment, header_client):
    response = client.delete(
        f'appointments/{create_appointment.id}', headers=header_client
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Appointment deleted successfully'}


def test_delete_appointment_not_found(client, header_client):
    response = client.delete('/appointments/0', headers=header_client)
    assert response.status_code == HTTPStatus.NOT_FOUND
