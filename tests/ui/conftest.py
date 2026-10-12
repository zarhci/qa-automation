import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture
def driver():
    options = Options()
    if os.getenv("HEADLESS", "false").lower() == "true":
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

    options.add_experimental_option(
        "prefs", {"profile.password_manager_leak_detection": False}
    )

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(0)
    yield driver
    driver.quit()
