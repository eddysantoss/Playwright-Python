import os
import pytest
from dotenv import load_dotenv
from pages.pim_page import PimPage
from pages.login_page import LoginPage
from pages.home_page import HomePage
from playwright.sync_api import sync_playwright

load_dotenv(override=True)

@pytest.fixture
def credentials():
    return {
        "username": os.getenv("TEST_USERNAME", "Admin"),
        "password": os.getenv("TEST_PASSWORD", "admin123"),
    }
    
@pytest.fixture
def invalid_credentials():
    return {
        "username": os.getenv("TEST_INVALID_USERNAME", "invalid_user"),
        "password": os.getenv("TEST_INVALID_PASSWORD", "invalid_pass"),
    }

@pytest.fixture
def authenticated_pim_page(page, credentials):
    """
    Fixture: Authenticated user ready on the PIM page

    Preconditions:
    - Successful login
    - PIM page loaded and ready for operations

    Scope: function (new instance per test)

    Returns:
        PimPage: Instance ready for use in tests
    """
    login_page = LoginPage(page)
    home_page = HomePage(page)
    pim_page = PimPage(page)
    
    page.goto(login_page.url)
    login_page.enter_login_credentials(credentials["username"], credentials["password"])
    assert home_page.is_upgrade_button_visible()
    
    pim_page.wait_for_pim_page_loaded()
    
    return pim_page

@pytest.fixture
def page():
    with sync_playwright() as p:
        headless = os.getenv("PLAYWRIGHT_HEADLESS", "false").lower() == "true"
        browser = p.chromium.launch(
            headless=headless,
            args=["--start-maximized"]
        )
        context = browser.new_context(no_viewport=True)
        page = context.new_page()
        yield page
        browser.close()