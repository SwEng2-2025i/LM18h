from flask import Blueprint, request, jsonify
from app.routes.user import users_db, require_auth
from app.core.handler import ChannelHandler


notifications_bp = Blueprint("notifications", __name__)

@notifications_bp.route('/notifications/send', methods=['POST'])
@require_auth
def send_notification():
    """
    Send a notification to a user
    ---
    parameters:
      - name: Authorization
        in: header
        required: true
        type: string
      - in: body
        name: body
        required: true
        schema:
          required: [user_name, message]
          properties:
            user_name:
              type: string
              example: Valentina
            message:
              type: string
              example: Your appointment is tomorrow
            priority:
              type: string
              example: high
    responses:
      200:
        description: Notification status
      404:
        description: User not found
    """
    data = request.get_json()
    name = data.get("user_name")
    message = data.get("message")

    # Retrieve user from in-memory users database
    user = users_db.get(name)
    if not user:
        return jsonify({"error": "User not found"}), 404

     # Create a chain of handlers for each available channel of the user
    handlers = [ChannelHandler(ch) for ch in user.available_channels]

    # Link each handler to the next to form the chain of responsibility
    for i in range(len(handlers) - 1):
        handlers[i].set_next(handlers[i + 1])

    # Start handling notification sending from the first handler
    delivered = handlers[0].handle(message)

    # Return whether the notification was delivered successfully
    return jsonify({"delivered": delivered})
