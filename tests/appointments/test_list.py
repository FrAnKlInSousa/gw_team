from http import HTTPStatus

import pytest

from tests.conftest import AppointmentFactory


def test_list_appointments(client, header_client):
    response = client.get('/appointments', headers=header_client)
    assert response.status_code == HTTPStatus.OK
    assert response.json()['appointments'] == []


@pytest.mark.asyncio
async def test_list_appointments_should_return_3(
    client, session, header_client, user, random_modality_id
):
    expected_len = 10
    session.add_all(
        AppointmentFactory.create_batch(
            10, user_id=user.id, modality_id=random_modality_id
        )
    )
    await session.commit()

    response = client.get('/appointments', headers=header_client)
    response_json = response.json().get('appointments')
    assert response.status_code == HTTPStatus.OK
    assert len(response_json) == expected_len
