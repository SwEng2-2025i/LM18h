#!/usr/bin/env python3
"""
Project Verification Script
This script verifies that all components are working correctly
"""

import os
import sys
import time
import subprocess
import requests
from pathlib import Path

def check_python_packages():
    """Check if all required Python packages are installed"""
    print("📦 Checking Python packages...")
    
    required_packages = [
        'flask', 'flask_sqlalchemy', 'flask_cors', 
        'requests', 'reportlab', 'selenium'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} (missing)")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install " + " ".join(missing_packages))
        return False
    else:
        print("✅ All packages installed!")
        return True

def check_project_structure():
    """Check if project structure is correct"""
    print("\n📁 Checking project structure...")
    
    base_dir = Path(__file__).parent
    
    required_structure = {
        'Front-End/main.py': 'Frontend application',
        'Users_Service/main.py': 'Users microservice',
        'Users_Service/instance/': 'Users database directory',
        'Task_Service/main.py': 'Tasks microservice',
        'Task_Service/instance/': 'Tasks database directory',
        'Test/BackEnd-Test.py': 'Backend integration tests',
        'Test/FrontEnd-Test.py': 'Frontend E2E tests',
        'Test/test_utils.py': 'Test utilities',
        'test_reports/': 'PDF reports directory',
        'requirements.txt': 'Dependencies file',
        'setup.py': 'Setup script',
        'README.md': 'Documentation'
    }
    
    all_good = True
    
    for path, description in required_structure.items():
        full_path = base_dir / path
        if full_path.exists():
            print(f"✅ {path} - {description}")
        else:
            print(f"❌ {path} - {description} (missing)")
            all_good = False
    
    return all_good

def test_database_creation():
    """Test that databases can be created"""
    print("\n🗄️  Testing database creation...")
    
    base_dir = Path(__file__).parent
    
    # Test Users Service database creation
    users_db_path = base_dir / "Users_Service" / "instance" / "users.db"
    tasks_db_path = base_dir / "Task_Service" / "instance" / "tasks.db"
    
    # Remove existing databases for clean test
    if users_db_path.exists():
        users_db_path.unlink()
        print("🗑️  Removed existing users.db")
    
    if tasks_db_path.exists():
        tasks_db_path.unlink()
        print("🗑️  Removed existing tasks.db")
    
    # Start Users Service briefly to create database
    print("🚀 Starting Users Service to create database...")
    try:
        users_process = subprocess.Popen(
            [sys.executable, "Users_Service/main.py"],
            cwd=base_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait a bit for the service to start
        time.sleep(3)
        
        # Terminate the process
        users_process.terminate()
        users_process.wait()
        
        if users_db_path.exists():
            print("✅ Users database created successfully")
        else:
            print("❌ Users database not created")
            return False
            
    except Exception as e:
        print(f"❌ Error starting Users Service: {e}")
        return False
    
    # Start Task Service briefly to create database
    print("🚀 Starting Task Service to create database...")
    try:
        tasks_process = subprocess.Popen(
            [sys.executable, "Task_Service/main.py"],
            cwd=base_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait a bit for the service to start
        time.sleep(3)
        
        # Terminate the process
        tasks_process.terminate()
        tasks_process.wait()
        
        if tasks_db_path.exists():
            print("✅ Tasks database created successfully")
        else:
            print("❌ Tasks database not created")
            return False
            
    except Exception as e:
        print(f"❌ Error starting Task Service: {e}")
        return False
    
    return True

def main():
    """Main verification function"""
    print("🔍 Project Verification Script")
    print("=" * 50)
    
    # Check 1: Python packages
    packages_ok = check_python_packages()
    
    # Check 2: Project structure
    structure_ok = check_project_structure()
    
    # Check 3: Database creation
    db_ok = test_database_creation()
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 VERIFICATION SUMMARY")
    print("=" * 50)
    
    print(f"📦 Python Packages: {'✅ OK' if packages_ok else '❌ FAIL'}")
    print(f"📁 Project Structure: {'✅ OK' if structure_ok else '❌ FAIL'}")
    print(f"🗄️  Database Creation: {'✅ OK' if db_ok else '❌ FAIL'}")
    
    if packages_ok and structure_ok and db_ok:
        print("\n🎉 ALL CHECKS PASSED!")
        print("\nYour project is ready to use!")
        print("\nNext steps:")
        print("1. Start services in separate terminals:")
        print("   Terminal 1: cd Users_Service && python main.py")
        print("   Terminal 2: cd Task_Service && python main.py") 
        print("   Terminal 3: cd Front-End && python main.py")
        print("2. Run tests:")
        print("   python Test/BackEnd-Test.py")
        print("   python Test/FrontEnd-Test.py")
        return True
    else:
        print("\n❌ SOME CHECKS FAILED")
        print("Please fix the issues above before proceeding.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
