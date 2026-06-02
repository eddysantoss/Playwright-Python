from pages.login_page import LoginPage
from pages.logout_page import LogoutPage


def test_logout(page, credentials):
    login_page = LoginPage(page)
    logout_page = LogoutPage(page)

    page.goto(login_page.url)
    login_page.enter_login_credentials(credentials["username"], credentials["password"])

    logout_page.open_user_menu()
    logout_page.click_logout()
    logout_page.expect_logged_out()
    

