import pytest

def test_delete_employee(authenticated_pim_page):
    """
    Test: Delete employee

    Objective: Validate that an employee record is successfully deleted 
    when the delete action is performed.
    
    """
    pim_page = authenticated_pim_page
    
    # Test data (fixed - multiple data sets tested in test_add_employee)
    first_name = "DeleteTest"
    middle_name = "Middle Name"
    last_name = "Last Name"
    employee_full_name = f"{first_name} {middle_name} {last_name}"
    employee_partial_name = f"{first_name} {middle_name}"
     

    # Step 1: Add a new employee
    pim_page.add_employee(first_name, middle_name, last_name)
    assert pim_page.is_employee_added_successfully()
    
    # Step 2: Search for the employee to ensure they exist and delete the correct one
    assert pim_page.search_employee(employee_full_name, employee_partial_name)
    assert pim_page.delete_employee()

    # Step 4: Verify deletion was successful
    assert pim_page.is_employee_deleted_successfully()
    