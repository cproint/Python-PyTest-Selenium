from selenium.webdriver.common.by import By
from src.pages.base_page import BasePage

class InventoryPage(BasePage):
    TITLE = (By.CSS_SELECTOR, "span.title")
    CART_BADGE = (By.CSS_SELECTOR, ".shopping_cart_badge")
    CART_LINK = (By.ID, "shopping_cart_container")

    # Example: Sauce Labs Backpack
    ADD_BACKPACK = (By.ID, "add-to-cart-sauce-labs-backpack")
    REMOVE_BACKPACK = (By.ID, "remove-sauce-labs-backpack")

    def assert_loaded(self):
        assert self.text_of(self.TITLE) == "Products"

    def add_backpack_to_cart(self):
        self.click(self.ADD_BACKPACK)

    def open_cart(self):
        self.click(self.CART_LINK)
