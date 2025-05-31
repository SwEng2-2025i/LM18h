# api.py

from flask import Flask, request, jsonify
from flasgger import Swagger
from app.models import User
from app.handlers import NotificationHandler
from app.logger import LoggerSingleton
from app.swagger import swagger_template, swagger_config

app = Flask(__name__)
Swagger(app, template=swagger_template(), config=swagger_config())

users = []

@app.route("/")
def index():
    return "<h1>Welcome to the Multichannel Notification API</h1><p>Go to <a href='/docs'>Swagger UI</a></p>"

@app.route("/users", methods=["POST"])
def register_user():
    """Register a user
    ---
    parameters:
      - in: body
        name: user
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
        description: User registered
    """
    data = request.get_json()
    user = User(data['name'], data['preferred_channel'], data['available_channels'])
    users.append(user)
    return jsonify({"message": "User registered"}), 201

@app.route("/users", methods=["GET"])
def list_users():
    """List all users
    ---
    responses:
      200:
        description: List of users
    """
    return jsonify([
        {
            "name": user.name,
            "preferred_channel": user.preferred_channel,
            "available_channels": user.available_channels
        }
        for user in users
    ])

@app.route("/notifications/send", methods=["POST"])
def send_notification():
    """Send a notification
    ---
    parameters:
      - in: body
        name: payload
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
        description: Notification attempt
    """
    data = request.get_json()
    user = next((u for u in users if u.name == data['user_name']), None)
    if not user:
        return jsonify({"error": "User not found"}), 404

    logger = LoggerSingleton()
    logger.log(f"Sending notification to {user.name}: '{data['message']}'")

    # Chain of Responsibility setup
    chain = None
    last_handler = None
    for ch in user.available_channels:
        handler = NotificationHandler(ch)
        if chain is None:
            chain = handler
        if last_handler:
            last_handler.set_next(handler)
        last_handler = handler

    result = chain.handle(data['message'], user.preferred_channel)
    return jsonify({"delivered": result}), 200
