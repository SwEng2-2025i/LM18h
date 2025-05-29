from app.api import app


swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs"
}

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Notification API",
        "description": "API for managing users and sending notifications through different channels",
        "version": "1.0.0",
        "contact": {
            "name": "API Support",
            "email": "support@example.com"
        }
    },
    "basePath": "/",
    "schemes": ["http", "https"],
    "consumes": ["application/json"],
    "produces": ["application/json"],
    "tags": [
        {
            "name": "users",
            "description": "User management operations"
        },
        {
            "name": "notifications",
            "description": "Notification operations"
        }
    ],
    "definitions": {
        "User": {
            "type": "object",
            "required": ["name", "preferred_channel", "available_channels"],
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Name of the user"
                },
                "preferred_channel": {
                    "type": "string",
                    "description": "Preferred notification channel (email, sms, console)",
                    "enum": ["email", "sms", "console"]
                },
                "available_channels": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": ["email", "sms", "console"]
                    },
                    "description": "List of available notification channels for the user"
                }
            }
        },
        "Notification": {
            "type": "object",
            "required": ["user_name", "message", "priority"],
            "properties": {
                "user_name": {
                    "type": "string",
                    "description": "Name of the user to send notification to"
                },
                "message": {
                    "type": "string",
                    "description": "Content of the notification message"
                },
                "priority": {
                    "type": "string",
                    "description": "Priority level of the notification",
                    "enum": ["high", "medium", "low"]
                }
            }
        }
    }
}

if __name__ == "__main__":
    app.run(debug=True)