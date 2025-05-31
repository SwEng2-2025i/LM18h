# 🧪 Multichannel Notification System (REST API)

**Full Name:** [Your Full Name Here]

**ID Number:** 1013667322

## 📝 System Description

This project implements a simple REST API for a multichannel notification system. Users register with preferred communication channels (email, SMS, console) and the system sends notifications with automatic fallback using the Chain of Responsibility pattern.

**Features:**
- User registration with preferred and available channels
- Notification delivery with automatic retries
- Logging of all delivery attempts
- Swagger documentation

## 🏗️ Design Patterns

### 1. Chain of Responsibility 🔗
Manages notification delivery across multiple channels. If one channel fails, it automatically tries the next available channel.

**Implementation:**
- `NotificationHandler`: Abstract base class
- `EmailHandler`, `SMSHandler`, `ConsoleHandler`: Concrete handlers
- Each handler can process the request or pass it to the next one

**Advantages:**
- Decoupling between sender and receiver
- Flexibility to add/remove handlers
- Distributed responsibilities

### 2. Singleton 🎯
The Logger uses the Singleton pattern to maintain a single instance that records all system events.

**Implementation:**
- `Logger._instance`: Class variable for the single instance
- `__new__()`: Controls instance creation
- Centralized logs for the entire application

**Advantages:**
- Consistency in logging
- Global access control
- Centralized resource management

## 🚀 Installation and Execution

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python main.py
```

3. Access Swagger UI: `http://127.0.0.1:5000/apidocs/`

## 🔧 API Endpoints

### POST /users
Registers a new user with their communication channels.

**Example:**
```json
{
  "name": "John",
  "preferred_channel": "email",
  "available_channels": ["email", "sms"]
}
```

### GET /users
Lists all registered users.

### POST /notifications/send
Sends a notification to a specific user.

**Example:**
```json
{
  "user_name": "John",
  "message": "Your appointment is tomorrow.",
  "priority": "high"
}
```

## 🔍 Usage Examples

**Request format for user registration:**
```json
{
  "name": "John",
  "preferred_channel": "email",
  "available_channels": ["email", "sms"]
}
```

**Request format for sending notification:**
```json
{
  "user_name": "John",
  "message": "Your appointment is tomorrow.",
  "priority": "high"
}
```

## 📁 Project Structure

```
├── main.py              # Application entry point
├── app/
│   ├── models.py        # Data models
│   ├── services.py      # Business logic
│   ├── patterns.py      # Pattern implementations
│   └── __init__.py
├── requirements.txt     # Dependencies
└── README.md           # Documentation
```

## 🔄 Operation Flow

1. **User Registration**: User registers with preferred and available channels
2. **Notification Sending**: System tries preferred channel first
3. **Chain of Responsibility**: If it fails, it tries alternative channels in order
4. **Logging**: Singleton Logger records all attempts
5. **Response**: Returns result with channel used and attempts made

## 📊 Diagrams

### Class Diagram

```mermaid
classDiagram
    direction TB    %% Models
    class User {
        +str name
        +str preferred_channel
        +List[str] available_channels
        +to_dict() dict
    }

    class Notification {
        +str user_name
        +str message
        +str priority
        +to_dict() dict
    }

    class NotificationResult {
        +bool success
        +str channel_used
        +List[str] attempts
        +str message
        +to_dict() dict
    }

    %% Design patterns
    class Logger {
        <<Singleton>>
        -_instance Logger
        +List logs
        +log(message: str) void
        +get_logs() List
    }

    class NotificationHandler {
        <<Abstract>>
        #_next_handler NotificationHandler
        +logger Logger
        +set_next(handler: NotificationHandler) NotificationHandler
        +handle(channel: str, message: str, user_name: str)* tuple
        #_try_send(channel: str, message: str, user_name: str) bool
    }

    class EmailHandler {
        +handle(channel: str, message: str, user_name: str) tuple
    }

    class SMSHandler {
        +handle(channel: str, message: str, user_name: str) tuple
    }

    class ConsoleHandler {
        +handle(channel: str, message: str, user_name: str) tuple
    }

    class NotificationChain {
        +logger Logger
        +email_handler EmailHandler
        +sms_handler SMSHandler
        +console_handler ConsoleHandler
        +send_notification(channels: list, message: str, user_name: str) tuple
    }    %% Services
    class UserService {
        +dict users
        +logger Logger
        +register_user(name: str, preferred_channel: str, available_channels: List[str]) User
        +get_user(name: str) Optional[User]
        +get_all_users() List[User]
    }

    class NotificationService {
        +notification_chain NotificationChain
        +logger Logger
        +send_notification(user: User, notification: Notification) NotificationResult
    }

    %% Relationships
    NotificationHandler <|-- EmailHandler : extends
    NotificationHandler <|-- SMSHandler : extends
    NotificationHandler <|-- ConsoleHandler : extends
    
    NotificationHandler --> Logger : uses
    NotificationChain --> EmailHandler : contains
    NotificationChain --> SMSHandler : contains
    NotificationChain --> ConsoleHandler : contains
    NotificationChain --> Logger : uses
    
    UserService --> User : creates
    UserService --> Logger : uses
    
    NotificationService --> NotificationChain : uses
    NotificationService --> Logger : uses
    NotificationService ..> User : uses
    NotificationService ..> Notification : uses
    NotificationService ..> NotificationResult : creates
```
