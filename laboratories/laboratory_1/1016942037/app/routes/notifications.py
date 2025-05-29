from flask import Blueprint, request, jsonify
from app.routes.users import users
from app.models.channels import ChannelFactory

# Creamos el Blueprint para el grupo de rutas relacionadas con notificaciones
notifications_bp = Blueprint('notifications', __name__)

# Ruta para enviar una notificación a un usuario
@notifications_bp.route('/notifications/send', methods=['POST'])
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
              example: Tu cita es mañana.
            priority:
              type: string
              example: high
    responses:
      200:
        description: Notification status
      404:
        description: User not found
    """
    data = request.get_json()  # Obtenemos el contenido JSON del request
    user_name = data.get('user_name')
    message = data.get('message')
    priority = data.get('priority')  # Por ahora no se usa, pero se puede implementar lógica futura

    # Buscar el usuario en la lista global de usuarios
    user = next((u for u in users if u.name == user_name), None)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    # Usamos la fábrica para crear una lista de handlers según los canales disponibles del usuario
    factory = ChannelFactory()
    handlers = [factory.create_channel(name) for name in user.available_channels]

    # Enlazamos los handlers usando el patrón Chain of Responsibility
    for i in range(len(handlers) - 1):
        handlers[i].set_next(handlers[i + 1])

    # Iniciamos el manejo desde el canal preferido del usuario
    start_index = user.available_channels.index(user.preferred_channel)
    success = handlers[start_index].handle(message)

    # Devolvemos el resultado de la notificación
    return jsonify({
        "status": "sent" if success else "failed",
        "message": message,
        "via": user.available_channels[start_index:]
    })
