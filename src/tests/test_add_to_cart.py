import pytest
from src.pages.login_page import LoginPage
from src.pages.inventory_page import InventoryPage
from src.pages.cart_page import CartPage

@pytest.mark.ui
def test_add_item_to_cart(driver, base_url, creds):
    username, password = creds

    LoginPage(driver).open(base_url)
    LoginPage(driver).login(username, password)

    inventory = InventoryPage(driver)
    inventory.assert_loaded()
    inventory.add_backpack_to_cart()
    inventory.open_cart()

    cart = CartPage(driver)
    cart.assert_loaded()
    cart.assert_has_items()
