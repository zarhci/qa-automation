import pytest

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


@pytest.mark.smoke
def test_login_with_valid_credentials(driver, ui_base_url):
    login_page = LoginPage(driver, ui_base_url)
    login_page.open_login()
    login_page.login("standard_user", "secret_sauce")

    inventory_page = InventoryPage(driver, ui_base_url)

    assert "/inventory.html" in driver.current_url
    assert inventory_page.title() == "Products"


@pytest.mark.regression
@pytest.mark.parametrize(
    "username, password, error",
    [
        ("locked_out_user", "secret_sauce", "Sorry, this user has been locked out"),
        ("standard_user", "wrong_password", "Username and password do not match"),
        ("", "secret_sauce", "Username is required"),
    ],
)
def test_login_shows_error(driver, ui_base_url, username, password, error):
    page = LoginPage(driver, ui_base_url)
    page.open_login()
    page.login(username, password)

    assert "/inventory.html" not in driver.current_url
    assert error in page.error_message()
