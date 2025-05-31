from flask import Blueprint, request, jsonify
from models.notification import Notification
from services.notification_service import NotificationService
from controllers.users_controller import users

# Define el blueprint para rutas relacionadas con notificaciones
notifications_bp = Blueprint('notifications', __name__)

@notifications_bp.route('/notifications/send', methods=['POST'])
def send_notification():
    data = request.json
    required_fields = ['user_name', 'message', 'priority']

    # Verifica que los campos requeridos estén presentes
    if not data or not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    # Busca el usuario por nombre
    user = next((u for u in users if u.name == data['user_name']), None)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Crea la notificación y la envía
    notification = Notification(user, data['message'], data['priority'])
    result = NotificationService().send(notification)

    # Retorna resultado según éxito o fallo
    if not result.get("success", False):
        return jsonify({
            "result": "Notification failed on all channels",
            "attempts": result.get("attempts", [])
        }), 200

    return jsonify({
        "result": "Notification sent successfully",
        "channel_used": result.get("channel_used"),
        "attempts": result.get("attempts", [])
    }), 200
