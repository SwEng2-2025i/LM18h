from flask import Blueprint, request, jsonify
from app.services.notification_service import NotificationService

notifications_bp = Blueprint('notifications', __name__)
notification_service = NotificationService()

@notifications_bp.route('/notifications/send', methods=['POST'])
def send_notification():
    """
    Enviar una notificación a un usuario
    ---
    tags:
      - Notificaciones
    parameters:
      - in: body
        name: body
        required: true
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
              example: "Hola, tienes una nueva notificación"
            priority:
              type: string
              enum: [high, low]
              example: high
    responses:
      200:
        description: Notificación enviada correctamente
        schema:
          type: object
          properties:
            message:
              type: string
      400:
        description: Faltan datos
        schema:
          type: object
          properties:
            error:
              type: string
      404:
        description: Usuario no encontrado
        schema:
          type: object
          properties:
            error:
              type: string
      500:
        description: Error interno
        schema:
          type: object
          properties:
            error:
              type: string
    """
    data = request.get_json()
    user_name = data.get("user_name")
    message = data.get("message")
    priority = data.get("priority")

    if not all([user_name, message, priority]):
        return jsonify({"error": "Faltan datos"}), 400

    try:
        result, status_code = notification_service.send_notification(user_name, message, priority)
        if status_code != 200:
            return jsonify({"error": result}), status_code
        return jsonify({"message": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500