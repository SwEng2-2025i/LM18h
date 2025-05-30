from flask import Blueprint, request, jsonify
from app.routes.user_routes import users
from app.services.notification_handler import NotificationHandler
import logging

notification_bp = Blueprint('notification_bp', __name__)
logger = logging.getLogger(__name__)

@notification_bp.route("/notifications/send", methods=["POST"])
def send_notification():
    data = request.json
    if (not data) or ('user_id' not in data) or ('message' not in data):
        return jsonify({"error": "user_id and message required"}), 400

    user_id = data['user_id']
    message = data['message']
    priority = data.get('priority', 'normal')  # Si no se envía, se asume prioridad "normal"

    user = users.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    ordered_channels = [user.preferred_channel] + [
        ch for ch in user.channels if ch != user.preferred_channel
    ]

    logger.info(f"Sending notification with priority '{priority}' to user '{user.name}'")

    handler = NotificationHandler(ordered_channels)
    success = handler.notify(message)

    return jsonify({"success": success,
                    "channel_attempts": handler.last_attempts,
    })

