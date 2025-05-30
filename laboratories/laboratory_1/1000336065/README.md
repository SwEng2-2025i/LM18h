# 🧪 Advanced Individual Lab: Multichannel Notification System (REST API)

**Full Name:** Manuel Eduardo Quintana Umbarila

**ID Document Number:** 1000336065

## 📝 System Explanation

This project implements a REST API for a multichannel notification system. Users can register with preferred and available communication channels (email, SMS, console). When a notification is sent to a user, the system attempts delivery through their preferred channel first. If this attempt fails (simulated randomly), it falls back to other available channels in a predefined order, demonstrating the Chain of Responsibility pattern.

The system uses an in-memory data store for users and logs all notification attempts. It's built with Flask and includes Swagger documentation for API endpoints.

**Key Features:**
*   User registration with channel preferences.
*   Sending notifications with priority.
*   Chain of Responsibility for resilient notification delivery.
*   Random simulation of channel delivery failures.
*   Singleton logger for all notification attempts.
*   Factory Method for creating notification channel handlers.
*   API to retrieve notification history for a user.
*   API to retrieve a specific user's details.
*   Swagger UI for API documentation and testing.

## 🚀 Setup and Execution

1. Create a python environment and execute `pip install -r requirements.txt`
2. Run with `python3 -m app.main`

## 🔧 REST API Endpoints

The API is served at `http://127.0.0.1:5000` by default.
Swagger documentation is available at `http://127.0.0.1:5000/apidocs/`.

### User Management

*   **`POST /users`**: Register a new user.
    *   **Description:** Registers a user with their name, preferred communication channel, and a list of available channels.
    *   **Payload:**
        ```json
        {
          "name": "Alice",
          "preferred_channel": "email",
          "available_channels": ["email", "sms", "console"]
        }
        ```
    *   **Response (201 Created):**
        ```json
        {
          "message": "User registered successfully",
          "user": {
            "name": "Alice",
            "preferred_channel": "email",
            "available_channels": ["email", "sms", "console"]
          }
        }
        ```

*   **`GET /users`**: List all registered users.
    *   **Description:** Retrieves a list of all users.
    *   **Response (200 OK):**
        ```json
        [
          {
            "name": "Alice",
            "preferred_channel": "email",
            "available_channels": ["email", "sms", "console"]
          }
        ]
        ```

*   **`GET /users/{user_name}`**: Get a specific user by name.
    *   **Description:** Retrieves details for a specific user.
    *   **Example:** `GET /users/Alice`
    *   **Response (200 OK):**
        ```json
        {
          "name": "Alice",
          "preferred_channel": "email",
          "available_channels": ["email", "sms", "console"]
        }
        ```
    *   **Response (404 Not Found):** If user does not exist.

### Notification Management

*   **`POST /notifications/send`**: Send a notification to a user.
    *   **Description:** Sends a notification. Attempts delivery via preferred channel, then fallbacks.
    *   **Payload:**
        ```json
        {
          "user_name": "Alice",
          "message": "Your package has arrived!",
          "priority": "high"
        }
        ```
    *   **Response (200 OK):**
        ```json
        {
          "user_name": "Alice",
          "message_sent": "Your package has arrived!",
          "status": "DELIVERED" 
        } 
        ```
        (Status can also be `DELIVERY_ATTEMPTED_FAILED_ALL_CHANNELS` or `FAILED_NO_CHANNELS`)

*   **`GET /users/{user_name}/notifications`**: Get notification history for a user.
    *   **Description:** Retrieves all logged notification attempts for a specific user.
    *   **Example:** `GET /users/Alice/notifications`
    *   **Response (200 OK):**
        ```json
        [
          {
            "timestamp": "2025-05-27T10:30:00.123Z",
            "user_name": "Alice",
            "channel": "email",
            "message": "Your package has arrived!",
            "priority": "high",
            "status": "SUCCESS",
            "details": ""
          },
          {
            "timestamp": "2025-05-27T10:29:50.000Z",
            "user_name": "Alice",
            "channel": "sms",
            "message": "Another message",
            "priority": "medium",
            "status": "FAILURE",
            "details": ""
          }
        ]
        ```

### Admin Endpoints

*   **`DELETE /admin/logs/clear`**: Clear all notification logs.
    *   **Description:** (For testing/admin) Clears all stored notification logs.
    *   **Response (200 OK):**
        ```json
        {
          "message": "All notification logs cleared."
        }
        ```

## 📊 Class/Module Diagram (Mermaid)



```mermaid
classDiagram
    direction LR

    class FlaskApp {
        +run()
        +route()
    }

    class UserService {
        +users_db: Dict
        +register_user(name, preferred, available) User
        +get_all_users() List~User~
        +get_user_by_name(name) User
    }

    class NotificationService {
        +factory: ChannelHandlerFactory
        +send_notification(user_name, message, priority) Dict
    }

    class User {
        +name: str
        +preferred_channel: str
        +available_channels: List~str~
        +to_dict() Dict
    }

    class NotificationData {
        +user_name: str
        +message: str
        +priority: str
    }

    class AppLogger {
        <<Singleton>>
        -_instance: AppLogger
        -_log_entries: List
        +get_instance() AppLogger
        +log_attempt(user, channel, msg, status, priority, details)
        +get_logs(user_name) List
        +clear_logs()
    }

    class NotificationHandler {
        <<Abstract>>
        #_next_handler: NotificationHandler
        #logger: AppLogger
        +set_next(handler) NotificationHandler
        +handle_notification(user, notification_data)* bool
        #_simulate_delivery(channel, user, notification_data) bool
    }

    class EmailHandler {
        +CHANNEL_NAME: str
        +handle_notification(user, notification_data) bool
    }

    class SMSHandler {
        +CHANNEL_NAME: str
        +handle_notification(user, notification_data) bool
    }

    class ConsoleHandler {
        +CHANNEL_NAME: str
        +handle_notification(user, notification_data) bool
    }

    class ChannelHandlerFactory {
        <<Factory>>
        -_handler_map: Dict
        +create_handler(channel_type) NotificationHandler
        +get_supported_channels() List~str~
    }

    class Errors {
        +UserNotFoundError
        +InvalidUsageError
        +register_error_handlers(app)
    }

    %% Relationships
    UserService ..> User : creates/manages
    NotificationService ..> NotificationData : creates
    NotificationHandler ..> AppLogger : uses
    NotificationHandler ..> User : uses
    NotificationHandler ..> NotificationData : uses
    EmailHandler --|> NotificationHandler : extends
    SMSHandler --|> NotificationHandler : extends
    ConsoleHandler --|> NotificationHandler : extends
    ChannelHandlerFactory ..> EmailHandler : creates
    ChannelHandlerFactory ..> SMSHandler : creates
    ChannelHandlerFactory ..> ConsoleHandler : creates
    NotificationService ..> ChannelHandlerFactory : uses
    FlaskApp ..> UserService : uses
    FlaskApp ..> NotificationService : uses
    FlaskApp ..> AppLogger : uses
    FlaskApp ..> Errors : uses