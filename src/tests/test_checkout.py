import pytest
from src.pages.login_page import LoginPage
from src.pages.inventory_page import InventoryPage
from src.pages.cart_page import CartPage
from src.pages.checkout_page import CheckoutStepOnePage, CheckoutStepTwoPage, CheckoutCompletePage

@pytest.mark.ui
@pytest.mark.smoke
def test_checkout_happy_path(driver, base_url, creds):
    username, password = creds

    login = LoginPage(driver)
    login.open(base_url)
    login.login(username, password)

    inventory = InventoryPage(driver)
    inventory.assert_loaded()
    inventory.add_backpack_to_cart()
    inventory.open_cart()

    cart = CartPage(driver)
    cart.assert_loaded()
    cart.checkout()

    step1 = CheckoutStepOnePage(driver)
    step1.assert_loaded()
    step1.enter_info_and_continue("Kris", "Tom", "94086")

    step2 = CheckoutStepTwoPage(driver)
    step2.assert_loaded()
    step2.finish()

    complete = CheckoutCompletePage(driver)
    complete.assert_loaded()
    assert "THANK YOU" in complete.success_message().upper()
