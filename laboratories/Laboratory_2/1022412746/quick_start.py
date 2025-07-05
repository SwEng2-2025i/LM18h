#!/usr/bin/env python3
"""
Quick Start Script
This script helps you get the project running quickly
"""

import os
import sys
import time
import subprocess
from pathlib import Path

def start_services():
    """Start all microservices"""
    print("🚀 Starting all microservices...")
    
    base_dir = Path(__file__).parent
    
    # Start Users Service
    print("🟢 Starting Users Service on port 5001...")
    users_process = subprocess.Popen(
        [sys.executable, "main.py"],
        cwd=base_dir / "Users_Service",
        creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0
    )
    
    time.sleep(2)
    
    # Start Task Service
    print("🟢 Starting Task Service on port 5002...")
    tasks_process = subprocess.Popen(
        [sys.executable, "main.py"],
        cwd=base_dir / "Task_Service",
        creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0
    )
    
    time.sleep(2)
    
    # Start Frontend
    print("🟢 Starting Frontend on port 5000...")
    frontend_process = subprocess.Popen(
        [sys.executable, "main.py"],
        cwd=base_dir / "Front-End",
        creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0
    )
    
    print("\n✅ All services started!")
    print("🌐 Frontend: http://localhost:5000")
    print("👥 Users API: http://localhost:5001/users")
    print("📝 Tasks API: http://localhost:5002/tasks")
    
    return users_process, tasks_process, frontend_process

def run_tests():
    """Run all tests"""
    print("\n🧪 Running tests...")
    
    base_dir = Path(__file__).parent
    
    # Wait for services to be ready
    print("⏳ Waiting for services to be ready...")
    time.sleep(5)
    
    # Run backend tests
    print("🔧 Running Backend Integration Tests...")
    result = subprocess.run(
        [sys.executable, "Test/BackEnd-Test.py"],
        cwd=base_dir,
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("✅ Backend tests passed!")
    else:
        print("❌ Backend tests failed!")
        print(result.stdout)
        print(result.stderr)
    
    time.sleep(2)
    
    # Run frontend tests
    print("🌐 Running Frontend E2E Tests...")
    result = subprocess.run(
        [sys.executable, "Test/FrontEnd-Test.py"],
        cwd=base_dir,
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("✅ Frontend tests passed!")
    else:
        print("❌ Frontend tests failed!")
        print(result.stdout)
        print(result.stderr)

def main():
    """Main function"""
    print("🚀 Quick Start Script")
    print("=" * 50)
    
    choice = input("What would you like to do?\n1. Start services only\n2. Start services and run tests\n3. Just run tests\nEnter choice (1-3): ")
    
    if choice == "1":
        start_services()
        input("\nPress Enter to exit...")
    elif choice == "2":
        processes = start_services()
        run_tests()
        input("\nPress Enter to exit...")
    elif choice == "3":
        run_tests()
    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    main()
