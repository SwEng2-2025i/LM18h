from flask import Blueprint, request, jsonify
from app.user import users
from app.channels.email import EmailChannel
from app.channels.sms import SMSChannel
from app.channels.console import ConsoleChannel
from app.logger import Logger

# Blueprint para las rutas relacionadas con notificaciones
notif_bp = Blueprint('notifications', __name__)

@notif_bp.route('/notifications/send', methods=['POST'])
def send_notification():
    """
    Envía una notificación a un usuario usando su canal preferido.
    Si el envío falla, se intenta con los siguientes canales disponibles
    utilizando el patrón Chain of Responsibility.
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: Notification
          properties:
            user_name:
              type: string
            message:
              type: string
            priority:
              type: string
    responses:
      200:
        description: Resultado del intento de notificación
      404:
        description: Usuario no encontrado
      400:
        description: Usuario sin canales disponibles
    """
    data = request.json
    user_name = data.get('user_name')
    message = data.get('message')

    if user_name not in users:
        return jsonify({"error": "Usuario no registrado"}), 404

    user = users[user_name]
    user['name'] = user_name  # Para usar en los logs

    # Diccionario de objetos de canal
    channel_objects = {
        'email': EmailChannel(),
        'sms': SMSChannel(),
        'console': ConsoleChannel()
    }

    available = user['available']
    if not available:
        return jsonify({"error": "El usuario no tiene canales disponibles"}), 400

    # Construcción de la cadena de responsabilidad
    first = channel_objects[available[0]]
    current = first
    for ch_name in available[1:]:
        current = current.set_next(channel_objects[ch_name])

    Logger().log(f"🔔 Enviando notificación a {user_name}: {message}")
    result = first.send(message, user)

    return jsonify({"resultado": result})