from flask import Flask, request, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
from models.user import User
from models.notification import Notification
from services.notification_service import NotificationService
from services.user_service import UserService
import json

app = Flask(__name__)

# Swagger configuration
SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Multichannel Notification System API"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Initialize services
user_service = UserService()
notification_service = NotificationService()

@app.route('/users', methods=['POST'])
def register_user():
    data = request.get_json()
    try:
        user = user_service.register_user(
            name=data['name'],
            preferred_channel=data['preferred_channel'],
            available_channels=data['available_channels']
        )
        return jsonify({"message": "User registered successfully", "user": user.to_dict()}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/users', methods=['GET'])
def list_users():
    users = user_service.get_all_users()
    return jsonify([user.to_dict() for user in users])

@app.route('/notifications/send', methods=['POST'])
def send_notification():
    data = request.get_json()
    try:
        result = notification_service.send_notification(
            user_name=data['user_name'],
            message=data['message'],
            priority=data.get('priority', 'normal')
        )
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True) 