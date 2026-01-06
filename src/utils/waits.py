from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

DEFAULT_TIMEOUT = 10

def wait_visible(driver, locator, timeout: int = DEFAULT_TIMEOUT):
    return WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(locator))

def wait_clickable(driver, locator, timeout: int = DEFAULT_TIMEOUT):
    return WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(locator))

def wait_url_contains(driver, fragment: str, timeout: int = DEFAULT_TIMEOUT):
    return WebDriverWait(driver, timeout).until(EC.url_contains(fragment))
