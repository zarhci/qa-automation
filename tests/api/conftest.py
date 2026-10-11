import pytest

from api.booker_client import BookerClient, booking_payload


@pytest.fixture(scope="session")
def client():
    return BookerClient()


@pytest.fixture(scope="session")
def token(client):
    response = client.create_token()
    assert response.status_code == 200
    return response.json()["token"]


@pytest.fixture
def cleanup(client, token):
    """Список ID, которые тест создал сам. После теста все удаляются."""
    ids = []
    yield ids
    for booking_id in ids:
        client.delete_booking(booking_id, token)


@pytest.fixture
def booking(client, cleanup):
    """Готовая бронь для тестов GET / PUT / DELETE. Возвращает её ID."""
    response = client.create_booking(booking_payload())
    assert response.status_code == 200
    booking_id = response.json()["bookingid"]
    cleanup.append(booking_id)
    return booking_id
