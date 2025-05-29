# Multichannel Notification System

**👤Diego Felipe Cabrejo Suárez
---

## System Explanation

This project is a **Flask-based REST API** that simulates a **notification system** capable of delivering messages through various channels:

- **Email**
- **SMS**
- **Console**
- **Phone Call**

Each user is registered with a **preferred channel** and one or more **available fallback channels**. When a notification is triggered, the system attempts delivery through the preferred channel and falls back to others if it fails.

---

## 📡 API Endpoints

| Method | Endpoint                | Description                                             |
|--------|-------------------------|---------------------------------------------------------|
| POST   | `/users`                | Register a new user with preferred and fallback channels |
| GET    | `/users`                | List all registered users                               |
| POST   | `/notifications/send`   | Send a notification with message and priority level     |

---

## 🎯 Design Patterns

### 🔁 Chain of Responsibility
Used to implement **fallback notification delivery**. Each handler attempts to send the notification and, if it fails, delegates the task to the next handler.

- Handlers: `EmailHandler`, `SMSHandler`, `ConsoleHandler`, `PhoneCallHandler`
- Benefits: Separation of concerns, flexible and extendable channel addition.

### 🔄 Strategy Pattern
Used to dynamically format the message content based on the **priority** level.

- Strategies: `HighPriorityStrategy`, `NormalPriorityStrategy`
- Benefits: Clean abstraction of message formatting logic and easy to extend with new strategies (e.g., `UrgentPriorityStrategy`).

### 🧾 Singleton Pattern (optional)
Used in the `NotificationLogger` to ensure all components log to the **same instance**.

- Benefit: Centralized tracking of delivery attempts.

---

## 🛠️ Setup Instructions

1. 🐍 Make sure you have Python installed.
2. 🧪 Create and activate a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

3. 📦 Install Flask:

```bash
pip install flask
```

4. ▶️ Run the app:

```bash
python app.py
```

Your server should now be running at:  
**`http://127.0.0.1:5000`**

---

## 🧪 Testing Instructions (via `curl`)

### ✅ Register a User

```bash
curl -X POST http://127.0.0.1:5000/users -H "Content-Type: application/json" -d '{
  "name": "Juan",
  "preferred_channel": "email",
  "available_channels": ["email", "sms", "console", "phone"]
}'
```

---

### 📋 Get All Users

```bash
curl http://127.0.0.1:5000/users
```

---

### ✉️ Send a Notification

```bash
curl -X POST http://127.0.0.1:5000/notifications/send -H "Content-Type: application/json" -d '{
  "user_name": "Juan",
  "message": "Reminder: Class starts at 7AM.",
  "priority": "high"
}'
```

---


