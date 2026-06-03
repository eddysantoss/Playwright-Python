from playwright.sync_api import Page, expect

class PimPage:
    def __init__(self, page: Page):
        self.page = page
        self.pim_page = page.get_by_role("link", name="PIM")
        self.add_employee_button = page.get_by_role("link", name="Add Employee")
        self.first_name_input = page.get_by_role("textbox", name="First Name")
        self.middle_name_input = page.get_by_role("textbox", name="Middle Name")    
        self.last_name_input = page.get_by_role("textbox", name="Last Name")
        self.save_button = page.get_by_role("button", name="Save")
                
    def wait_for_PIM_page_loaded(self, timeout: float = 5000) -> bool:
        expect(self.page.get_by_text("PIM", exact=True)).to_be_visible(timeout=timeout)
        return True

    def add_employee(self, first_name: str, middle_name: str, last_name: str, timeout: float = 5000):
      
        # 1. Wait until the PIM link is visible and clickable.
        expect(self.pim_page).to_be_visible(timeout=timeout)
        expect(self.pim_page).to_be_enabled(timeout=timeout)
        self.pim_page.click()
        
        # 2. After clicking on PIM, wait for the "Add Employee" button to appear
        expect(self.add_employee_button).to_be_visible(timeout=timeout)
        expect(self.add_employee_button).to_be_enabled(timeout=timeout)
        self.add_employee_button.click()
        
        # 3. Wait for the input fields to appear (indicator that the form has loaded)
        expect(self.first_name_input).to_be_visible(timeout=timeout)
        expect(self.first_name_input).to_be_enabled(timeout=timeout)
        
        # 4. Fill the name fields
        self.first_name_input.fill(first_name)
        
        expect(self.middle_name_input).to_be_visible(timeout=timeout)
        expect(self.middle_name_input).to_be_enabled(timeout=timeout)
        self.middle_name_input.fill(middle_name)
        
        expect(self.last_name_input).to_be_visible(timeout=timeout)
        expect(self.last_name_input).to_be_enabled(timeout=timeout)
        self.last_name_input.fill(last_name)
        
        # 5. Wait for the Save button to be clickable before clicking
        expect(self.save_button).to_be_visible(timeout=timeout)
        expect(self.save_button).to_be_enabled(timeout=timeout)
        self.save_button.click()
        
    def is_employee_added_successfully(self, timeout: float = 5000) -> bool:
        expect(self.page.get_by_text("Success", exact=True)).to_be_visible(timeout=timeout)
        return True
        
        

  
        
        