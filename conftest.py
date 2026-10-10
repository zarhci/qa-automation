import os
import pytest

BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com")


@pytest.fixture
def ui_base_url():
    return BASE_URL
