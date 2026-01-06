import pytest
from src.pages.login_page import LoginPage
from src.pages.inventory_page import InventoryPage

@pytest.mark.ui
@pytest.mark.smoke
def test_login_success(driver, base_url, creds):
    username, password = creds

    login = LoginPage(driver)
    login.open(base_url)
    login.login(username, password)

    inventory = InventoryPage(driver)
    inventory.assert_loaded()

@pytest.mark.ui
def test_login_invalid_user_shows_error(driver, base_url):
    login = LoginPage(driver)
    login.open(base_url)
    login.login("invalid_user", "secret_sauce")

    msg = login.error_message()
    assert "Username and password do not match" in msg or "Epic sadface" in msg
