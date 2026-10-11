import pytest


@pytest.mark.smoke
def test_auth_service_available(client):
    response = client.create_token()
    assert response.status_code == 200


@pytest.mark.critical_path
def test_create_token_with_valid_credentials(client):
    response = client.create_token()
    assert response.status_code == 200
    assert response.json()["token"]  # непустой; тип str не проверяем


@pytest.mark.extended
def test_create_token_with_wrong_password(client):
    response = client.create_token(password="wrong_password")
    assert response.status_code == 200
    body = response.json()
    assert "reason" in body
    assert "token" not in body
