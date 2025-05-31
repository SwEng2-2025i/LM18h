from flask import Flask, request, jsonify
from flasgger import Swagger

def create_http_handler(user_services, notification_services):
    app = Flask(__name__)
    swagger = Swagger(app, template={
        "info": {
            "title": "Laboratory 1 - Multichannel Notification System (REST API) ",
            "description": "Author: Sebastián Moreno - This system implements a multichannel notification service using Flask, which allows sending notifications to users via various channels (email, SMS, or console)."
        }
    })

    @app.route("/users", methods=["POST"])
    def register_user():
        """
        Register a new user
        ---
        tags:
          - Users
        parameters:
          - in: body
            name: user
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
                  example: Alice
                preferred_channel:
                  type: string
                  enum: [email, sms, console]
                  example: email
                available_channels:
                  type: array
                  items:
                    type: string
                    enum: [sms, email, console]
                  example: ["sms", "email"]
        responses:
          201:
            description: User registered successfully
          400:
            description: Invalid input or user already exists
        """
        
        data = request.json
        
        try:
            user = user_services.register_user(data["name"], data["preferred_channel"], data["available_channels"])
            return jsonify({"name": user.name, "preferred_channel": user.preferred_channel, "available_channels": user.available_channels}), 201
        
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        
    @app.route("/users", methods=["GET"])
    def list_users():
        """
        Get a list of all users
        ---
        tags:
          - Users
        responses:
          200:
            description: A list of registered users
        """

        users = user_services.list_users()
        return jsonify([{"name": user.name, "preferred_channel": user.preferred_channel, "available_channels": user.available_channels} for user in users]), 200

    @app.route("/notifications/send", methods=["POST"])
    def notify_user():
        """
        Send a notification to a user
        ---
        tags:
          - Notifications
        parameters:
          - in: body
            name: notification
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
                  example: Alice
                message:
                  type: string
                  example: Your package has been shipped.
                priority:
                  type: string
                  example: High
        responses:
          200:
            description: Notification sent successfully
            schema:
              type: object
              properties:
                status:
                  type: string
                  example: success
                data:
                  type: object
                  properties:
                    user_name:
                      type: string
                      example: Alice
                    message:
                      type: string
                      example: Your package has been shipped.
                    priority:
                      type: string
                      example: High
                    channel_used:
                      type: string
                      example: email
                details:
                  type: string
                  example: Notification delivered successfully.
          400:
            description: Invalid user or data
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: User 'Bob' does not exist.
          503:
            description: All delivery attempts failed
            schema:
              type: object
              properties:
                status:
                  type: string
                  example: error
                data:
                  type: object
                  properties:
                    user_name:
                      type: string
                      example: Alice
                    message:
                      type: string
                      example: Your package has been shipped.
                    priority:
                      type: string
                      example: High
                details:
                  type: string
                  example: All delivery attempts failed.
        """

        data = request.json

        try:
            notification, success, channel_used = notification_services.notify_user(
                data["user_name"], data["message"], data["priority"]
            )

            if success:
                return jsonify({
                    "status": "success",
                    "data": {
                        "user_name": notification.user_name,
                        "message": notification.message,
                        "priority": notification.priority,
                        "channel_used": channel_used
                    },
                    "details": f"Notification delivered successfully."
                }), 200
            else:
                return jsonify({
                    "status": "error",
                    "data": {
                        "user_name": notification.user_name,
                        "message": notification.message,
                        "priority": notification.priority
                    },
                    "details": "All delivery attempts failed."
                }), 503        
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

        
    @app.route("/logs", methods=["GET"])
    def get_logs():
        """
        Get logs of all notification attempts
        ---
        tags:
          - Logs
        responses:
          200:
            description: List of notification attempts
        """

        from adapters.notification_logger import NotificationLogger
        return jsonify(NotificationLogger().get_logs()), 200
    
    return app
