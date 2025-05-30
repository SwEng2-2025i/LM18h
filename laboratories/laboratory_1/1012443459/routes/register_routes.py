"""
API routes and endpoint handlers for the Notification System.

This module contains all Flask route definitions and their corresponding
handler functions for user management and notification operations.
"""

from flasgger import Swagger
from functools import wraps
from flask import request, jsonify
from handlers.notification_handler import NotificationHandler
from registries.notification_registry import NotificationRegistry


def register_routes(app, user_registry):

    @app.route('/users', methods=['GET'])
    def get_users():
        """
        Get all users
        ---
        tags:
          - Users
        responses:
          200:
            description: A list of users
            schema:
              type: array
              items:
                type: object
                properties:
                  name:
                    type: string
                  preferred_channel:
                    type: string
                  available_channels:
                    type: array
                    items:
                      type: string
          401:
            description: Unauthorized
        """

        return jsonify(user_registry.get_all_users())


    @app.route('/users', methods=['POST'])
    def register_user():
        """
        Register a new user
        ---
        tags:
          - Users
        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              required:
                - name
                - preferred_channel
                - available_channels
              properties:
                name:
                  type: string
                  description: Name of the user
                  example: Charlie
                preferred_channel:
                  type: string
                  description: Preferred communication channel
                  example: sms
                available_channels:
                  type: array
                  items:
                    type: string
                  description: User's available communication channels
                  example: [email, sms, whatsapp]
        responses:
          201:
            description: User created
            schema:
              type: object
              properties:
                name:
                  type: string
                preferred_channel:
                  type: string
                available_channels:
                  type: array
                  items:
                    type: string
          400:
            description: Invalid input
        """

        data = request.get_json()
        new_user = {"name": data["name"], 
                    "preferred_channel": data["preferred_channel"], 
                    "available_channels" : data["available_channels"]}
        user_registry.add_user(new_user)
        return jsonify(new_user), 201



    @app.route('/notifications/send', methods=['POST'])
    def send_notification():
        """
        Send a notification with message and priority
        ---
        tags:
          - Notifications
        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              required:
                - user_name
                - message
                - priority
              properties:
                user_name:
                  type: string
                  description: Name of the user
                  example: Juan
                message:
                  type: string
                  description: Notification message
                  example: Your appointment is tomorrow.
                priority:
                  type: string
                  description: Notification priority
                  example: high
        responses:
          200:
            description: Notification registered
            schema:
              type: object
              properties:
                to:
                  type: string
                  example: Juan
                message:
                  type: string
                  example: Your appointment is tomorrow.
                priority:
                  type: string
                  example: high
                status:
                  type: string
                  example: Notification registered
                channel:
                  type: string
                  example: sms
          404:
            description: User not found
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: User 'Juan' not found.
        """

        data = request.get_json()
        user_name = data.get("user_name")
        message = data.get("message")
        priority = data.get("priority")

        user = user_registry.find_user_by_name(user_name)
        if not user:
            return jsonify({"error": f"User '{user_name}' not found."}), 404

        preferred = user["preferred_channel"]
        available = user["available_channels"]

        # Creamos una cadena de responsabilidad
        head_handler = None
        current_handler = None

        # Ponemos primero el canal preferido, luego los demás sin repetir
        ordered_channels = [preferred] + [c for c in available if c != preferred]

        for channel in ordered_channels:
            handler = NotificationHandler(channel)
            if not head_handler:
                head_handler = handler
                current_handler = handler
            else:
                current_handler = current_handler.set_next(handler)

        registry = NotificationRegistry()

        result = head_handler.handle(user_name, message, priority)
        registry.add_notification(result)  # guardar la notificación
        return jsonify(result), 200
    
    @app.route('/notifications', methods=['GET'])
    def get_notifications():
        """
        Get all sent notifications
        ---
        tags:
          - Notifications
        responses:
          200:
            description: A list of notifications
            schema:
              type: array
              items:
                type: object
                properties:
                  to:
                    type: string
                  message:
                    type: string
                  priority:
                    type: string
                  channel:
                    type: string
        """

        registry = NotificationRegistry()
        return jsonify(registry.get_all_notifications())

