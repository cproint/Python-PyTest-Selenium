from selenium.webdriver.common.by import By
from src.pages.base_page import BasePage

class CartPage(BasePage):
    TITLE = (By.CSS_SELECTOR, "span.title")
    CHECKOUT_BTN = (By.ID, "checkout")
    CART_ITEM = (By.CSS_SELECTOR, ".cart_item")

    def assert_loaded(self):
        assert self.text_of(self.TITLE) == "Your Cart"

    def assert_has_items(self):
        assert len(self.driver.find_elements(*self.CART_ITEM)) > 0

    def checkout(self):
        self.click(self.CHECKOUT_BTN)
