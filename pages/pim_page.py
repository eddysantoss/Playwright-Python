import re

from playwright.sync_api import Page, expect


class PimPage:
    DEFAULT_TIMEOUT = 5000
    
    def __init__(self, page: Page):
        self.page = page
        self.pim_page = page.get_by_role("link", name="PIM")
        self.add_employee_button = page.get_by_role("link", name="Add Employee")
        self.first_name_input = page.get_by_role("textbox", name="First Name")
        self.middle_name_input = page.get_by_role("textbox", name="Middle Name")    
        self.last_name_input = page.get_by_role("textbox", name="Last Name")
        self.save_button = page.get_by_role("button", name="Save")
        
                               
    def wait_for_PIM_page_loaded(self, timeout: float = DEFAULT_TIMEOUT) -> bool:
        expect(self.page.get_by_text("PIM", exact=True)).to_be_visible(timeout=timeout)
        return True
    
    def _wait_and_click(self, locator, timeout: float = DEFAULT_TIMEOUT):
        expect(locator).to_be_visible(timeout=timeout)
        expect(locator).to_be_enabled(timeout=timeout)
        locator.click()
        
    def _wait_and_fill(self, locator, value: str, timeout: float = DEFAULT_TIMEOUT):   
        expect(locator).to_be_visible(timeout=timeout)
        expect(locator).to_be_enabled(timeout=timeout)
        locator.fill(value)

    def add_employee(self, first_name: str, middle_name: str, last_name: str, timeout: float = DEFAULT_TIMEOUT):
        """
        "Adds a new employee by filling in the required fields and clicking save
        
        """
        self._wait_and_click(self.pim_page, timeout)
        self._wait_and_click(self.add_employee_button, timeout)

        self._wait_and_fill(self.first_name_input, first_name, timeout)
        self._wait_and_fill(self.middle_name_input, middle_name, timeout)
        self._wait_and_fill(self.last_name_input, last_name, timeout)

        self._wait_and_click(self.save_button, timeout)
        
    def is_employee_added_successfully(self, timeout: float = DEFAULT_TIMEOUT) -> bool:
        expect(self.page.get_by_text("Success", exact=True)).to_be_visible(timeout=timeout)
        return True
        
        
    def get_error_messages(self, timeout: float = DEFAULT_TIMEOUT) -> list:
        expect(self.page.get_by_text("Required").first).to_be_visible(timeout=timeout)
        error_elements = self.page.get_by_text("Required").all()
        return [elem.inner_text() for elem in error_elements if elem.is_visible()]
    
    def search_employee(self, employee_full_name: str, employee_partial_name: str, timeout: float = DEFAULT_TIMEOUT) -> bool:
        """
        Search for an employee by name in the employee list.

        """
        # Navigate to Employee List if not already there
        employee_list_link = self.page.get_by_role("link", name="Employee List")
        self._wait_and_click(employee_list_link, timeout)
        expect(self.page.get_by_role("heading", name="Employee Information")).to_be_visible(timeout=timeout)
        
        # Fill the search field
        search_input = self.page.get_by_role("textbox", name="Type for hints...").first
        search_input.clear()
        self._wait_and_fill(search_input, employee_full_name, timeout)
        
        search_button = self.page.locator("button[type='submit']")
        self._wait_and_click(search_button, timeout)
        
        employee_row = self.page.locator(f"text={employee_partial_name}").first
        expect(employee_row).to_be_visible(timeout=timeout)
        return True
    
    def is_employee_in_results(self, employee_partial_name: str, timeout: float = DEFAULT_TIMEOUT) -> bool:
        """
        Checks if an employee with the given partial name is present in the search results.
        
        """
        employee_row = self.page.locator(f"text={employee_partial_name}").first
        expect(employee_row).to_be_visible(timeout=timeout)
               
        
    def delete_employee(self, timeout: float = DEFAULT_TIMEOUT) -> bool:
        """
        Deletes a selected employee from the list.
        
        """
        delete_button = self.page.locator(".oxd-table-card-cell-checkbox > .oxd-checkbox-wrapper > label > .oxd-checkbox-input > .oxd-icon").first
        self._wait_and_click(delete_button, timeout)
            
        delete_selected_button = self.page.get_by_role("button", name=" Delete Selected")
        self._wait_and_click(delete_selected_button, timeout)
        
        confirm_delete_button = self.page.get_by_role("button", name=" Yes, Delete")
        self._wait_and_click(confirm_delete_button, timeout)
        return True
        
    def is_employee_deleted_successfully(self, timeout: float = DEFAULT_TIMEOUT) -> bool:
        
        success_message = self.page.get_by_text(re.compile(r"Successfully Deleted"), exact=False)
        expect(success_message).to_be_visible(timeout=timeout)
        return True


