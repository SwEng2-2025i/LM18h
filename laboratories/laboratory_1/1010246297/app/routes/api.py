from flask import Flask, request, jsonify
from app import app
from app.models.user import User
from app.utils.logger import Logger
from app.notifications.notification_service import NotificationService


# Temporary in-memory user storage
users = []  
logger = Logger()
notification_service = NotificationService()


@app.route('/users', methods=['POST'])
def register_user():
    """
    Register a new user
    ---
    parameters:
      - name: body
        in: body
        required: True
        schema:
          type: object
          required:
            - name
            - preferred_channel
            - available_channels
          properties:
            name:
              type: string
              description: User's name
            preferred_channel:
              type: string
              enum: [email, sms, console]
              description: Preferred notification channel
            available_channels:
              type: array
              items:
                type: string
                enum: [email, sms, console]
              description: List of available channels
    responses:
      201:
        description: User successfully registered
        examples:
          application/json: {"message": "User Juan correctly registered."}
      400:
        description: Invalid input
    """
    data = request.get_json()

    if not all(field in data for field in ['name', 'preferred_channel', 'available_channels']):
        return jsonify({"error": "Missing required fields"}), 400
    
    preferred = data["preferred_channel"].lower()
    available = [channel.lower() for channel in data["available_channels"]]

    VALID_CHANNELS = notification_service.get_supported_channels()
    if any(channel not in VALID_CHANNELS for channel in available):
        return jsonify({"error": "One or more available channels are invalid."}), 400
    
    if preferred not in available:
        return jsonify({"error": "Preferred channel must be one of the available channels."}), 400

    user = User(
        name=data["name"],
        preferred_channel=preferred,
        available_channels=available
    )
    
    users.append(user)
    return jsonify({"message": f"User {user.name} correctly registered."}), 201


@app.route('/users', methods=['GET'])
def get_users():
    """
    Get all users
    ---
    responses:
      200:
        description: A list of users
        examples:
          application/json: [
            {
              "name": "Alice",
              "preferred_channel": "email",
              "available_channels": ["email", "sms"]
            }
          ]
    """
    return jsonify([
        {
            "name": user.name,
            "preferred_channel": user.preferred_channel,
            "available_channels": user.available_channels
        } for user in users
    ])


@app.route('/notifications/send', methods=['POST'])
def send_notification():
    """
    Send a notification to a user
    ---
    parameters:
      - name: body
        in: body
        required: True
        schema:
          type: object
          required:
            - user_name
            - message
          properties:
            user_name:
              type: string
              description: The name of the user to notify
            message:
              type: string
              description: The message to send
            priority:
              type: string
              enum: [low, normal, high]
              default: normal
              description: Priority level of the notification
    responses:
      200:
        description: Notification sent successfully
        examples:
          application/json: {
            "message": "Notification sent. See logs for details.",
            "status": "success"
          }
      404:
        description: User not found
        examples:
          application/json: {
            "error": "User not found."
          }
      500:
        description: Failed to send notification
        examples:
          application/json: {
            "message": "Notification could not be sent. See logs for details.",
            "status": "failed"
          }
    """
    data = request.get_json()
    user_name = data.get("user_name")
    message = data.get("message")
    priority = data.get("priority", "normal")

    user = next((u for u in users if u.name == user_name), None)
    if not user:
        return jsonify({"error": "User not found."}), 404

    success = notification_service.send_notification(user, message, priority)

    return jsonify({
        "message": "Notification sent. See logs for details." if success else "Notification could not be sent. See logs for details.",
        "status": "success" if success else "failed"
    }), 200 if success else 500

if __name__ == '__main__':
    app.run(debug=True)