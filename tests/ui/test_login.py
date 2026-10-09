import pytest

from pages.login_page import LoginPage


@pytest.mark.smoke
def test_login_with_valid_credentials(driver, ui_base_url):
    page = LoginPage(driver, ui_base_url)
    page.open_login()
    page.login("standard_user", "secret_sauce")

    assert "/inventory.html" in driver.current_url
