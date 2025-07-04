# Integration Testing Example

This project demonstrates integration testing between multiple microservices and a frontend application, with enhanced features for data cleanup and automated PDF report generation.

## Project Structure

```
Example 5 - Integration Test/
├── Front-End/          # Frontend application (Flask web app)
├── Users_Service/      # User management microservice
├── Task_Service/       # Task management microservice
├── Test/              # Integration test files
├── requirements.txt   # Python dependencies
└── README.md         # This file
```

## Services

### Users Service (Port 5001)
- **POST** `/users` - Create a new user
- **GET** `/users` - List all users
- **GET** `/users/<id>` - Get user by ID
- **DELETE** `/users/<id>` - Delete user by ID *(Added)*

### Task Service (Port 5002)
- **POST** `/tasks` - Create a new task
- **GET** `/tasks` - List all tasks
- **DELETE** `/tasks/<id>` - Delete task by ID *(Added)*

### Frontend (Port 5000)
- Web interface for creating users and tasks
- Displays task list

## Test Files

### BackEnd-Test.py
Integration test for backend services that:
1. Creates a user
2. Creates a task for that user
3. Verifies the task is properly linked to the user
4. **Deletes the created task and user** *(Added)*
5. **Verifies that both user and task are properly deleted** *(Added)*
6. **Generates a PDF report with test results** *(Added)*

### FrontEnd-Test.py
End-to-end test using Selenium that:
1. Opens the frontend application
2. Creates a user through the web interface
3. Creates a task for that user
4. Verifies the task appears in the task list
5. **Deletes the created user and task via API calls** *(Added)*
6. **Verifies deletion through API verification** *(Added)*
7. **Generates a PDF report with test results** *(Added)*

## New Features Added

### 1. Data Cleanup
- **DELETE endpoints** added to both Users_Service and Task_Service
- **Automatic cleanup** after test execution in both test files
- **Verification** that test data is properly deleted
- Ensures tests don't leave residual data in the system

### 2. PDF Report Generation
- **Automatic PDF generation** after each test run
- **Sequential numbering** (report_1.pdf, report_2.pdf, etc.)
- **Preservation of previous reports** - no overwriting
- Reports include:
  - Test results (pass/fail)
  - Created user and task IDs
  - Cleanup verification status
  - Timestamp information

## Code Changes Summary

### Backend Services
- **Users_Service/main.py**: Added DELETE endpoint for user deletion
- **Task_Service/main.py**: Added DELETE endpoint for task deletion

### Test Files
- **Test/BackEnd-Test.py**: 
  - Added cleanup functions (`delete_user`, `delete_task`)
  - Added verification logic for data deletion
  - Added PDF report generation with sequential numbering
- **Test/FrontEnd-Test.py**:
  - Added cleanup functions using API calls
  - Added verification logic for data deletion
  - Added PDF report generation with sequential numbering

### Dependencies
- **requirements.txt**: Added `fpdf` package for PDF generation

## Running the Tests

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Start the services:
   ```bash
   # Terminal 1
   cd Users_Service
   python main.py
   
   # Terminal 2
   cd Task_Service
   python main.py
   
   # Terminal 3
   cd Front-End
   python main.py
   ```

3. Run the tests:
   ```bash
   # Backend integration test
   cd Test
   python BackEnd-Test.py
   
   # Frontend E2E test
   python FrontEnd-Test.py
   ```

## Test Results

After running the tests, you will find:
- Console output showing test execution and results
- PDF reports in the `Test/` directory (e.g., `Frontend-report_1.pdf`, `Frontend-report_2.pdf`)
- Clean system state with no residual test data

## Benefits

1. **Data Integrity**: Tests clean up after themselves, preventing data pollution
2. **Reproducibility**: Each test run starts with a clean state
3. **Documentation**: PDF reports provide permanent records of test execution
4. **Traceability**: Sequential numbering allows tracking of test history
5. **Reliability**: Verification ensures cleanup actually worked

This enhanced integration testing framework provides a robust foundation for testing microservice architectures with proper data management and comprehensive reporting. 