# src/pages/checkout_page.py
from selenium.webdriver.common.by import By
from src.pages.base_page import BasePage
from src.utils.waits import wait_url_contains, wait_visible

class CheckoutStepOnePage(BasePage):
    TITLE = (By.CSS_SELECTOR, "span.title")
    FIRST = (By.ID, "first-name")
    LAST = (By.ID, "last-name")
    ZIP = (By.ID, "postal-code")
    CONTINUE = (By.ID, "continue")
    ERROR = (By.CSS_SELECTOR, "[data-test='error']")

    def assert_loaded(self):
        assert self.text_of(self.TITLE) == "Checkout: Your Information"

    def enter_info_and_continue(self, first: str, last: str, zip_code: str):
        self.type(self.FIRST, first)
        self.type(self.LAST, last)
        self.type(self.ZIP, zip_code)
        self.click(self.CONTINUE)

    def has_error(self) -> bool:
        return self.is_displayed(self.ERROR)

    def error_message(self) -> str:
        return self.text_of(self.ERROR)


class CheckoutStepTwoPage(BasePage):
    TITLE = (By.CSS_SELECTOR, "span.title")
    FINISH = (By.ID, "finish")

    def assert_loaded(self):
        # Strong signal that navigation finished
        wait_url_contains(self.driver, "checkout-step-two.html", timeout=10)

        # Strong signal that Step Two UI is ready
        wait_visible(self.driver, self.FINISH, timeout=10)

        # Then assert title
        assert self.text_of(self.TITLE) == "Checkout: Overview"

    def finish(self):
        self.click(self.FINISH)


class CheckoutCompletePage(BasePage):
    TITLE = (By.CSS_SELECTOR, "span.title")
    COMPLETE_HEADER = (By.CSS_SELECTOR, "[data-test='complete-header']")

    def assert_loaded(self):
        wait_url_contains(self.driver, "checkout-complete.html", timeout=10)
        assert self.text_of(self.TITLE) == "Checkout: Complete!"

    def success_message(self) -> str:
        return self.text_of(self.COMPLETE_HEADER)
