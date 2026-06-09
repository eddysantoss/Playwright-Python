import pytest

@pytest.mark.parametrize("first_name, middle_name, last_name", [
    ("Boni", "Middle", "Santos"),
    ("John", "Doe", "Smith"),
    ("Jane", "A.", "Doe"),
    ("Boni", "Chique", "Santos")
    
])

def test_add_employee(authenticated_pim_page, first_name, middle_name, last_name):
    """
    Test: Add new employee

    Objective: Validate that an employee is successfully added 
    when all required fields are filled with valid data.
    """
    pim_page = authenticated_pim_page

    # Action: Add a new employee with valid data
    pim_page.add_employee(first_name, middle_name, last_name)
    assert pim_page.is_employee_added_successfully()
    
def test_validate_required_fields(authenticated_pim_page):
    """
    Test: Validate required fields

    Objective: Verify that the system displays error messages
    when attempting to add an employee with empty required fields.
    """
    pim_page = authenticated_pim_page
        
    # Action: Trying to add new employee without filling required fields
    pim_page.add_employee("", "", "")
    assert pim_page.get_error_messages()
       
  
    
 