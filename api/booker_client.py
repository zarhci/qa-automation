import requests

BASE_URL = "https://restful-booker.herokuapp.com"
USERNAME = "admin"
PASSWORD = "password123"


def booking_payload(**overrides):
    """Валидное тело брони. Любое поле можно заменить: booking_payload(firstname="Anna")."""
    payload = {
        "firstname": "Ivan",
        "lastname": "Petrov",
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {"checkin": "2026-11-01", "checkout": "2026-11-05"},
        "additionalneeds": "Breakfast",
    }
    payload.update(overrides)
    return payload


class BookerClient:
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update(
            {"Content-Type": "application/json", "Accept": "application/json"}
        )

    @staticmethod
    def _auth(token):
        return {"Cookie": f"token={token}"} if token else {}

    def create_token(self, username=USERNAME, password=PASSWORD):
        return self.session.post(
            f"{self.base_url}/auth",
            json={"username": username, "password": password},
            timeout=10,
        )

    def get_booking_ids(self):
        return self.session.get(f"{self.base_url}/booking", timeout=10)

    def get_booking(self, booking_id):
        return self.session.get(f"{self.base_url}/booking/{booking_id}", timeout=10)

    def create_booking(self, payload):
        return self.session.post(f"{self.base_url}/booking", json=payload, timeout=10)

    def update_booking(self, booking_id, payload, token=None):
        return self.session.put(
            f"{self.base_url}/booking/{booking_id}",
            json=payload,
            headers=self._auth(token),
            timeout=10,
        )

    def delete_booking(self, booking_id, token=None):
        return self.session.delete(
            f"{self.base_url}/booking/{booking_id}",
            headers=self._auth(token),
            timeout=10,
        )
