from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CartPage(BasePage):
    ITEM_NAME = (By.CSS_SELECTOR, "[data-test='inventory-item-name']")
    CHECKOUT = (By.CSS_SELECTOR, "[data-test='checkout']")

    def item_name(self):
        return self.get_text(self.ITEM_NAME)

    def checkout(self):
        self.click(self.CHECKOUT)
