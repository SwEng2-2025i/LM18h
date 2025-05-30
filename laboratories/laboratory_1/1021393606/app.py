from flask import Flask, request, jsonify
from flasgger import Swagger
from notification_chain import build_notification_chain
from logger import NotificationLogger

app = Flask(__name__)
swagger = Swagger(app)

# Almacenamiento temporal en memoria
users = {}

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
          properties:
            name:
              type: string
            preferred_channel:
              type: string
            available_channels:
              type: array
              items:
                type: string
    responses:
      201:
        description: User created successfully
      400:
        description: Missing required fields
    """
    data = request.get_json()
    name = data.get('name')
    preferred = data.get('preferred_channel')
    available = data.get('available_channels')

    if not name or not preferred or not available:
        return jsonify({'error': 'Missing required fields'}), 400

    users[name] = {
        'name': name,
        'preferred_channel': preferred,
        'available_channels': available
    }

    return jsonify({'message': f'User {name} registered successfully'}), 201

@app.route('/users', methods=['GET'])
def list_users():
    """
    List all registered users
    ---
    tags:
      - Users
    responses:
      200:
        description: List of users
    """
    return jsonify(list(users.values())), 200

@app.route('/notifications/send', methods=['POST'])
def send_notification():
    """
    Send a notification to a user
    ---
    tags:
      - Notifications
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            user_name:
              type: string
            message:
              type: string
            priority:
              type: string
    responses:
      200:
        description: Notification sent successfully
      400:
        description: Bad request
      404:
        description: User not found
      500:
        description: All delivery attempts failed
    """
    data = request.get_json()
    user_name = data.get('user_name')
    message = data.get('message')
    priority = data.get('priority', 'normal')

    user = users.get(user_name)

    if not user:
        return jsonify({'error': f'User {user_name} not found'}), 404

    handler_chain = build_notification_chain(user['available_channels'])
    success = handler_chain.handle(user, message)

    if success:
        return jsonify({'message': 'Notification sent successfully'}), 200
    else:
        return jsonify({'error': 'All delivery attempts failed'}), 500

@app.route('/notifications/logs', methods=['GET'])
def get_logs():
    """
    Get notification logs
    ---
    tags:
      - Logs
    responses:
      200:
        description: List of notification logs
    """
    logger = NotificationLogger()
    return jsonify(logger.get_logs()), 200

if __name__ == '__main__':
    app.run(debug=True)
