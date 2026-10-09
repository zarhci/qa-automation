import pytest

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


@pytest.mark.smoke
def test_add_backpack_to_cart(driver, ui_base_url):
    login_page = LoginPage(driver, ui_base_url)
    login_page.open_login()
    login_page.login("standard_user", "secret_sauce")

    inventory_page = InventoryPage(driver, ui_base_url)
    inventory_page.add_backpack()

    assert inventory_page.cart_count() == "1"
