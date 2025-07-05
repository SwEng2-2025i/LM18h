#!/usr/bin/env python3
"""
Test Runner Script
Executes all tests in the correct order and provides a summary
"""

import subprocess
import sys
import time
import os
from datetime import datetime

def check_services():
    """Check if all required services are running"""
    import requests
    
    services = [
        ("Frontend", "http://localhost:5000"),
        ("Users Service", "http://localhost:5001/users"),
        ("Task Service", "http://localhost:5002/tasks")
    ]
    
    print("🔍 Checking services...")
    
    for service_name, url in services:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code in [200, 405]:  # 405 is OK for some endpoints
                print(f"✅ {service_name} is running")
            else:
                print(f"❌ {service_name} returned status {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ {service_name} is not responding: {e}")
            return False
    
    return True

def run_test(test_file, test_name):
    """Run a single test file"""
    print(f"\n{'='*60}")
    print(f"🚀 Running {test_name}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(
            [sys.executable, test_file], 
            capture_output=True, 
            text=True, 
            timeout=300  # 5 minutes timeout
        )
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        if result.returncode == 0:
            print(f"✅ {test_name} completed successfully")
            return True
        else:
            print(f"❌ {test_name} failed with return code {result.returncode}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"❌ {test_name} timed out")
        return False
    except Exception as e:
        print(f"❌ {test_name} failed with error: {e}")
        return False

def count_reports():
    """Count the number of PDF reports generated"""
    report_dir = "test_reports"
    if not os.path.exists(report_dir):
        return 0
    
    pdf_files = [f for f in os.listdir(report_dir) if f.endswith('.pdf')]
    return len(pdf_files)

def main():
    """Main test runner function"""
    print("🔧 Integration Test Runner")
    print("=" * 60)
    print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check if services are running
    if not check_services():
        print("\n❌ Not all services are running!")
        print("Please start the services first:")
        print("1. cd Users_Service && python main.py")
        print("2. cd Task_Service && python main.py") 
        print("3. cd Front-End && python main.py")
        return False
    
    # Count initial reports
    initial_reports = count_reports()
    print(f"\n📊 Initial PDF reports: {initial_reports}")
    
    # Run tests
    tests = [
        ("Test/BackEnd-Test.py", "Backend Integration Tests"),
        ("Test/FrontEnd-Test.py", "Frontend E2E Tests")
    ]
    
    results = {}
    
    for test_file, test_name in tests:
        if os.path.exists(test_file):
            success = run_test(test_file, test_name)
            results[test_name] = success
            time.sleep(2)  # Brief pause between tests
        else:
            print(f"❌ Test file not found: {test_file}")
            results[test_name] = False
    
    # Final summary
    print("\n" + "=" * 60)
    print("📋 TEST EXECUTION SUMMARY")
    print("=" * 60)
    
    total_tests = len(results)
    passed_tests = sum(1 for success in results.values() if success)
    failed_tests = total_tests - passed_tests
    
    print(f"📊 Total Tests: {total_tests}")
    print(f"✅ Passed: {passed_tests}")
    print(f"❌ Failed: {failed_tests}")
    print(f"📈 Success Rate: {(passed_tests/total_tests*100):.1f}%")
    
    print("\n📋 Individual Results:")
    for test_name, success in results.items():
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"  {test_name}: {status}")
    
    # Count final reports
    final_reports = count_reports()
    new_reports = final_reports - initial_reports
    print(f"\n📄 PDF reports generated: {new_reports}")
    print(f"📄 Total PDF reports: {final_reports}")
    
    if new_reports > 0:
        print(f"📁 Reports location: test_reports/")
    
    print(f"\n🏁 Execution completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Return success if all tests passed
    return passed_tests == total_tests

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
