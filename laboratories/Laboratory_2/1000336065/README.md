Of course! Here is the updated `README.md` file in English, detailing all the implemented features and including instructions for running the project.

---

# Lab 2: Integration Testing with Cleanup and Reporting

This document outlines the modifications made to the base project to meet the requirements for Lab 2. The two primary features implemented are:

1.  **Test Data Cleanup:** Ensuring that all data generated during test execution is deleted afterward.
2.  **Automatic PDF Report Generation:** Automatically saving the results of each test run into a unique, sequential PDF file.

---

## 1. Data Cleanup Implementation

To enable the deletion of test data, changes were made to both the backend services and the test scripts.

### Backend Service Modifications

New `DELETE` endpoints were added to the user and task services to allow for the removal of specific records by their ID.

-   **`Users_Service/main.py`**:
    -   A `DELETE /users/<int:user_id>` route was added.
    -   This route finds a user by their `id`, removes them from the database (`db.session.delete(user)`), and confirms the operation.

    ```python
    @service_a.route('/users/<int:user_id>', methods=['DELETE'])
    def delete_user(user_id):
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted'}), 200
    ```

-   **`Task_Service/main.py`**:
    -   Similarly, a `DELETE /tasks/<int:task_id>` route was added to allow for the deletion of a specific task.
    -   A `GET /tasks/<int:task_id>` route was also added to allow for verification, completing the API.

    ```python
    @service_b.route('/tasks/<int:task_id>', methods=['DELETE'])
    def delete_task(task_id):
        # ... logic to find and delete the task ...
    ```

### Test Script Modifications

Both test scripts (`Test/BackEnd-Test.py` and `Test/FrontEnd-Test.py`) were restructured to ensure reliable cleanup.

-   **Use of `try...finally`**: The main test logic is encapsulated in a `try` block. The cleanup logic is placed in a `finally` block, guaranteeing its execution even if a test assertion fails.

-   **Deletion Verification**: After sending a `DELETE` request, the script performs a `GET` request for the same resource. It then asserts that it receives a `404 Not Found` status code, which confirms that the record has been successfully deleted.

    ```python
    # Example from Test/BackEnd-Test.py
    finally:
        # ...
        if created_user_id:
            logs.append(f"CLEANUP: Deleting user ID {created_user_id}...")
            requests.delete(f"{USERS_URL}/{created_user_id}")
            
            # Verification step
            verify_resp = requests.get(f"{USERS_URL}/{created_user_id}")
            if verify_resp.status_code == 404:
                 logs.append("  -> VERIFIED: User no longer exists (404).")
    ```

---

## 2. Automatic PDF Report Generation

The `reportlab` library was used to implement this feature.

### Dependencies

-   `reportlab` was added to the `requirements.txt` file.

### Reporting Logic

This logic was implemented in both `Test/BackEnd-Test.py` and `Test/FrontEnd-Test.py`.

-   **Activity Logging**: During test execution, each step (creation, verification, cleanup) and its outcome (success or failure) is recorded into a list of strings called `logs`.

-   **Sequential File Naming**:
    -   A function `get_next_report_filename()` was created.
    -   This function scans the `Test/reports` directory, finds all existing reports (e.g., `Backend_Test_Report_1.pdf`, `Backend_Test_Report_2.pdf`), determines the highest number, and returns the name for the new report (e.g., `Backend_Test_Report_3.pdf`). This prevents overwriting previous reports.

-   **PDF Creation**:
    -   A `generate_pdf_report()` function takes the list of `logs` and the filename as input.
    -   It uses `reportlab` to create a PDF document containing a title, the execution timestamp, and the formatted content of the logs.
    -   This function is called within the `finally` block to ensure a report is always generated.

    ```python
    # Example function from the test scripts
    def generate_pdf_report(filename, logs, test_name):
        c = canvas.Canvas(filename, pagesize=letter)
        # ... Logic to draw the title, date, and logs onto the PDF ...
        c.save()
    ```

---

## How to Run the Project

1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Start the services (in separate terminals):**
    ```bash
    python3 Users_Service/main.py
    ```
    ```bash
    python3 Task_Service/main.py
    ```
    ```bash
    python3 Front-End/main.py
    ```

3.  **Run the tests (in another terminal):**
    ```bash
    # To run the backend integration test
    python3 Test/BackEnd-Test.py

    # To run the frontend E2E test
    python3 Test/FrontEnd-Test.py
    ```

4.  **Verify the Results:**
    -   Check the terminal output for success messages and the cleanup logs.
    -   Navigate to the `Test/reports` directory to find the generated PDF reports, each with a unique sequential number.