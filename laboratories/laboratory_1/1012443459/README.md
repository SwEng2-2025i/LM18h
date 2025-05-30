# Notification System API

**Julio Cesar Albadan** 

A Flask-based REST API for user management and notification delivery using a chain of responsibility pattern.

## System Overview

This system allows:
- User registration with preferred and available communication channels
- Sending notifications to users through their preferred channel with automatic fallback to alternative channels
- Tracking all sent notifications

The system implements two key design patterns:
1. **Chain of Responsibility** - For handling notification delivery attempts through multiple channels
2. **Singleton** - For managing the notification registry

## 🔧 API Endpoints

| Method | Endpoint              | Description |
|--------|-----------------------|-------------|
| POST   | `/users`              | Register user |
| GET    | `/users`              | List users |
| POST   | `/notifications/send` | Send a notification |
| GET    | `/notifications`      | List sent notifications |

### Users

#### Register a new user

POST /users

**Request:**
```json
{
  "name": "Juan",
  "preferred_channel": "email",
  "available_channels": ["email", "sms"]
}
```

#### List all users

GET /users

### Notifications

#### Send a notification

POST /notifications/send

**Request:**

```json
{
  "user_name": "Juan",
  "message": "Your appointment is tomorrow.",
  "priority": "high"
}
```

#### List all notifications

GET /notifications

### System Architecture
                   ┌──────────────────┐        ┌────────────────────────┐
                   │   UserRegistry   │        │  NotificationRegistry  │
                   ├──────────────────┤        ├────────────────────────┤
                   │ - _users: list   │        │ - _notifications: list │
                   ├──────────────────┤        ├────────────────────────┤
                   │ + add_user()     │        │ + add_notification()   │
                   │ + get_all_users()│        │ + get_all_notifs()     │
                   │ + find_user()    │        └────────────────────────┘
                   └──────────────────┘                   ▲
                           ▲                              │
                           │                      ┌───────┴────────┐
                           │                      │   Singleton    │
                           │                      └────────────────┘
                           │
      ┌────────────────────┴─────┐        ┌────────────────────────┐
      │       Flask App          │        │  NotificationHandler   │
      ├──────────────────────────┤        ├────────────────────────┤
      │ - routes                 │        │ - channel: str         │
      │ - swagger docs           │        │ - next_handler         │
      └──────────────────────────┘        ├────────────────────────┤
                                          │ + set_next()           │
                                          │ + handle()             │
                                          └────────────────────────┘


#### Design Pattern Justifications
Chain of Responsibility (NotificationHandler)
- Allows flexible handling of notification delivery through multiple channels
- Automatically falls back to alternative channels if preferred channel fails
- Makes it easy to add new channel types without modifying existing code

Singleton (NotificationRegistry)
- Ensures all notifications are tracked in a single, centralized location
- Prevents duplicate registry instances
- Provides global access point for notification history


### 🚀 Setup Instructions
- Install dependencies (requirements.txt)
- Run the application:

```powershell
python app.py
```

- Access the API documentation at:
http://localhost:5000/apidocs/

🧪 Testing Examples
Using cURL

- Register a new user:

```bash
curl -X POST http://localhost:5000/users \
-H "Content-Type: application/json" \
-d '{"name":"Maria","preferred_channel":"whatsapp","available_channels":["whatsapp","sms","email"]}'
```

Response example:
```
{
  "available_channels": [
    "whatsapp",
    "sms",
    "email"
  ],
  "name": "Maria",
  "preferred_channel": "whatsapp"
}
```
- Send a notification
```bash
curl -X POST http://localhost:5000/notifications/send \
-H "Content-Type: application/json" \
-d '{"user_name":"Maria","message":"Test message","priority":"high"}'
```
Response example:
```
{
  "channel": "sms",
  "message": "Test message",
  "priority": "high",
  "status": "Notification registered",
  "to": "Maria"
}
```
- View all notifications
```bash
curl http://localhost:5000/notifications
```
Response example:
```
[
  {
    "channel": "sms",
    "message": "Test message",
    "priority": "high",
    "status": "Notification registered",
    "to": "Maria"
  }
]
```
