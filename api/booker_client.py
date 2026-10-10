import requests


def booking_payload(**overrides):
    payload = {
        "firstname": "Zara",
        "lastname": "Chiba",
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2026-10-20",
            "checkout": "2026-10-25",
        },
        "additionalneeds": "Breakfast",
    }
    payload.update(overrides)
    return payload


class BookerClient:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})

    def get_bookings(self):
        return self.session.get(f"{self.base_url}/booking", timeout=30)

    def get_booking(self, booking_id):
        return self.session.get(f"{self.base_url}/booking/{booking_id}", timeout=30)

    def create_booking(self, payload):
        return self.session.post(
            f"{self.base_url}/booking",
            json=payload,
            timeout=30,
        )

    def create_token(self, username, password):
        return self.session.post(
            f"{self.base_url}/auth",
            json={"username": username, "password": password},
            timeout=30,
        )

    def update_booking(self, booking_id, payload, token=None):
        headers = {}
        if token:
            headers["Cookie"] = f"token={token}"
        return self.session.put(
            f"{self.base_url}/booking/{booking_id}",
            json=payload,
            headers=headers,
            timeout=30,
        )

    def delete_booking(self, booking_id, token):
        return self.session.delete(
            f"{self.base_url}/booking/{booking_id}",
            headers={"Cookie": f"token={token}"},
            timeout=30,
        )
