"""
Test script for the Multichannel Notification System API
Run this after starting the Flask application to test all endpoints
"""

import requests
import json
import time

BASE_URL = "http://localhost:5000"

def test_api():
    print("🧪 Testing Multichannel Notification System API")
    print("=" * 50)
    
    # Test 1: Método GET con todos los usuarios  
    print("\n1. Testing GET /users")
    response = requests.get(f"{BASE_URL}/users")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Test 2: Registrar nuevo usuario
    print("\n2. Testing POST /users")
    new_user = {
        "name": "TestUser",
        "preferred_channel": "email",
        "available_channels": ["email", "sms", "console"]
    }
    response = requests.post(f"{BASE_URL}/users", json=new_user)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Test 3: Mandar una notificación a un usuario ya existente
    print("\n3. Testing POST /notifications/send (Alice)")
    notification = {
        "user_name": "Alice",
        "message": "Your order has been shipped!",
        "priority": "high"
    }
    response = requests.post(f"{BASE_URL}/notifications/send", json=notification)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Test 4: Envío de notificación a un usuario con canales límitados
    print("\n4. Testing POST /notifications/send (Charlie - console only)")
    notification = {
        "user_name": "Charlie",
        "message": "System maintenance scheduled for tonight",
        "priority": "medium"
    }
    response = requests.post(f"{BASE_URL}/notifications/send", json=notification)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Test 5: Envío de multiples notificaciones para probar la aleatoriedad
    print("\n5. Testing multiple notifications (Bob - SMS preferred)")
    for i in range(3):
        notification = {
            "user_name": "Bob",
            "message": f"Test notification #{i+1}",
            "priority": "low"
        }
        response = requests.post(f"{BASE_URL}/notifications/send", json=notification)
        print(f"Attempt {i+1} - Status: {response.status_code}, Channel: {response.json().get('result', {}).get('channel', 'failed')}")
        time.sleep(0.5)  # Demora pequeña entre requests
    
    # Test 6: Get logs
    print("\n6. Testing GET /logs")
    response = requests.get(f"{BASE_URL}/logs")
    print(f"Status: {response.status_code}")
    logs = response.json().get('logs', [])
    print(f"Total logs: {len(logs)}")
    print("Recent logs:")
    for log in logs[-5:]:  # Show last 5 logs
        print(f"  {log}")
    
    # Test 7: Casos de error
    print("\n7. Testing error cases")
    
    # Error 1: Usuario inválido
    print("\n7a. Notification to non-existent user")
    notification = {
        "user_name": "NonExistentUser",
        "message": "This should fail",
        "priority": "high"
    }
    response = requests.post(f"{BASE_URL}/notifications/send", json=notification)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Error 2: Prioridad inválida
    print("\n7b. Invalid priority")
    notification = {
        "user_name": "Alice",
        "message": "Invalid priority test",
        "priority": "urgent"  # Las únicas prioridades válidas son  "low", "medium" o "high"
    }
    response = requests.post(f"{BASE_URL}/notifications/send", json=notification)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    print("\n" + "=" * 50)
    print("✅ API testing completed!")
    print("📚 Visit http://localhost:5000/docs/ for interactive API documentation")

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the API server.")
        print("Make sure the Flask application is running on http://localhost:5000")
        print("Run: python app.py")
