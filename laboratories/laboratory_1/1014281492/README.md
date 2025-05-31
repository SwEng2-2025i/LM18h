# Multichannel Notification System REST API

## System Overview
This is a REST API implementation of a multichannel notification system that allows users to register with multiple communication channels and receive notifications through their preferred channels with fallback options.

## Design Patterns Used
1. **Chain of Responsibility Pattern**: Used for handling notification delivery through different channels with fallback mechanisms.
2. **Singleton Pattern**: Implemented for the logger to ensure a single instance throughout the application.
3. **Factory Pattern**: Used for creating different types of notification handlers.

## API Documentation

### Endpoints

#### Register User
- **POST** `/users`
- **Description**: Register a new user with their preferred and available notification channels
- **Request Body**:
```json
{
  "name": "Juan",
  "preferred_channel": "email",
  "available_channels": ["email", "sms"]
}
```

#### List Users
- **GET** `/users`
- **Description**: Retrieve a list of all registered users

#### Send Notification
- **POST** `/notifications/send`
- **Description**: Send a notification to a specific user
- **Request Body**:
```json
{
  "user_name": "Juan",
  "message": "Your appointment is tomorrow.",
  "priority": "high"
}
```

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

## Testing
Run the test suite using pytest:
```bash
pytest
```

## Class Diagram
```
[User] 1--* [NotificationChannel]
[NotificationHandler] <|-- [EmailHandler]
[NotificationHandler] <|-- [SMSHandler]
[NotificationHandler] <|-- [ConsoleHandler]
[Logger] (Singleton)
```

## Author
Mateo Vivas 