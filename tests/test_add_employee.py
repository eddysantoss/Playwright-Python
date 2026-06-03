import pytest
from pages.login_page import LoginPage  
from pages.home_page import HomePage
from pages.pim_page import PimPage

@pytest.mark.parametrize("first_name, middle_name, last_name", [
    ("Boni", "Middle", "Santos"),
    ("John", "Doe", "Smith"),
    ("Jane", "A.", "Doe"),
    ("Boni", "Chique", "Santos")
    
])

def test_add_employee(page, credentials, first_name, middle_name, last_name):
    login_page = LoginPage(page)
    home_page = HomePage(page)
    pim_page = PimPage(page)
    
    page.goto(login_page.url)
    login_page.enter_login_credentials(credentials["username"], credentials["password"])
    assert home_page.is_upgrade_button_visible()
    
    #Adding new employee
    pim_page.wait_for_PIM_page_loaded()
    pim_page.add_employee(first_name, middle_name, last_name)
    assert pim_page.is_employee_added_successfully()
       
  
    
 