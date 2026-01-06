from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from src.utils.waits import wait_visible, wait_clickable
from src.utils.logger import get_logger

class BasePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.log = get_logger(self.__class__.__name__)

    def open(self, url: str):
        self.log.info(f"Open URL: {url}")
        self.driver.get(url)

    def find_visible(self, locator):
        return wait_visible(self.driver, locator)

    def click(self, locator):
        el = wait_clickable(self.driver, locator)
        el.click()
        return el

    def type(self, locator, text: str, clear: bool = True):
        el = self.find_visible(locator)
        if clear:
            el.clear()
        el.send_keys(text)
        return el

    def text_of(self, locator) -> str:
        return self.find_visible(locator).text

    def is_displayed(self, locator) -> bool:
        try:
            return self.find_visible(locator).is_displayed()
        except Exception:
            return False
