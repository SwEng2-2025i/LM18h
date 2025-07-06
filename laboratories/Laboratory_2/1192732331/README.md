# Laboratory 2 - Integration Testing with Data Cleanup and PDF Reporting

## Student Information
- **Student ID**: 119273233
- **Lab**: Laboratory 2 - Integration Testing Extensions
- **Course**: Software Engineering II

## Overview
This laboratory extends the original integration testing example by implementing two major features:
1. **Data Cleanup**: Automatic deletion and verification of test data for both Backend and Frontend tests
2. **PDF Report Generation**: Automatic generation of sequential PDF reports with comprehensive test results

## Implemented Features

### 1. Data Cleanup System
- **Automatic Data Tracking**: Both test suites now track all created users and tasks during test execution
- **Comprehensive Cleanup**: All test data is automatically deleted after test completion
- **Verification Process**: System verifies that all test data has been properly deleted
- **API Integration**: Frontend tests use API calls to clean up data created through the web interface

### 2. PDF Report Generation
- **Sequential Numbering**: Reports are automatically numbered sequentially (001, 002, 003, etc.)
- **No Overwriting**: Previous reports are preserved, new reports get the next available number
- **Comprehensive Content**: Reports include test results, timestamps, configuration details, and summaries
- **Separate Reports**: Backend and Frontend tests generate their own report series

## Code Sections Added

### Backend Service Extensions

#### Users Service (`Users_Service/main.py`)
Added DELETE endpoints for data cleanup:

```python
@service_a.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a specific user by ID"""
    
@service_a.route('/users', methods=['DELETE'])
def delete_all_users():
    """Delete all users - used for test cleanup"""
```

#### Tasks Service (`Task_Service/main.py`)
Added DELETE endpoints for data cleanup:

```python
@service_b.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a specific task by ID"""
    
@service_b.route('/tasks', methods=['DELETE'])
def delete_all_tasks():
    """Delete all tasks - used for test cleanup"""
    
@service_b.route('/tasks/user/<int:user_id>', methods=['DELETE'])
def delete_tasks_by_user(user_id):
    """Delete all tasks for a specific user"""
```

### Test Suite Enhancements

#### Backend Test (`Test/BackEnd-Test.py`)
Added comprehensive test data management:

```python
class TestDataTracker:
    """Class to track test data for cleanup"""
    
def cleanup_test_data():
    """Clean up all test data and verify deletion"""
    
def verify_cleanup():
    """Verify that all test data has been properly deleted"""
    
def generate_pdf_report():
    """Generate a PDF report with test results"""
```

#### Frontend Test (`Test/FrontEnd-Test.py`)
Added frontend-specific cleanup and reporting:

```python
class FrontEndTestTracker:
    """Class to track frontend test data for cleanup"""
    
def cleanup_frontend_test_data():
    """Clean up all frontend test data and verify deletion"""
    
def generate_frontend_pdf_report():
    """Generate a PDF report with frontend test results"""
```

## Dependencies Updated

### Requirements (`requirements.txt`)
Added new dependencies for PDF generation and enhanced testing:

```
pip install flask flask_sqlalchemy requests selenium reportlab flask-cors
```

**New Dependencies:**
- `selenium`: For web browser automation in frontend tests
- `reportlab`: For PDF generation functionality
- `flask-cors`: For Cross-Origin Resource Sharing support

## Test Execution Flow

### Backend Test Flow
1. **Test Execution**: Create user, create task, verify association
2. **Data Tracking**: Track all created entities with TestDataTracker
3. **Data Cleanup**: Delete all tracked users and tasks via API
4. **Verification**: Confirm all test data has been deleted
5. **PDF Generation**: Generate numbered report with results

