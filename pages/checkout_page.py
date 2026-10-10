from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    FIRST_NAME = (By.CSS_SELECTOR, "[data-test='firstName']")
    LAST_NAME = (By.CSS_SELECTOR, "[data-test='lastName']")
    POSTAL_CODE = (By.CSS_SELECTOR, "[data-test='postalCode']")
    CONTINUE = (By.CSS_SELECTOR, "[data-test='continue']")
    FINISH = (By.CSS_SELECTOR, "[data-test='finish']")
    COMPLETE_HEADER = (By.CSS_SELECTOR, "[data-test='complete-header']")
    ERROR = (By.CSS_SELECTOR, "[data-test='error']")

    def fill_info(self, first_name, last_name, zip_code):
        self.type(self.FIRST_NAME, first_name)
        self.type(self.LAST_NAME, last_name)
        self.type(self.POSTAL_CODE, zip_code)
        self.click(self.CONTINUE)

    def finish(self):
        self.click(self.FINISH)

    def complete_message(self):
        return self.get_text(self.COMPLETE_HEADER)

    def continue_checkout(self):
        self.click(self.CONTINUE)

    def error_message(self):
        return self.get_text(self.ERROR)
