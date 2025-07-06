# Lab 2: Integration Testing with Cleanup and Reporting

This document outlines the modifications made to the base project to meet the requirements for Lab 2. The two primary features implemented are:

1. **Test Data Cleanup:** Ensuring that all data generated during test execution is deleted afterward.
2. **Automatic PDF Report Generation:** Automatically saving the results of each test run into a unique, sequential PDF file.

---

## 1. Data Cleanup Implementation

To enable the deletion of test data, changes were made to both the backend services and the test scripts.

### Backend Service Modifications

New `DELETE` endpoints were added to the user and task services to allow for the removal of specific records by their ID.

- **`Users_Service/main.py`**:
  - A `DELETE /users/<int:user_id>` route was added.
  - This route finds a user by their `id`, removes them from the database (`db.session.delete(user)`), and confirms the operation.

- **`Task_Service/main.py`**:
  - Similarly, a `DELETE /tasks/<int:task_id>` route was added to allow for the deletion of a specific task.
  - A `GET /tasks/<int:task_id>` route was also added to allow for verification, completing the API.

### Test Script Modifications

Both test scripts (`Test/BackEnd-Test.py` and `Test/FrontEnd-Test.py`) were restructured to ensure reliable cleanup.

- **Use of `try...finally`**: The main test logic is encapsulated in a `try` block. The cleanup logic is placed in a `finally` block, guaranteeing its execution even if a test assertion fails.

- **Deletion Verification**: After sending a `DELETE` request, the script performs a `GET` request for the same resource. It then asserts that it receives a `404 Not Found` status code, which confirms that the record has been successfully deleted.

---

## 2. Automatic PDF Report Generation

The `reportlab` library was used to implement this feature.

### Dependencies

- `reportlab` was added to the `requirements.txt` file.

### Reporting Logic

This logic was implemented in both `Test/BackEnd-Test.py` and `Test/FrontEnd-Test.py`.

- **Activity Logging**: During test execution, each step (creation, verification, cleanup) and its outcome (success or failure) is recorded into a list of strings called `logs`.

- **Sequential File Naming**:
  - A function `get_next_report_filename()` was created.
  - This function scans the `Test/reports` directory, finds all existing reports (e.g., `Backend_Test_Report_1.pdf`, `Backend_Test_Report_2.pdf`), determines the highest number, and returns the name for the new report (e.g., `Backend_Test_Report_3.pdf`). This prevents overwriting previous reports.

- **PDF Creation**:
  - A `generate_pdf_report()` function takes the list of `logs` and the filename as input.
  - It uses `reportlab` to create a PDF document containing a title, the execution timestamp, and the formatted content of the logs.
  - This function is called within the `finally` block to ensure a report is always generated.

---

## Prerequisites

- **Python 3.7+** installed
- **Chrome browser** (for Selenium frontend tests)
- **Chrome WebDriver** (automatically managed by Selenium)
- **Network ports 5001, 5002, 5003** available

## Important Notes

1. **Data Cleanup**: All test data is automatically cleaned up after each test run, including verification that the data was properly deleted.

2. **PDF Reports**: Each test execution generates a unique PDF report with sequential numbering. Reports are never overwritten.

3. **Service Dependencies**: The Task Service validates user IDs against the Users Service before creating tasks.

4. **Frontend Testing**: Uses Selenium WebDriver in headless mode for automated browser testing.

5. **Error Handling**: Comprehensive error handling and logging throughout all components.

---

## How to Run the Project

### Option 1: Using Helper Scripts (Recommended)

**For Windows:**
```bash
# Start all services and run tests automatically
start_services.bat

# Or run tests only (services must be running)
run_tests.bat
```

**For Linux/Mac:**
```bash
# Make scripts executable first
chmod +x start_services.sh run_tests.sh

# Start all services and run tests automatically
./start_services.sh

# Or run tests only (services must be running)
./run_tests.sh
```

### Option 2: Manual Setup

1. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Start the services (in separate terminals):**

   ```bash
   python Users_Service/main.py
   ```

   ```bash
   python Task_Service/main.py
   ```

   ```bash
   python Front-End/main.py
   ```

3. **Run the tests (in another terminal):**

   ```bash
   # To run the backend integration test
   python Test/BackEnd-Test.py

   # To run the frontend E2E test
   python Test/FrontEnd-Test.py
   ```

4. **Verify the Results:**
   - Check the terminal output for success messages and the cleanup logs.
   - Navigate to the `Test/reports` directory to find the generated PDF reports, each with a unique sequential number.

---

## Code Sections Added

### Backend Services

- Added DELETE endpoints in both Users_Service and Task_Service
- Added GET endpoint for individual tasks in Task_Service for verification

### Test Scripts

- Implemented try...finally blocks for guaranteed cleanup execution
- Added logging system to track all test steps
- Added PDF report generation with sequential numbering
- Added deletion verification for all created resources

### Additional Dependencies

- Added reportlab for PDF generation
- Added selenium for frontend testing
- All dependencies managed through requirements.txt
