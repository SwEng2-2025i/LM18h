# Integration Test Lab
**Author:** Melissa Forero Narváez

## Overview

This project demonstrates integration and end-to-end testing for a microservices-based system using Flask, Selenium, and Python. The system includes:

**Users Service** (Port 5001)  
- `POST /users` — Create a new user  
- `GET /users` — List all users  
- `GET /users/<id>` — Get user by ID  
- `DELETE /users/<id>` — Delete user by ID *(Added for automated cleanup)*

**Tasks Service** (Port 5002)  
- `POST /tasks` — Create a new task  
- `GET /tasks` — List all tasks  
- `DELETE /tasks/<id>` — Delete task by ID *(Added for automated cleanup)*

**Frontend** (Port 5000)  
- Web interface to create users and tasks  
- Displays the list of tasks  

## Test Automation Features

### 1. Data Cleanup

- **What was added?**
  - After each test run, all data (users and tasks) created by the test is deleted using the corresponding API endpoints.
  - The tests verify that the data was actually deleted by checking the API responses and, in the frontend test, by ensuring the deleted task no longer appears in the UI.

- **Where?**
  - In `BackEnd-Test.py` and `FrontEnd-Test.py`, the following sections were added:
    - Functions for deleting and verifying deletion: `delete_user`, `delete_task`, `verificar_usuario_eliminado`, `verificar_tarea_eliminada`.
    - Cleanup and verification logic at the end of each test (`integration_test` and `main` functions), ensuring only data created by the test is deleted and its removal is verified.
  - **In `Users_Service/main.py` and `Task_Service/main.py`:**
    - Added new `DELETE` endpoints to allow deletion of users and tasks, respectively. This enables automated cleanup from the test scripts.

### 2. Automatic PDF Report Generation

- **What was added?**
  - After each test run, a PDF report is generated automatically, summarizing the test steps and results.
  - Each report is saved with a sequential number and stored in a `test_reports` folder inside the `Test` directory. Previous reports are preserved and never overwritten.
  - The PDF includes a title, timestamp, and all relevant test logs.

- **Where?**
  - The function `generate_pdf_report` was added in `pdf_report.py` and is called in the `finally` block of both `BackEnd-Test.py` and `FrontEnd-Test.py`.

## How to Run

1. Start all services (`Users_Service`, `Task_Service`, `Front-End`).
2. Run the backend or frontend test:
3. After each run, check the `test_reports` folder inside `Test` for the generated PDF report.

## Summary of Results

- All test data is properly cleaned up after each run.
- PDF reports are generated automatically and stored sequentially.
- Reports include detailed information about created and deleted users and tasks.

---