from flask import Flask, request, jsonify
from logger import Logger
from flasgger import Swagger
import notification_handler as handler

app = Flask(__name__)
log = Logger()
swagger = Swagger(app)

users = [
    {
        "name": "Juan",
        "preferred_channel": "email",
        "available_channels": ["email", "sms"]
    },
    {
        "name": "Diego",
        "preferred_channel": "sms",
        "available_channels": ["email", "sms"]
    },
]

@app.post("/users")
def create_user():
    """
    Create a new user
    ---
    parameters:
      - in: body
        name: user
        description: Information of the user that is going to be created
        schema:
            type: object
            required:
                - name
                - preferred_channel
                - available_channels
            properties:
                name:
                    type: string
                    example: Felipe
                preferred_channel:
                    type: string
                    example: sms
                available_channels:
                    type: array
                    items:
                        type: string
                    example: [console, sms]

    responses:
        201:
            description: A user was created
    """
    data = request.get_json()
    user = {
        "name": data["name"],
        "preferred_channel": data["preferred_channel"],
        "available_channels": data["available_channels"]
    }
    users.append(user)
    return jsonify(user), 201

@app.get("/users")
def get_users():
    """
    Return users
    ---
    responses:
        200:
            description: Users returned successfully
    """
    return jsonify(users), 200

@app.route("/notifications/send", methods=['POST'])
def send_message():
    """
    Send a notification
    ---
    parameters:
      - in: body
        name: user
        description: Information of the user that is going to be created
        schema:
            type: object
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
                    example: Hi!
                priority:
                    type: string
                    example: low
    responses:
        200:
            description: Message sent sucesfully
        400:
            description: User doesn't exist or none of the channels worked
    """
    data = request.json
    result = {}
    for user in users:
        if user["name"] == data["user_name"]:
            result = user
            break
    
    if result == {}:
        return jsonify({"error": "The user doesn't exist"}), 400

    channel_order = [result["preferred_channel"]]
    for channel in result["available_channels"]:
        if channel not in channel_order:
            channel_order.append(channel)

    chain = None

    for channel in reversed(channel_order):
        if channel == "console":
            chain = handler.consoleHandler(chain)
        elif channel == "sms":
            chain = handler.smsHandler(chain)
        elif channel == "email":
            chain = handler.emailHandler(chain)

    response = chain.handle(data, log)

    if response:
        return jsonify({"message": "The notification was sent"}), 200
    else:
        return jsonify({"error": "The notification can't be sent"}), 400

@app.route("/notifications", methods=['GET'])
def logs():
    """
    Return all the notification attempts
    ---
    responses:
        200:
            description: Users returned successfully
    """
    return jsonify(log.logs), 200

if __name__ == "__main__":
    app.run(debug=True)
