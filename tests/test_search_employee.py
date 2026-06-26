from pages.pim_page import PimPage

# Test data 
first_name = "DeleteTest"
middle_name = "Middle Name"
last_name = "Last Name"
employee_full_name = f"{first_name} {middle_name} {last_name}"
employee_partial_name = f"{first_name} {middle_name}"

def test_search_employee(authenticated_pim_page):
    pim_page = authenticated_pim_page
   
    pim_page.add_employee(first_name, middle_name, last_name)
    assert pim_page.is_employee_added_successfully()
    
    # Search for an employee by name
    pim_page.search_employee(employee_full_name, employee_partial_name)
    
    # Verify that the employee appears in the search results
    pim_page.is_employee_in_results(employee_partial_name)
    
    # Delete the employee after verification to clean up
    assert pim_page.delete_employee()
    assert pim_page.is_employee_deleted_successfully()