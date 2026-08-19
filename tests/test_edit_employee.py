def test_edit_employee(authenticated_pim_page):
    """
    Test: Edit existing employee

    Objective: Validate that an employee's details can be updated successfully.
    """
    pim_page = authenticated_pim_page

    # Add a new employee to edit
    pim_page.add_employee("Boni", "Middle", "Santos")
    assert pim_page.is_employee_added_successfully()

    # Action: edit the newly added employee's details
    pim_page.edit_employee("Boni Middle", new_last_name="Silva")

    # Validation: verify that the details were updated
    updated_employee = pim_page.get_employee_details("Boni Middle")
    assert updated_employee["LastName"] == "Silva"
    