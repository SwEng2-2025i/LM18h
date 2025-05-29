from  loggerSingleton import Logger
from flasgger import Swagger
from flask import Flask, jsonify, request
from data import getAllUsers, getUserInfo, loadUserInfo
from notificationService import sendNotification


app = Flask(__name__)
swagger = Swagger(app)

# New user
@app.route('/users', methods=['POST'])
def user():
    """
    Register a new user
    ---
    tags:
      - Users
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - name
              - preferred_channel
              - available_channels
            properties:
              name:
                type: string
                example: Pablo
              preferred_channel:
                type: string
                example: email
              available_channels:
                type: array
                items:
                  type: string
                example: ["email", "SMS", "console"]
    responses:
      201:
        description: User registered successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: User registered successfully
      400:
        description: Missing fields or invalid preferred channel
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: Missing fields
    """
    data = request.get_json()

    required_fields = {"name", "preferred_channel", "available_channels"}
    if not required_fields.issubset(data.keys()):
        return jsonify({"error": "Missing fields"}), 400

    if data["preferred_channel"] not in data["available_channels"]:
        return jsonify({"error": "Preferred channel must be in available channels"}), 400

    loadUserInfo(data)
    return jsonify({"message": "User registered successfully"}), 201

# Get all users
@app.route('/users', methods=['GET'])
def getUser():
    """
    Get all registered users
    ---
    tags:
      - Users
    responses:
      200:
        description: List of users
        content:
          application/json:
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
    """
    return jsonify(getAllUsers()), 200

# send notification
@app.route('/notification/send', methods=["POST"])
def send():
    """
    Send a notification to a user
    ---
    tags:
      - Notifications
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - user_name
              - message
              - priority
            properties:
              user_name:
                type: string
                example: Pablo
              message:
                type: string
                example: Hello, this is a notification
              priority:
                type: integer
                example: 1
    responses:
      200:
        description: Notification processed successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: Notification processed
      404:
        description: User not found
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: User not found
    """
    info = request.get_json()
    username = info.get("user_name")
    message = info.get("message")
    priority = info.get("priority")

    user = getUserInfo(username)
    if not user:
        return jsonify({"error": "User not found"}), 404

    sendNotification(user, message, priority)
    return jsonify({"message": "Notification processed"}), 200

#Get all logs
@app.route('/logs', methods = ["GET"])
def getLogs():
    """
    Get all notification logs
    ---
    tags:
      - Logs
    responses:
      200:
        description: List of logs
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                properties:
                  timestamp:
                    type: string
                    format: date-time
                  user:
                    type: string
                  channel:
                    type: string
                  status:
                    type: string
                  message:
                    type: string
    """
    return jsonify(Logger().get_logs()), 200

if __name__ == '__main__':
    app.run(debug=True, port=4000)
