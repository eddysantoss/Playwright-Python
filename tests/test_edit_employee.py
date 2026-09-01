def test_edit_employee(authenticated_pim_page):
    """
    Test: Edit existing employee

    Objective: Validate that an employee's details can be updated successfully.
    """
    pim_page = authenticated_pim_page
    
    # Cleanup: remove old employee if exists to ensure a clean state for the test  
    pim_page.search_employee(employee_partial_name="Boni Middle", employee_full_name="Boni Middle")
    pim_page.delete_employee()
    assert pim_page.is_employee_deleted_successfully(timeout=15000)
    
    # Add a new employee to edit
    pim_page.add_employee("Boni", "Middle", "Santos")
    assert pim_page.is_employee_added_successfully(timeout=15000)

    # Action: edit the newly added employee's details
    pim_page.edit_employee("Boni Middle", new_last_name="Silva")

    # Validation: verify that the details were updated
    updated_employee = pim_page.get_employee_details("Boni Middle")
    assert updated_employee["LastName"] == "Silva"
    