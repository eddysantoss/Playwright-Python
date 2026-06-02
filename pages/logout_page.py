from playwright.sync_api import Page, expect

class LogoutPage:
    def __init__(self, page: Page):
        self.page = page
        self.user_menu_button = self.page.locator('.oxd-userdropdown-tab')
        self.logout_button = self.page.locator('a.oxd-userdropdown-link', has_text='Logout')
        self.login_heading = self.page.get_by_role('heading', name='Login')

    def open_user_menu(self):
        self.user_menu_button.click()

    def click_logout(self):
        self.logout_button.click()

    def expect_logged_out(self, timeout: float = 5000):
        expect(self.login_heading).to_be_visible(timeout=timeout)
