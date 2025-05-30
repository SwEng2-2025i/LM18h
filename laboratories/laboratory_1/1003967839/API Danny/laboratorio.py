from flask import Flask, request, jsonify
from utils.logger import Logger
from services import user_service, notification_service  # Importación corregida

app = Flask(__name__)

@app.route('/')
def home():
    return "API de Danny"

@app.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        user = user_service.create_user(
            name=data['name'],
            preferred_channel=data['preferred_channel'],
            available_channels=data['available_channels']
        )
        return jsonify({
            "name": user.name,
            "preferred_channel": user.preferred_channel,
            "available_channels": user.available_channels
        }), 201
    except KeyError as e:
        return jsonify({"error": f"Missing required field: {str(e)}"}), 400

@app.route('/users', methods=['GET'])
def get_users():
    users = user_service.get_all_users()
    return jsonify([{
        "name": user.name,
        "preferred_channel": user.preferred_channel,
        "available_channels": user.available_channels
    } for user in users])

@app.route('/notifications/send', methods=['POST'])
def send_notification():
    try:
        data = request.get_json()
        user = user_service.get_user_by_name(data['user_name'])
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        result = notification_service.send_notification(
            user=user,
            message=data['message'],
            priority=data['priority']
        )
        
        return jsonify(result)
    except KeyError as e:
        return jsonify({"error": f"Missing required field: {str(e)}"}), 400

@app.route('/logs', methods=['GET'])
def get_logs():
    logger = Logger()
    return jsonify({"logs": logger.get_logs()})

if __name__ == '__main__':
    app.run(debug=True)