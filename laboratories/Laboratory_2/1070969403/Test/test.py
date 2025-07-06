import os
import subprocess
import sys
import time

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
    
# Run tests
tests = [
        ("BackEnd-Test.py", "Backend Integration Tests"),
        ("FrontEnd-Test.py", "Frontend E2E Tests")
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
