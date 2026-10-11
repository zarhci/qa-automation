import pytest

from api.booker_client import booking_payload


@pytest.mark.critical_path
def test_update_booking_with_token(client, token, booking):
    new_data = booking_payload(firstname="Anna", lastname="Sidorova", totalprice=300)
    response = client.update_booking(booking, new_data, token)
    assert response.status_code == 200
    body = response.json()
    assert body["firstname"] == "Anna"
    assert body["lastname"] == "Sidorova"
    assert body["totalprice"] == 300


@pytest.mark.extended
def test_update_booking_without_token(client, booking):
    response = client.update_booking(
        booking, booking_payload(firstname="Hacker", lastname="X")
    )
    assert response.status_code == 403
    # бронь осталась прежней
    after = client.get_booking(booking).json()
    assert after["firstname"] == booking_payload()["firstname"]
    assert after["lastname"] == booking_payload()["lastname"]


@pytest.mark.critical_path
def test_delete_booking_with_token(client, token, booking):
    response = client.delete_booking(booking, token)
    assert response.status_code == 201  # DELETE даёт 201 Created
    assert client.get_booking(booking).status_code == 404


@pytest.mark.extended
def test_delete_booking_without_token(client, booking):
    response = client.delete_booking(booking)
    assert response.status_code == 403
    assert client.get_booking(booking).status_code == 200
