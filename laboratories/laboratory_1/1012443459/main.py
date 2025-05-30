"""
Main application entry point for the Notification System API.

This module initializes the Flask application, sets up Swagger documentation,
preloads some sample users, and registers all API routes.
"""

from flask import Flask
from flasgger import Swagger
from registries.user_registry import UserRegistry
from routes.register_routes import register_routes

app = Flask(__name__)
swagger = Swagger(app)

# Crear instancia del registro de usuarios
registry = UserRegistry()

# Usuarios precargados
registry.add_user({"name": "Juan", "preferred_channel": "email", "available_channels": ["email", "sms"]})
registry.add_user({"name": "Pablo", "preferred_channel": "sms", "available_channels": ["email", "sms", "whatsapp"]})

register_routes(app, registry)

if __name__ == '__main__':
    app.run(debug=True)
    