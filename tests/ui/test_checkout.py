import pytest

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


@pytest.mark.smoke
def test_checkout_completes_order(driver, ui_base_url):
    login_page = LoginPage(driver, ui_base_url)
    login_page.open_login()
    login_page.login("standard_user", "secret_sauce")

    inventory_page = InventoryPage(driver, ui_base_url)
    inventory_page.add_backpack()
    inventory_page.open_cart()

    cart_page = CartPage(driver, ui_base_url)
    cart_page.checkout()

    checkout_page = CheckoutPage(driver, ui_base_url)
    checkout_page.fill_info("John", "Doe", "12345")
    checkout_page.finish()

    assert checkout_page.complete_message() == "Thank you for your order!"
    assert "/checkout-complete.html" in driver.current_url


@pytest.mark.regression
def test_checkout_requires_first_name(driver, ui_base_url):
    login_page = LoginPage(driver, ui_base_url)
    login_page.open_login()
    login_page.login("standard_user", "secret_sauce")

    inventory_page = InventoryPage(driver, ui_base_url)
    inventory_page.add_backpack()
    inventory_page.open_cart()

    cart_page = CartPage(driver, ui_base_url)
    cart_page.checkout()

    checkout_page = CheckoutPage(driver, ui_base_url)
    checkout_page.continue_checkout()

    assert "First Name is required" in checkout_page.error_message()
    assert "/checkout-step-two.html" not in driver.current_url
