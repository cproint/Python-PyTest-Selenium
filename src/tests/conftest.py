# src/tests/conftest.py
import pathlib
import tempfile
import shutil

import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from src.config import settings

ARTIFACTS_DIR = pathlib.Path("artifacts")


def _build_chrome_driver() -> webdriver.Chrome:
    opts = ChromeOptions()

    # Fresh profile every run to avoid persisted state popups
    user_data_dir = tempfile.mkdtemp(prefix="selenium-chrome-profile-")
    opts.add_argument(f"--user-data-dir={user_data_dir}")

    # macOS: avoid Keychain/password-store UI that can trigger blocking prompts
    opts.add_argument("--password-store=basic")
    opts.add_argument("--use-mock-keychain")

    if settings.headless:
        opts.add_argument("--headless=new")

    # Stability / compatibility
    opts.add_argument("--window-size=1400,900")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")

    # Best-effort suppression of password/leak UI
    opts.add_argument("--disable-notifications")
    opts.add_argument("--disable-save-password-bubble")
    opts.add_argument("--disable-features=PasswordLeakDetection")

    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "autofill.profile_enabled": False,
        "autofill.credit_card_enabled": False,
    }
    opts.add_experimental_option("prefs", prefs)

    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=opts)
    driver.implicitly_wait(0)

    driver._temp_user_data_dir = user_data_dir  # type: ignore[attr-defined]
    return driver


def _build_firefox_driver() -> webdriver.Firefox:
    opts = FirefoxOptions()
    if settings.headless:
        opts.add_argument("-headless")

    opts.set_preference("signon.rememberSignons", False)
    opts.set_preference("signon.autofillForms", False)
    opts.set_preference("dom.webnotifications.enabled", False)

    service = FirefoxService(executable_path=GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=opts)
    driver.implicitly_wait(0)
    driver.set_window_size(1400, 900)
    return driver


def _build_driver():
    browser = (settings.browser or "chrome").lower()
    if browser == "firefox":
        return _build_firefox_driver()
    return _build_chrome_driver()


@pytest.fixture(scope="session")
def base_url():
    return settings.base_url


@pytest.fixture(scope="session")
def creds():
    return settings.username, settings.password


@pytest.fixture()
def driver():
    drv = _build_driver()
    yield drv

    temp_dir = getattr(drv, "_temp_user_data_dir", None)
    try:
        drv.quit()
    finally:
        if temp_dir:
            shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        drv = item.funcargs.get("driver")
        if not drv:
            return

        ARTIFACTS_DIR.mkdir(exist_ok=True)

        # Screenshot
        try:
            drv.save_screenshot(str(ARTIFACTS_DIR / f"{item.name}.png"))
        except Exception:
            pass

        # Page source
        try:
            (ARTIFACTS_DIR / f"{item.name}.html").write_text(drv.page_source, encoding="utf-8")
        except Exception:
            pass
