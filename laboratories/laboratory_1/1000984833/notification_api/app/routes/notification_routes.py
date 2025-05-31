# app/routes/notification_routes.py

from flask import Blueprint, request, jsonify
from app.services.notification_service import send_notification
from app.utils.logger import NotificationLogger

notification_bp = Blueprint('notification_bp', __name__)

@notification_bp.route('/notifications/send', methods=['POST'])
def send():
    """
    Send a notification to a user.
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
          properties:
            user_name:
              type: string
              example: Juan
            message:
              type: string
              example: "Your appointment is tomorrow."
            priority:
              type: string
              example: high
    responses:
      200:
        description: Notification sent or failed
        schema:
          type: object
          properties:
            status:
              type: string
              example: success
            channel:
              type: string
              example: sms
      400:
        description: Missing fields
        schema:
          type: object
          properties:
            error:
              type: string
              example: Missing fields
      404:
        description: User not found
        schema:
          type: object
          properties:
            error:
              type: string
              example: User not found
    """
    data = request.get_json()
    user_name = data.get('user_name')
    message = data.get('message')
    priority = data.get('priority')  # no usamos aún

    if not all([user_name, message]):
        return jsonify({"error": "Missing fields"}), 400

    result, code = send_notification(user_name, message)
    return jsonify(result), code


@notification_bp.route('/logs', methods=['GET'])
def get_logs():
    """
    Get all notification logs.
    ---
    tags:
      - Notifications
    responses:
      200:
        description: List of all notification attempts
        schema:
          type: array
          items:
            type: object
            properties:
              timestamp:
                type: string
                example: "2025-05-30T15:45:30.123456"
              user:
                type: string
                example: Juan
              channel:
                type: string
                example: sms
              status:
                type: string
                example: success
    """
    logger = NotificationLogger()
    return jsonify(logger.get_logs()), 200
