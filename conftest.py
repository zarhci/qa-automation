import os

import pytest


BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com")

BOOKER_BASE_URL = os.getenv(
    "BOOKER_BASE_URL",
    "https://restful-booker.herokuapp.com",
)


@pytest.fixture(scope="session")
def ui_base_url():
    return BASE_URL


@pytest.fixture(scope="session")
def api_base_url():
    return BOOKER_BASE_URL
