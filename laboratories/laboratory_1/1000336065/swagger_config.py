# Not strictly needed, can define template in main.py
# For more complex configs, this is useful.
SWAGGER_TEMPLATE = {
    "swagger": "2.0",
    "info": {
        "title": "Multichannel Notification System API",
        "description": "API for managing users and sending notifications via multiple channels.",
        "version": "1.0.0",
        "contact": {
            "name": "Developer Name",
            "email": "developer@example.com"
        }
    },
    "host": "http://127.0.0.1:5000",  # Update if deployed elsewhere
    "basePath": "/",
    "schemes": [
        "http"
    ],
    "consumes": [
        "application/json"
    ],
    "produces": [
        "application/json"
    ]
}

SWAGGER_CONFIG = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/" # URL for Swagger UI
}