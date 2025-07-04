
===============================================================
INTEGRATION TESTING - DATA CLEANUP IMPLEMENTATION
===============================================================

This document outlines the changes made to support automatic
creation and deletion of test data during integration testing.
The objective is to ensure that any data added by tests is
cleaned up afterward, and its deletion is verified.

---------------------------------------------------------------
✅ Code Added:
---------------------------------------------------------------

1. File: task_service/main.py

A new route was added to allow deletion of tasks by ID:

@service_b.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'No se encuentra el task'}), 404
    db.session.delete(task)
    db.session.commit()
    return '', 204

2. File: Users_Service/main.py

A new route was added to allow deletion of users by ID:

@service_a.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return '', 204

3. File: Test/BackEnd-Test.py

- New functions delete_user() and delete_task() were added.
- The integration_test() function was adapted to:
  - Create user and task via the API.
  - Verify user-task association.
  - Delete the created data at the end.
  - Verify that the data has been successfully removed.
  - Collect test results and send them to a PDF report.

4. File: Test/FrontEnd-Test.py

- Two global variables were added to store the user ID and task ID created during the test.
- The following functions were implemented:
  - delete_user(): Deletes a user via the API.
  - delete_task(): Deletes a task via the API.
  - verify_delete(): Confirms that a task no longer appears in the task list.
- The main() function was adapted to:
  - Track the user and task created via the UI.
  - Delete them at the end of the test.
  - Verify that deletion was successful.
  - Store the test result and generate a report.

5. File: pdf_report.py

- This new file manages the generation of PDF reports
  from the results collected during the backend and frontend tests.
  It serves as a centralized report builder for quality assurance
  and documentation.

---------------------------------------------------------------
🧪 Results:
---------------------------------------------------------------

Both the Backend and Frontend integration tests passed successfully.
The test results confirm that:
- Users and tasks were created correctly.
- The created data was deleted after the test finished.
- The system was left in a clean state.

This ensures safe, repeatable automated testing without leaving residual data.
