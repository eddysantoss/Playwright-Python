
from pages.login_page import LoginPage
from pages.home_page import HomePage


def test_successful_login(page, credentials):
    login_page = LoginPage(page)
    home_page = HomePage(page)

    page.goto(login_page.url)
    login_page.enter_login_credentials(credentials["username"], credentials["password"])
    assert home_page.is_upgrade_button_visible()
    home_page.click_performance()
    home_page.click_dashboard()
    
def test_invalid_login(page, invalid_credentials):
    login_page = LoginPage(page)

    page.goto(login_page.url)
    login_page.enter_login_credentials(invalid_credentials["username"], invalid_credentials["password"])
    assert login_page.is_login_invalid_credentials()
