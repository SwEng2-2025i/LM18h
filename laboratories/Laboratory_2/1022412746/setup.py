#!/usr/bin/env python3
"""
Setup script for the Integration Test project
This script installs all required dependencies and sets up the environment
"""

import subprocess
import sys
import os

def install_package(package):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ {package} installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {package}: {e}")
        return False

def install_requirements():
    """Install all required packages"""
    packages = [
        "flask",
        "flask-sqlalchemy", 
        "flask-cors",
        "requests",
        "reportlab",
        "selenium",
        "pytest"
    ]
    
    print("🚀 Installing required packages...")
    
    failed_packages = []
    for package in packages:
        if not install_package(package):
            failed_packages.append(package)
    
    if failed_packages:
        print(f"\n❌ Failed to install: {', '.join(failed_packages)}")
        return False
    else:
        print("\n✅ All packages installed successfully!")
        return True

def create_directories():
    """Create necessary directories"""
    directories = [
        "test_reports",
        "Users_Service/__pycache__",
        "Task_Service/__pycache__",
        "Test/__pycache__"
    ]
    
    print("📁 Creating directories...")
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            print(f"✅ Created directory: {directory}")
        else:
            print(f"📁 Directory already exists: {directory}")

def check_chrome_driver():
    """Check if Chrome and ChromeDriver are available"""
    print("🔍 Checking Chrome and ChromeDriver...")
    
    try:
        # Try to import selenium and create a webdriver
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        driver = webdriver.Chrome(options=options)
        driver.quit()
        print("✅ Chrome and ChromeDriver are working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Chrome/ChromeDriver issue: {e}")
        print("📝 Please ensure Chrome browser and ChromeDriver are installed and in PATH")
        return False

def main():
    """Main setup function"""
    print("🔧 Setting up Integration Test Environment")
    print("=" * 50)
    
    # Step 1: Install requirements
    if not install_requirements():
        print("❌ Setup failed during package installation")
        return False
    
    # Step 2: Create directories
    create_directories()
    
    # Step 3: Check Chrome/ChromeDriver
    chrome_ok = check_chrome_driver()
    if not chrome_ok:
        print("⚠️  Chrome/ChromeDriver not configured properly")
        print("   Frontend tests may fail")
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed!")
    print("\nNext steps:")
    print("1. Start the microservices:")
    print("   - cd Users_Service && python main.py")
    print("   - cd Task_Service && python main.py")
    print("   - cd Front-End && python main.py")
    print("2. Run the tests:")
    print("   - python Test/BackEnd-Test.py")
    print("   - python Test/FrontEnd-Test.py")
    print("3. Check the generated PDF reports in the 'test_reports' directory")
    
    return True

if __name__ == "__main__":
    main()
