from playwright.sync_api import Page, expect

class HomePage:
    def __init__(self, page: Page):
        self.page = page
        self.upgrade_button = page.get_by_role("button", name="Upgrade")
        self.performance_link = page.get_by_role("link", name="Performance")
        self.dashboard_link = page.get_by_role("link", name="Dashboard")

    def is_upgrade_button_visible(self, timeout: float = 5000):
        expect(self.upgrade_button).to_be_visible(timeout=timeout)
        return True
              
    def click_performance(self):
        self.performance_link.click()

    def click_dashboard(self):
        self.dashboard_link.click()
