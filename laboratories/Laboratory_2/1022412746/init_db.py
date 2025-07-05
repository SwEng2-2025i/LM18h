#!/usr/bin/env python3
"""
Database Initialization Script
This script ensures that the database structure is properly set up
"""

import os
import sys
import sqlite3
import subprocess
import time
from pathlib import Path

def create_database_structure():
    """Create database structure for both services"""
    print("🔧 Initializing database structure...")
    
    # Get the base directory
    base_dir = Path(__file__).parent
    
    # Initialize Users Service Database
    users_instance_dir = base_dir / "Users_Service" / "instance"
    users_instance_dir.mkdir(exist_ok=True)
    users_db_path = users_instance_dir / "users.db"
    
    print(f"📁 Users Service instance directory: {users_instance_dir}")
    print(f"💾 Users database path: {users_db_path}")
    
    # Initialize Task Service Database
    tasks_instance_dir = base_dir / "Task_Service" / "instance"
    tasks_instance_dir.mkdir(exist_ok=True)
    tasks_db_path = tasks_instance_dir / "tasks.db"
    
    print(f"📁 Task Service instance directory: {tasks_instance_dir}")
    print(f"💾 Tasks database path: {tasks_db_path}")
    
    # Create test reports directory
    test_reports_dir = base_dir / "test_reports"
    test_reports_dir.mkdir(exist_ok=True)
    print(f"📁 Test reports directory: {test_reports_dir}")
    
    print("✅ Database structure initialized successfully!")

def initialize_databases_by_starting_services():
    """Initialize databases by briefly starting each service"""
    print("\n🚀 Initializing databases by starting services...")
    
    base_dir = Path(__file__).parent
    
    # Initialize Users Service Database
    print("🔧 Starting Users Service to create database...")
    try:
        users_process = subprocess.Popen(
            [sys.executable, "main.py"],
            cwd=base_dir / "Users_Service",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait for the service to start and create the database
        time.sleep(3)
        
        # Terminate the process
        users_process.terminate()
        users_process.wait(timeout=5)
        
        # Check if database was created
        users_db_path = base_dir / "Users_Service" / "instance" / "users.db"
        if users_db_path.exists():
            print("✅ Users database created successfully!")
        else:
            print("⚠️  Users database not found!")
            
    except Exception as e:
        print(f"❌ Error initializing Users database: {e}")
    
    # Initialize Tasks Service Database
    print("🔧 Starting Tasks Service to create database...")
    try:
        tasks_process = subprocess.Popen(
            [sys.executable, "main.py"],
            cwd=base_dir / "Task_Service",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait for the service to start and create the database
        time.sleep(3)
        
        # Terminate the process
        tasks_process.terminate()
        tasks_process.wait(timeout=5)
        
        # Check if database was created
        tasks_db_path = base_dir / "Task_Service" / "instance" / "tasks.db"
        if tasks_db_path.exists():
            print("✅ Tasks database created successfully!")
        else:
            print("⚠️  Tasks database not found!")
            
    except Exception as e:
        print(f"❌ Error initializing Tasks database: {e}")

def create_databases_manually():
    """Create databases manually using SQLite"""
    print("\n🔧 Creating databases manually...")
    
    base_dir = Path(__file__).parent
    
    # Create Users database
    users_db_path = base_dir / "Users_Service" / "instance" / "users.db"
    try:
        conn = sqlite3.connect(users_db_path)
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY,
                name VARCHAR(100) NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
        print(f"✅ Users database created manually: {users_db_path}")
        
    except Exception as e:
        print(f"❌ Error creating Users database: {e}")
    
    # Create Tasks database
    tasks_db_path = base_dir / "Task_Service" / "instance" / "tasks.db"
    try:
        conn = sqlite3.connect(tasks_db_path)
        cursor = conn.cursor()
        
        # Create tasks table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS task (
                id INTEGER PRIMARY KEY,
                title VARCHAR(100) NOT NULL,
                user_id INTEGER NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
        print(f"✅ Tasks database created manually: {tasks_db_path}")
        
    except Exception as e:
        print(f"❌ Error creating Tasks database: {e}")

def check_current_structure():
    """Check and display current project structure"""
    print("\n📋 Current Project Structure:")
    print("=" * 50)
    
    base_dir = Path(__file__).parent
    
    # Check main directories and files
    structure_items = [
        ("Front-End/", "📁"),
        ("Front-End/main.py", "📄"),
        ("Users_Service/", "📁"),
        ("Users_Service/main.py", "📄"),
        ("Users_Service/instance/", "📁"),
        ("Users_Service/instance/users.db", "💾"),
        ("Task_Service/", "📁"),
        ("Task_Service/main.py", "📄"),
        ("Task_Service/instance/", "📁"),
        ("Task_Service/instance/tasks.db", "💾"),
        ("Test/", "📁"),
        ("Test/BackEnd-Test.py", "📄"),
        ("Test/FrontEnd-Test.py", "📄"),
        ("Test/test_utils.py", "📄"),
        ("test_reports/", "📁"),
        ("requirements.txt", "📄"),
        ("setup.py", "📄"),
        ("README.md", "📄")
    ]
    
    for item_path, icon in structure_items:
        full_path = base_dir / item_path
        if full_path.exists():
            print(f"✅ {icon} {item_path}")
        else:
            print(f"❌ {icon} {item_path} (missing)")
    
    print("=" * 50)

def main():
    """Main function"""
    print("🚀 Database Initialization Script")
    print("=" * 50)
    
    # Step 1: Create directory structure
    create_database_structure()
    
    # Step 2: Try to initialize databases by starting services
    print("\n🎯 Choose initialization method:")
    print("1. Auto-initialize by starting services (recommended)")
    print("2. Manual database creation")
    print("3. Skip database creation")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        initialize_databases_by_starting_services()
    elif choice == "2":
        create_databases_manually()
    elif choice == "3":
        print("⏭️  Skipping database creation...")
    else:
        print("⚠️  Invalid choice, using manual creation...")
        create_databases_manually()
    
    # Step 3: Check current structure
    check_current_structure()
    
    print("\n" + "=" * 50)
    print("🎉 Initialization completed!")
    print("\nNext steps:")
    print("1. Start the services:")
    print("   - Terminal 1: cd Users_Service && python main.py")
    print("   - Terminal 2: cd Task_Service && python main.py")
    print("   - Terminal 3: cd Front-End && python main.py")
    print("2. Run the tests:")
    print("   - python Test/BackEnd-Test.py")
    print("   - python Test/FrontEnd-Test.py")
    print("   - python run_tests.py")

if __name__ == "__main__":
    main()
