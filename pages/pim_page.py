import re
from typing import Dict, Optional

from playwright.sync_api import Page, expect


class PimPage:
    DEFAULT_TIMEOUT = 5000

    def __init__(self, page: Page) -> None:
        self.page = page
        self.pim_page = page.get_by_role("link", name="PIM")
        self.add_employee_button = page.get_by_role("link", name="Add Employee")
        self.first_name_input = page.get_by_role("textbox", name="First Name")
        self.middle_name_input = page.get_by_role("textbox", name="Middle Name")
        self.last_name_input = page.get_by_role("textbox", name="Last Name")
        self.save_button = page.get_by_role("button", name="Save")
        self.employee_list_link = page.get_by_role("link", name="Employee List")
                                     
    def wait_for_pim_page_loaded(self, timeout: float = DEFAULT_TIMEOUT) -> bool:
        expect(self.page.get_by_text("PIM", exact=True)).to_be_visible(timeout=timeout)
        return True
    
    def _normalize_timeout(self, timeout):
        if isinstance(timeout, str):
            try:
                return float(timeout)
            except ValueError as e:
                raise ValueError(f"Invalid timeout: {timeout!r}") from e
        return timeout

    def _wait_and_click(self, locator, timeout: float = DEFAULT_TIMEOUT):
        timeout = self._normalize_timeout(timeout)
        expect(locator).to_be_visible(timeout=timeout)
        expect(locator).to_be_enabled(timeout=timeout)
        locator.click()
        
    def _wait_and_fill(self, locator, value: str, timeout: float = DEFAULT_TIMEOUT):   
        timeout = self._normalize_timeout(timeout)
        expect(locator).to_be_visible(timeout=timeout)
        expect(locator).to_be_enabled(timeout=timeout)
        locator.fill(value)

    def add_employee(
        self,
        first_name: str,
        middle_name: str,
        last_name: str,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        """Add a new employee and submit the form."""
        self._wait_and_click(self.pim_page, timeout)
        self._wait_and_click(self.add_employee_button, timeout)
        self._wait_and_fill(self.first_name_input, first_name, timeout)
        self._wait_and_fill(self.middle_name_input, middle_name, timeout)
        self._wait_and_fill(self.last_name_input, last_name, timeout)
        self._wait_and_click(self.save_button, timeout)

    def is_employee_added_successfully(self, timeout: float = DEFAULT_TIMEOUT) -> bool:
        toast = self.page.locator(".oxd-toast.oxd-toast--success").first
        expect(toast).to_be_visible(timeout=timeout)
        expect(toast).to_contain_text("Successfully", timeout=timeout)
        return True
              
    def get_error_messages(self, timeout: float = DEFAULT_TIMEOUT) -> list:
        expect(self.page.get_by_text("Required").first).to_be_visible(timeout=timeout)
        error_elements = self.page.get_by_text("Required").all()
        return [elem.inner_text() for elem in error_elements if elem.is_visible()]
    
    def search_employee(
        self,
        employee_full_name: str,
        employee_partial_name: str | None = None,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> bool:
        """Open Employee List and search by full or partial name."""
        self._wait_and_click(self.pim_page, timeout)

        employee_list_link = self.page.get_by_role("link", name="Employee List")
        self._wait_and_click(employee_list_link, timeout)
        expect(
            self.page.get_by_role("heading", name="Employee Information")
        ).to_be_visible(timeout=timeout)

        search_input = self.page.get_by_role("textbox", name="Type for hints...").first
        search_input.clear()
        self._wait_and_fill(search_input, employee_full_name, timeout)

        search_button = self.page.locator("button[type='submit']")
        self._wait_and_click(search_button, timeout)
        return True

    def assert_employee_in_results(
        self,
        employee_name: str,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> bool:
        employee_row = self.page.locator(f"text={employee_name}").first
        expect(employee_row).to_be_visible(timeout=timeout)
        return True
               
        
    def delete_employee(self, timeout: float = DEFAULT_TIMEOUT) -> bool:
        """Delete the selected employee and confirm the action."""
        delete_button = self.page.locator(
            ".oxd-table-card-cell-checkbox > .oxd-checkbox-wrapper > label > "
            ".oxd-checkbox-input > .oxd-icon"
        ).first
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

    def is_employee_not_in_results(
        self,
        employee_partial_name: str,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> bool:
        employee_row = self.page.locator(f"text={employee_partial_name}").first
        expect(employee_row).not_to_be_visible(timeout=timeout)
        return True

    def assert_no_search_results(self, timeout: float = DEFAULT_TIMEOUT) -> bool:
        no_records_message = self.page.get_by_text("No Records Found", exact=True).first
        expect(no_records_message).to_be_visible(timeout=timeout)
        expect(no_records_message).to_contain_text("No Records Found", timeout=timeout)
        return True
    
    def edit_employee(
        self,
        employee_name: str,
        new_first_name: Optional[str] = None,
        new_middle_name: Optional[str] = None,
        new_last_name: Optional[str] = None,
        new_job_title: Optional[str] = None,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        """Edit employee data and validate that the update persists."""
        self._wait_and_click(self.pim_page, timeout)
        self.search_employee(
            employee_partial_name=employee_name,
            employee_full_name=employee_name,
            timeout=timeout,
        )
        
        # Click on the employee name to open details (instead of edit button)
        employee_cell = self.page.get_by_text(employee_name, exact=False).first
        self._wait_and_click(employee_cell, timeout)
        
        # Wait for the employee details form to load
        expect(self.page.locator("input[name='firstName']")).to_be_visible(timeout=timeout)

        # Edit employee fields
        if new_first_name:
            first_input = self.page.locator("input[name='firstName']")
            first_input.clear()
            self._wait_and_fill(first_input, new_first_name, timeout)
            expect(first_input).to_have_value(new_first_name, timeout=timeout)
            
        if new_middle_name:
            middle_input = self.page.locator("input[name='middleName']")
            middle_input.clear()
            self._wait_and_fill(middle_input, new_middle_name, timeout)
            expect(middle_input).to_have_value(new_middle_name, timeout=timeout)
            
        if new_last_name:
            last_input = self.page.locator("input[name='lastName']")
            last_input.click()  
            last_input.clear()
            self._wait_and_fill(last_input, new_last_name, timeout)
            expect(last_input).to_have_value(new_last_name, timeout=timeout)  
                          
        # Save the changes
        save_button = self.page.get_by_role("button", name="Save").first
        self._wait_and_click(save_button, timeout)
        
        # Wait for success message and then for it to disappear (server processing complete)
        toast = self.page.locator(".oxd-toast.oxd-toast--success").first
        expect(toast).to_be_visible(timeout=15000)
        expect(toast).to_contain_text("Successfully Updated", timeout=timeout)
        expect(toast).to_be_hidden(timeout=timeout)
        
        # Refresh the page to get fresh data from server
        self.page.reload()
        expect(self.page.get_by_role("heading", name="Personal Details")).to_be_visible(timeout=timeout)
        
        # Navigate back to Employee List to ensure clean state for next operation
        employee_list_link = self.page.get_by_role("link", name="Employee List")
        self._wait_and_click(employee_list_link, timeout)
        expect(self.page.get_by_role("heading", name="Employee Information")).to_be_visible(timeout=timeout)
        
    def _get_field_value(self, field_name: str, timeout: float = DEFAULT_TIMEOUT) -> str:
        input_locator = self.page.locator(f"input[name='{field_name}']")
        expect(input_locator).to_be_visible(timeout=timeout)

        expect(input_locator).to_have_value(re.compile(r".+"), timeout=timeout)

        value = input_locator.input_value().strip()
        return value

    def get_employee_details(
        self, employee_full_name: str, timeout: float = DEFAULT_TIMEOUT
    ) -> Dict[str, str]:
        """Return employee details as a dict: FirstName, MiddleName, LastName."""
        timeout = self._normalize_timeout(timeout)

        self._wait_and_click(self.pim_page, timeout)
        employee_list_link = self.page.get_by_role("link", name="Employee List")
        self._wait_and_click(employee_list_link, timeout)
        expect(
            self.page.get_by_role("heading", name="Employee Information")
        ).to_be_visible(timeout=timeout)

        search_input = self.page.get_by_role("textbox", name="Type for hints...").first
        search_input.clear()
        self._wait_and_fill(search_input, employee_full_name, timeout)

        search_button = self.page.locator("button[type='submit']")
        self._wait_and_click(search_button, timeout)

        employee_cell = self.page.get_by_text(employee_full_name, exact=True).first
        try:
            expect(employee_cell).to_be_visible(timeout=timeout)
        except AssertionError:
            parts = employee_full_name.strip().split()
            if len(parts) >= 2:
                first, last = parts[0], parts[-1]
                pattern = re.compile(
                    rf"{re.escape(first)}.*{re.escape(last)}", re.IGNORECASE
                )
                employee_cell = self.page.get_by_text(pattern, exact=False).first
                expect(employee_cell).to_be_visible(timeout=timeout)
            else:
                raise
        employee_cell.click()

        expect(self.page.locator("input[name='firstName']")).to_be_visible(timeout=timeout)

        first_name = self._get_field_value("firstName", timeout)
        middle_name = self._get_field_value("middleName", timeout)
        last_name = self._get_field_value("lastName", timeout)

        return {
            "FirstName": first_name,
            "MiddleName": middle_name,
            "LastName": last_name,
        }
        
       
        
        