### Frontend Test Flow
1. **Browser Setup**: Initialize Chrome WebDriver
2. **Test Execution**: Navigate to frontend, create user, create task, verify display
3. **Data Tracking**: Track all created entities with FrontEndTestTracker
4. **Data Cleanup**: Delete all tracked data via API calls
5. **Verification**: Confirm all test data has been deleted
6. **PDF Generation**: Generate numbered report with results
7. **Browser Cleanup**: Close WebDriver

## Key Features Implemented

### Data Cleanup Features
- ✅ **Automatic Tracking**: All test data is tracked during creation
- ✅ **Complete Deletion**: Both users and tasks are deleted after tests
- ✅ **Verification Process**: System confirms successful deletion
- ✅ **Error Handling**: Robust error handling for cleanup operations
- ✅ **Cross-Service Cleanup**: Frontend tests clean up via API calls

### PDF Report Features
- ✅ **Sequential Numbering**: Reports numbered automatically (001, 002, 003...)
- ✅ **No Overwriting**: Previous reports are preserved
- ✅ **Comprehensive Content**: Test results, timestamps, configuration
- ✅ **Separate Series**: Backend and Frontend reports have separate numbering
- ✅ **Professional Layout**: Clean, readable PDF format

## Directory Structure

```
119273233/
├── Users_Service/
│   └── main.py (Enhanced with DELETE endpoints)
├── Task_Service/
│   └── main.py (Enhanced with DELETE endpoints)
├── Test/
│   ├── BackEnd-Test.py (Enhanced with cleanup and PDF generation)
│   ├── FrontEnd-Test.py (Enhanced with cleanup and PDF generation)
│   └── __pycache__/
├── Front-End/
├── reports/ (Generated during test execution)
│   ├── backend_test_report_001.pdf
│   ├── backend_test_report_002.pdf
│   ├── frontend_test_report_001.pdf
│   └── frontend_test_report_002.pdf
├── requirements.txt (Updated with new dependencies)
└── README.md (This file)
```

## Results Summary

### Implementation Status
- ✅ **Data Cleanup**: Fully implemented for both Backend and Frontend
- ✅ **PDF Report Generation**: Fully implemented with sequential numbering
- ✅ **Service Extensions**: DELETE endpoints added to both services
- ✅ **Test Enhancements**: Both test suites enhanced with new functionality
- ✅ **Dependency Management**: Requirements updated with new packages

### Test Coverage
- **Backend Tests**: User creation, task creation, data association, cleanup, verification
- **Frontend Tests**: UI interaction, user creation, task creation, data display, cleanup, verification
- **Integration**: Cross-service data cleanup and verification
- **Reporting**: Comprehensive PDF generation for both test suites

### Quality Assurance
- **Error Handling**: Robust error handling throughout all new code
- **Verification**: Multi-step verification ensures data cleanup success
- **Documentation**: Comprehensive code documentation and comments
- **Logging**: Detailed console output for debugging and monitoring

## Usage Instructions

1. **Install Dependencies**:
   ```bash
   pip install flask flask_sqlalchemy requests selenium reportlab flask-cors
   ```

2. **Start Services**:
   ```bash
   # Terminal 1: Start Users Service
   python Users_Service/main.py
   
   # Terminal 2: Start Tasks Service
   python Task_Service/main.py
   
   # Terminal 3: Start Frontend (if testing frontend)
   python Front-End/main.py
   ```

3. **Run Tests**:
   ```bash
   # Backend Test
   python Test/BackEnd-Test.py
   
   # Frontend Test (requires Chrome browser)
   python Test/FrontEnd-Test.py
   ```

4. **Check Results**:
   - Console output shows test execution details
   - PDF reports are generated in the `reports/` directory
   - Each execution creates a new sequentially numbered report

## Conclusion

This laboratory successfully implements both required features:
1. **Complete data cleanup** with verification for both Backend and Frontend tests
2. **Automatic PDF report generation** with sequential numbering and comprehensive content

The implementation maintains the original functionality while adding robust data management and reporting capabilities, making the test suite more professional and production-ready. 