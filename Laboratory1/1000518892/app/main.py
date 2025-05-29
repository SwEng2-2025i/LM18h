from flask import Flask, jsonify, request
from flasgger import Swagger
from services.user_service import UserService
from services.logger import Logger

app = Flask(__name__)
swagger = Swagger(app)

user_service = UserService()

@app.route('/')
def index():
    return "Multichannel Notification API"

@app.route('/users', methods=['POST'])
def create_user():
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
          id: User
          required:
            - name
            - preferred_channel
            - available_channels
          properties:
            name:
              type: string
              example: Juan
            preferred_channel:
              type: string
              example: email
            available_channels:
              type: array
              items:
                type: string
              example: [email, sms, console]
    responses:
      200:
        description: User created
      400:
        description: Missing data
    """
    data = request.get_json()
    name = data.get("name")
    preferred = data.get("preferred_channel")
    available = data.get("available_channels")

    if not name or not preferred or not available:
        return {"error": "Missing data"}, 400

    user_service.add_user(name, preferred, available)
    return {"message": f"User {name} created successfully"}

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
        schema:
          type: array
          items:
            properties:
              name:
                type: string
              preferred_channel:
                type: string
              available_channels:
                type: array
                items:
                  type: string
    """
    users = user_service.get_all_users()
    return jsonify([{
        "name": user.name,
        "preferred_channel": user.preferred_channel,
        "available_channels": user.available_channels
    } for user in users])

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
          id: Notification
          required:
            - user_name
            - message
            - priority
          properties:
            user_name:
              type: string
              example: Juan
            message:
              type: string
              example: Your appointment is tomorrow.
            priority:
              type: string
              example: high
    responses:
      200:
        description: Notification sent result
      400:
        description: Missing or invalid data
      404:
        description: User not found
    """
    data = request.get_json()
    user_name = data.get("user_name")
    message = data.get("message")
    priority = data.get("priority")

    user = user_service.get_user(user_name)
    if not user:
        return {"error": f"User {user_name} not found"}, 404

    first_channel = user.build_channel_chain()
    if not first_channel:
        return {"error": "User has no available channels"}, 400

    logger = Logger()
    logger.log(f"Notification request for {user_name} (priority: {priority})")

    result = first_channel.handle(message)
    logger.log(f"Final result: {result}")

    return {"result": result}

if __name__ == "__main__":
    app.run(debug=True)
