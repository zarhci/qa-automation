import pytest

from api.booker_client import booking_payload


@pytest.mark.critical_path
def test_get_booking_ids(client):
    response = client.get_booking_ids()
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list) and data
    assert "bookingid" in data[0]


@pytest.mark.smoke
def test_create_booking_minimal(client, cleanup):
    payload = booking_payload()
    payload.pop("additionalneeds")
    response = client.create_booking(payload)
    assert response.status_code == 200
    body = response.json()
    assert "bookingid" in body
    cleanup.append(body["bookingid"])


@pytest.mark.critical_path
def test_create_booking_full(client, cleanup):
    payload = booking_payload()
    response = client.create_booking(payload)
    assert response.status_code == 200
    body = response.json()
    cleanup.append(body["bookingid"])
    created = body["booking"]
    assert created["firstname"] == payload["firstname"]
    assert created["lastname"] == payload["lastname"]
    assert created["totalprice"] == payload["totalprice"]
    assert created["additionalneeds"] == payload["additionalneeds"]


@pytest.mark.extended
def test_create_booking_empty_body(client):
    response = client.create_booking({})
    assert response.status_code == 500
    assert "bookingid" not in response.text


@pytest.mark.extended
def test_create_booking_without_firstname(client):
    payload = booking_payload()
    payload.pop("firstname")
    response = client.create_booking(payload)
    assert response.status_code == 500
    assert "bookingid" not in response.text


@pytest.mark.critical_path
def test_get_booking_by_id(client, booking):
    response = client.get_booking(booking)
    assert response.status_code == 200
    body = response.json()
    assert body["firstname"] == booking_payload()["firstname"]
    assert body["lastname"] == booking_payload()["lastname"]


@pytest.mark.extended
def test_get_nonexistent_booking(client):
    response = client.get_booking(999999999)
    assert response.status_code == 404
