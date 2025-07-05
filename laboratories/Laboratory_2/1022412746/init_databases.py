#!/usr/bin/env python3
"""
Manual Database Initialization Script
This script creates the databases without starting the full services
"""

import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def init_users_db():
    """Initialize Users Service Database"""
    print("🔧 Initializing Users Service Database...")
    
    # Change to Users_Service directory
    users_dir = project_root / "Users_Service"
    os.chdir(users_dir)
    
    # Import and configure the Flask app
    from main import service_a, db
    
    # Create database tables
    with service_a.app_context():
        db.create_all()
        print("✅ Users database created successfully!")
        
        # Check if database file exists
        db_path = users_dir / "instance" / "users.db"
        if db_path.exists():
            print(f"📁 Database file: {db_path}")
        else:
            print("⚠️  Database file not found!")

def init_tasks_db():
    """Initialize Tasks Service Database"""
    print("\n🔧 Initializing Tasks Service Database...")
    
    # Change to Task_Service directory
    tasks_dir = project_root / "Task_Service"
    os.chdir(tasks_dir)
    
    # Import and configure the Flask app
    from main import service_b, db
    
    # Create database tables
    with service_b.app_context():
        db.create_all()
        print("✅ Tasks database created successfully!")
        
        # Check if database file exists
        db_path = tasks_dir / "instance" / "tasks.db"
        if db_path.exists():
            print(f"📁 Database file: {db_path}")
        else:
            print("⚠️  Database file not found!")

def main():
    """Main function to initialize all databases"""
    print("🚀 Manual Database Initialization")
    print("=" * 50)
    
    try:
        # Initialize Users DB
        init_users_db()
        
        # Initialize Tasks DB
        init_tasks_db()
        
        print("\n" + "=" * 50)
        print("🎉 All databases initialized successfully!")
        print("\nYou can now start the services:")
        print("1. cd Users_Service && python main.py")
        print("2. cd Task_Service && python main.py")
        print("3. cd Front-End && python main.py")
        
    except Exception as e:
        print(f"\n❌ Error during initialization: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
