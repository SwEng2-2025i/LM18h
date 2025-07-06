# Lab 2: Integration Testing with Data Cleanup and PDF Reporting

**Student ID:** YOUR_STUDENT_ID  
**Submission Date:** July 5, 2025

## Overview
This project extends the initial integration testing example by implementing two key features:
1. **Automatic Data Cleanup**: All test data is deleted after test execution, with verification
2. **PDF Report Generation**: Test results are saved in sequentially numbered PDF reports

## Implemented Features

### 1. Data Cleanup
- ✅ Added DELETE endpoints to both services:
  - `DELETE /users/<id>` in Users Service
  - `DELETE /tasks/<id>` in Task Service
- ✅ Modified tests to delete all created data after execution
- ✅ Added verification steps to confirm data deletion
- ✅ Ensured cleanup works for both successful and failed test cases

### 2. PDF Report Generation
- ✅ Sequential PDF reports using `fpdf` library
- ✅ Reports include:
  - Test name and sequential number
  - Start/end timestamps and duration
  - Overall status (PASSED/FAILED)
  - Detailed step-by-step logs
- ✅ Reports saved in `Test/reports/` directory
- ✅ Unique numbered filenames (report_001.pdf, report_002.pdf)
- ✅ Previous reports are never overwritten

## Code Changes Summary

### Services
| Service | File | Changes |
|---------|------|---------|
| Users Service | `Users_Service/main.py` | Added DELETE endpoint |
| Task Service | `Task_Service/main.py` | Added DELETE and GET endpoints |

### Tests
| Test | File | Changes |
|------|------|---------|
| Backend Test | `Test/BackEnd-Test.py` | Added cleanup, verification, PDF reports |
| Frontend Test | `Test/FrontEnd-Test.py` | Improved synchronization, PDF reports |
| Test Logger | `Test/TestLogger.py` | New class for logging and PDF generation |

### Dependencies

> `flask`
>
> `flask_sqlalchemy`
>
> `requests`
>
> `selenium`
>
> `fpdf`

## How to Run the Tests

### 1. Install Dependencies

> `pip install -r requirements.txt`

### 2. Start Services

> `\# Terminal 1: Users Service (port 5001)`
> 
> `cd Users_Service && python main.py`
> 
> 
> `\# Terminal 2: Task Service (port 5002)`
>
> `cd ../Task_Service && python main.py`
> 
> `\# Terminal 3: Frontend (port 5000)`
>
> `cd ../Front-End && python main.py`

### 3. Run Tests

> `\# Backend test (service integration)`
> 
> `cd Test`
>
> `python BackEnd-Test.py`
>
>
> `\# Frontend test (browser interaction)`
> 
> `python FrontEnd-Test.py`

### 3. Run Tests
- Console output shows test execution details
- PDF reports: `Test/reports/` directory
- Screenshots on failure: `Test/` directory